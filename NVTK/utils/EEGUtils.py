import warnings
import mne
import matplotlib.pyplot as plt
import numpy as np
from mne.utils import verbose, logger
from mne.io.meas_info import create_info
from mne.io.base import BaseRaw

STD_EEG_CHANNEL_NAMES = ["Fp1", "Fp2", "C3", "C4", "P7", "P8", "O1", "O2",
                         "F7", "F8", "F3", "F4", "T7", "T8", "P3", "P4"]

def parse_eeg_data(sample, channel, aux):
    id_str = str(sample) + ', '
    channel_str = ''
    for i in channel:
        channel_str = channel_str + str(i)[:-9] + ", "

    aux_str = ''
    for i in aux:
        aux_str = aux_str + str(i) + ', '

    data_str = id_str + channel_str + aux_str + '\n'
    return data_str

class OpenBCItoMNERaw(BaseRaw):
    """
    This class is essentially an exact replica of the class "RawOpenBCI"
    from the OpenBCI_Python/externals module. Attempting to use that method indicated
    that the class also needed to override the _read_segment method so that the
    data is passed back from the _read_segment_file method. The offset parameter also
    had to be removed from the _read_segment method.

    Credit for 99% of the code goes to the origianl author, Teon Brooks
    """

    def __init__(self, input_fname, montage=None, eog=None,
                 misc=(-3, -2, -1), stim_channel=None, scale=1e-6, sfreq=250,
                 missing_tol=1, preload=True, verbose=None):

        bci_info = {'missing_tol': missing_tol, 'stim_channel': stim_channel}
        if not eog:
            eog = list()
        if not misc:
            misc = list()
        nsamps, nchan = self._get_data_dims(input_fname)

        last_samps = [nsamps - 1]
        ch_names = ['EEG %03d' % num for num in range(1, nchan + 1)]
        ch_types = ['eeg'] * nchan
        if misc:
            misc_names = ['MISC %03d' % ii for ii in range(1, len(misc) + 1)]
            misc_types = ['misc'] * len(misc)
            for ii, mi in enumerate(misc):
                ch_names[mi] = misc_names[ii]
                ch_types[mi] = misc_types[ii]
        if eog:
            eog_names = ['EOG %03d' % ii for ii in range(len(eog))]
            eog_types = ['eog'] * len(eog)
            for ii, ei in enumerate(eog):
                ch_names[ei] = eog_names[ii]
                ch_types[ei] = eog_types[ii]
        if stim_channel:
            ch_names[stim_channel] = 'STI 014'
            ch_types[stim_channel] = 'stim'

        # fix it for eog and misc marking
        info = create_info(ch_names, sfreq, ch_types, montage)
        super(OpenBCItoMNERaw, self).__init__(info, last_samps=last_samps,
                                         raw_extras=[bci_info],
                                         filenames=[input_fname],
                                         preload=False, verbose=verbose)
        # load data
        if preload:
            self.preload = preload
            logger.info('Reading raw data from %s...' % input_fname)
            self._data = self._read_segment()

    def _read_segment(self, start=0, stop=None, sel=None, data_buffer=None,
                      projector=None, verbose=None):
        """Read a chunk of raw data.

        Parameters
        ----------
        start : int, (optional)
            first sample to include (first is 0). If omitted, defaults to the
            first sample in data.
        stop : int, (optional)
            First sample to not include.
            If omitted, data is included to the end.
        sel : array, optional
            Indices of channels to select.
        data_buffer : array or str, optional
            numpy array to fill with data read, must have the correct shape.
            If str, a np.memmap with the correct data type will be used
            to store the data.
        projector : array
            SSP operator to apply to the data.
        verbose : bool, str, int, or None
            If not None, override default verbose level (see
            :func:`mne.verbose` and :ref:`Logging documentation <tut_logging>`
            for more).

        Returns
        -------
        data : array, [channels x samples]
           the data matrix (channels x samples).
        """
        #  Initial checks
        start = int(start)
        stop = self.n_times if stop is None else min([int(stop), self.n_times])

        if start >= stop:
            raise ValueError('No data in this range')

        #  Initialize the data and calibration vector
        n_sel_channels = self.info['nchan'] if sel is None else len(sel)
        assert n_sel_channels <= self.info['nchan']
        # convert sel to a slice if possible for efficiency
        if sel is not None and len(sel) > 1 and np.all(np.diff(sel) == 1):
            sel = slice(sel[0], sel[-1] + 1)
        idx = slice(None, None, None) if sel is None else sel
        data_shape = (n_sel_channels, stop - start)
        dtype = self._dtype
        if isinstance(data_buffer, np.ndarray):
            if data_buffer.shape != data_shape:
                raise ValueError('data_buffer has incorrect shape: %s != %s'
                                 % (data_buffer.shape, data_shape))
            data = data_buffer
        elif isinstance(data_buffer, str):
            # use a memmap
            data = np.memmap(data_buffer, mode='w+',
                             dtype=dtype, shape=data_shape)
        else:
            data = np.zeros(data_shape, dtype=dtype)

        # deal with having multiple files accessed by the raw object
        cumul_lens = np.concatenate(([0], np.array(self._raw_lengths,
                                                   dtype='int')))
        cumul_lens = np.cumsum(cumul_lens)
        files_used = np.logical_and(np.less(start, cumul_lens[1:]),
                                    np.greater_equal(stop - 1,
                                                     cumul_lens[:-1]))

        # set up cals and mult (cals, compensation, and projector)
        cals = self._cals.ravel()[np.newaxis, :]
        if self._comp is not None:
            if projector is not None:
                mult = self._comp * cals
                mult = np.dot(projector[idx], mult)
            else:
                mult = self._comp[idx] * cals
        elif projector is not None:
            mult = projector[idx] * cals
        else:
            mult = None
        cals = cals.T[idx]

        # read from necessary files
        offset = 0
        for fi in np.nonzero(files_used)[0]:
            start_file = self._first_samps[fi]
            # first iteration (only) could start in the middle somewhere
            if offset == 0:
                start_file += start - cumul_lens[fi]
            stop_file = np.min([stop - cumul_lens[fi] + self._first_samps[fi],
                                self._last_samps[fi] + 1])
            if start_file < self._first_samps[fi] or stop_file < start_file:
                raise ValueError('Bad array indexing, could be a bug')
            n_read = stop_file - start_file
            this_sl = slice(offset, offset + n_read)
            data = self._read_segment_file(data[:, this_sl], idx, fi,
                                    int(start_file), int(stop_file),
                                    cals, mult)
            offset += n_read
        return data

    def _read_segment_file(self, data, idx, fi, start, stop,
                           cals, mult):
        """Read a chunk of raw data"""
        input_fname = self._filenames[fi]
        data_ = np.genfromtxt(input_fname, delimiter=',', comments='%',
                              skip_footer=1)
        """
        Dealing with the missing data
        -----------------------------
        When recording with OpenBCI over Bluetooth, it is possible for some of
        the data packets, samples, to not be recorded. This does not happen
        often but it poses a problem for maintaining proper sampling periods.
        OpenBCI data format combats this by providing a counter on the sample
        to know which ones are missing.

        Solution
        --------
        Interpolate the missing samples by resampling the surrounding samples.
        1. Find where the missing samples are.
        2. Deal with the counter reset (resets after cycling a byte).
        3. Resample given the diffs.
        4. Insert resampled data in the array using the diff indices
           (index + 1).
        5. If number of missing samples is greater than the missing_tol, Values
           are replaced with np.nan.
        """
        # counter goes from 0 to 255, maxdiff is 255.
        # make diff one like others.
        missing_tol = self._raw_extras[fi]['missing_tol']
        diff = np.abs(np.diff(data_[:, 0]))
        diff = np.mod(diff, 254) - 1
        missing_idx = np.where(diff != 0)[0]
        missing_samps = diff[missing_idx].astype(int)

        if missing_samps.size:
            missing_nsamps = np.sum(missing_samps, dtype=int)
            missing_cumsum = np.insert(np.cumsum(missing_samps), 0, 0)[:-1]
            missing_data = np.empty((missing_nsamps, data_.shape[-1]),
                                    dtype=float)
            insert_idx = list()
            for idx_, nn, ii in zip(missing_idx, missing_samps,
                                    missing_cumsum):
                missing_data[ii:ii + nn] = np.mean(data_[(idx_, idx_ + 1), :])
                if nn > missing_tol:
                    missing_data[ii:ii + nn] *= np.nan
                    warnings.warn('The number of missing samples exceeded the '
                                  'missing_tol threshold.')
                insert_idx.append([idx_] * nn)
            insert_idx = np.hstack(insert_idx)
            data_ = np.insert(data_, insert_idx, missing_data, axis=0)

        data_ = data_[start:stop, 1:].T

        data = np.dot(mult, data_[idx]) if mult is not None else data_[idx]
        return data

    def _get_data_dims(self, input_fname):
        """Briefly scan the data file for info"""
        # raw data formatting is nsamps by nchans + counter
        data = np.genfromtxt(input_fname, delimiter=',', comments='%',
                             skip_footer=1)
        diff = np.abs(np.diff(data[:, 0]))
        diff = np.mod(diff, 254) - 1
        missing_idx = np.where(diff != 0)[0]
        missing_samps = diff[missing_idx].astype(int)
        nsamps, nchan = data.shape
        # add the missing samples
        nsamps += sum(missing_samps)
        # remove the tracker column
        nchan -= 1
        del data

        return nsamps, nchan


def read_raw_openbci(input_fname, montage=None, eog=None, misc=(-3, -2, -1),
                     stim_channel=None, scale=1e-6, sfreq=250, missing_tol=1,
                     preload=True, verbose=None):
    """Raw object from OpenBCI file

    Parameters
    ----------
    input_fname : str
        Path to the OpenBCI file.
    montage : str | None | instance of Montage
        Path or instance of montage containing electrode positions.
        If None, sensor locations are (0,0,0). See the documentation of
        :func:`mne.channels.read_montage` for more information.
    eog : list or tuple
        Names of channels or list of indices that should be designated
        EOG channels. Default is None.
    misc : list or tuple
        List of indices that should be designated MISC channels.
        Default is (-3, -2, -1), which are the accelerator sensors.
    stim_channel : str | int | None
        The channel name or channel index (starting at 0).
        -1 corresponds to the last channel (default).
        If None, there will be no stim channel added.
    scale : float
        The scaling factor for EEG data. Units for MNE are in volts.
        OpenBCI data are typically stored in microvolts. Default scale
        factor is 1e-6.
    sfreq : int
        The sampling frequency of the data. OpenBCI defaults are 250 Hz.
    missing_tol : int
        The tolerance for interpolating missing samples. Default is 1. If the
        number of contiguous missing samples is greater than tolerance, then
        values are marked as NaN.
    preload : bool
        If True, all data are loaded at initialization.
        If False, data are not read until save.
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).

    Returns
    -------
    raw : Instance of RawOpenBCI
        A Raw object containing OpenBCI data.


    See Also
    --------
    mne.io.Raw : Documentation of attribute and methods.
    """
    raw = OpenBCItoMNERaw(input_fname=input_fname, montage=montage, eog=eog,
                     misc=misc, stim_channel=stim_channel, scale=scale,
                     sfreq=sfreq, missing_tol=missing_tol, preload=preload,
                     verbose=verbose)
    return raw
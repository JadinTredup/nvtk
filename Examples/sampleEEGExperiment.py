import argparse
import pygame
import os
import sys
import serial
import time, timeit

from threading import Thread

#from NVTK.Sensors import EEG

IMAGE_DIR = "Images"
PLACEHOLDER_FN = "RandomGnome.png"
IMG = os.path.join(IMAGE_DIR, PLACEHOLDER_FN)



#################################################################
#                                                               #
#                                                               #
#               Open BCI Global Variables                       #
#                                                               #
#                                                               #
#################################################################
BAUD_RATE = 115200
NB_CHANNELS = 8
SAMPLING_FACTOR = -1.024
SAMPLING_RATE = 256
SERVER_PORT = 12345
SERVER_IP = "localhost"
DEBUG = False
STD_PORT = '/dev/ttyUSB0'

# Check packet drop
last_id = -1

# Counter for sampling rate
nb_samples_in = -1
nb_samples_out = -1

# last seen values for interpolation
last_values = [0]*NB_CHANNELS

# Counter to trigger duplications...
leftover_duplications = 0

tick = timeit.default_timer()

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="NVTK - ERP Experiment")
    parser.add_argument('--trials', default=50, type=int,
                        help="Number of times to repeat stimulus presentation.")
    parser.add_argument('--sd', default=False,
                        help="Sets recording to SD card on-board.")

    args = parser.parse_args()
    num_trials = args.trials
    record_sd = args.sd
    time_per_trial = 5  # Seconds
    total_time = num_trials*time_per_trial

    # Initialize Pygame
    pygame.init()
    pygame.font.init()

    try:
        pygImg = pygame.image.load(IMG)
    except:
        msg = "\nNo Stimulus Available for Presentation. Exiting"
        raise(UserWarning, msg)

    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen = pygame.display.set_mode((800,470))
    screenrect = screen.get_rect()
    pygImg.convert_alpha()
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    font = pygame.font.SysFont('mono', 24, bold=True)

    # Inisitalize EEG
    #eeg = EEGMonitor()

    # Start stimulus loop
    x = 10
    y = 10
    clock = pygame.time.Clock()
    fps = 30
    playtime = 0.0
    running = True

    while running:
        milliseconds = clock.tick(fps)
        seconds = milliseconds / 1000.0
        playtime += seconds

        if playtime < 60:
            task = "Eyes Open"
        elif (playtime >= 120) & (playtime < 120):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    screen.blit(pygImg, (x, y))
                elif event.key == pygame.K_RIGHT:
                    screen.blit(background, (0,0))
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # txt = "FPS: {:.2f} Total Playtime: {:.2f}".format(clock.get_fps(), playtime)
        # txtsurface = font.render(txt, False, (0, 0, 0))
        # screen.blit(txtsurface, (300,10))

        if playtime >= total_time:
            running = False

        pygame.display.flip()

    print("Experiment over")

    #eeg.stopEEGStreaming()
    pygame.quit()
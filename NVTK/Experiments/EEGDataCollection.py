import timeit
import pygame

class eegBaseline(object):
    """
    Simple experiment for recording EEG baseline signal
        10  seconds of warm up
        2   Minutes of recording first with eyes open
        10  second intermission
        2   Minutes with eyes closed
        10  second end
    """
    def __init__(self, resolution=None):
        pygame.init()
        pygame.font.init()
        if resolution==None:
            self.screen = pygame.display.set_mode((0,0) pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(resolution)

        self.background = pygame.Surface(screen.get_size()).convert()
        self.background.fill((255, 255, 255))
        self.screen.blit(background, (0,0))
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.playtime = 0.0
        self.running = False
        self.task = None
        self.total_time = 150

    def Run(self):
        """
        Main loop for the experiment
        """
        self.running = True
        while self.running:
            milliseconds = self.clock.tick(fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds

            if self.playtime < 10:    # Warm up period
                self.task = "Warm Up"
                self.WarmUp()
            elif (self.playtime >= 10) & (self.playtime < 70):
                self.task = "Eyes Open"
                self.EyesOpen()
            elif (self.playtime >= 70) & (self.playtime < 80):
                self.task = "Intermission"
                self.Intermission()
            elif (self.playtime >= 80) & (self.playtime < 140):
                self.task = "Eyes Closed"
                self.EyesClosed()
            elif (self.playtime >= 140) & (self.playtime < 150):
                self.task = "End"
                self.Ending()
            else:
                self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            pygame.display.flip()


    def WarmUp(self):
        """

        """
        self.background.fill((0, 0, 0))
        self.screen.blit(background, (0,0))


    def EyesOpen(self):
        """

        """
        self.background.fill((255, 255, 255))
        self.screen.blit(background, (0, 0))


    def EyesClosed(self):
        """

        """
        self.background.fill((255, 255, 255))
        self.screen.blit(background, (0, 0))


    def Intermission(self):
        """

        """
        self.background.fill((255, 255, 255))
        self.screen.blit(background, (0, 0))


    def Ending(self):
        """

        """
        self.background.fill((255, 255, 255))
        self.screen.blit(background, (0, 0))

class eegMotorImageryHandsFeet(object):
    """
    Simple experiment for recording EEG baseline signal
        10  seconds of warm up
        2   Minutes of recording first with eyes open
        10  second intermission
        2   Minutes with eyes closed
        10  second end
    """
    def __init__(self, resolution=None):
        pygame.init()
        pygame.font.init()
        if resolution==None:
            self.screen = pygame.display.set_mode((0,0) pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(resolution)

        self.background = pygame.Surface(screen.get_size()).convert()
        self.background.fill((255, 255, 255))
        self.screen.blit(background, (0,0))
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.playtime = 0.0
        self.running = False
        self.task = None
        self.total_time = 150

    def Run(self):
        """
        Main loop for the experiment
        """
        self.running = True
        while self.running:
            milliseconds = self.clock.tick(fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds

            if self.playtime < 10:    # Warm up period
                self.task = "Warm Up"
                self.WarmUp()
            elif (self.playtime >= 10) & (self.playtime < 70):
                self.task = "Eyes Open"
                self.EyesOpen()
            elif (self.playtime >= 70) & (self.playtime < 80):
                self.task = "Intermission"
                self.Intermission()
            elif (self.playtime >= 80) & (self.playtime < 140):
                self.task = "Eyes Closed"
                self.EyesClosed()
            elif (self.playtime >= 140) & (self.playtime < 150):
                self.task = "End"
                self.Ending()
            else:
                self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            pygame.display.flip()
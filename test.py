import pygame
import engine
import light
import math

class Main():
    _continue_flag = True
    
    def __init__(self, width,
                 height):
        pygame.init()
        if (width == 0 or height == 0):
            self.canvas = pygame.display \
                                .set_mode(
                                         (width, height),
                                          pygame.NOFRAME |
                                          pygame.FULLSCREEN)
        else:
            self.canvas = pygame.display.set_mode((width, height), pygame.SRCALPHA)
        self.canvas.fill((40, 40, 40, 0))
        # Sets the width and height
        screen_details = pygame.display.Info()
        self.width = screen_details.current_w
        self.height = screen_details.current_h
        self.engine = engine.Engine(self.canvas)
        self.engine.load_model("../Models/teapot.obj", "teapot")
        self.engine.load_model("../Models/ship.obj", "model")
        light_test = light.Light([0, -1, -1], [0, -1, -10])
        self.engine.load_light(light_test)
    def start(self, _range=None):
        self.clock = pygame.time.Clock()

    def loop(self):
        offset = 0.1
        while self._continue_flag is True:
            self.canvas.fill((40, 40, 40))
            self.engine.translate("model", [0, 0, -10])
            self.engine.scale("teapot", [0.05, 0.05, 0.05])
            self.engine.loaded_lights[0].pos[1] = math.cos(offset/50) * 40
            self.engine.translate("teapot", self.engine.loaded_lights[0].pos)
            self.engine.render()
            offset += 1
            pygame.display.flip()
            self.clock.tick(30)
            # print(self.clock.get_fps())
            for event in pygame.event.get():
                # Quit the program if the use close the windows
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    self._continue_flag = False
                # Or press ESCAPE
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        self._continue_flag = False
main = Main(600, 600)
main.start()
main.loop()
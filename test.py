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
        self.engine.load_model("teapot.obj", "teapot")
        self.engine.load_model("teapot.obj", "teapot2")
        self.engine.loaded_models[1].color = [255, 0, 255]
        self.engine.load_light()
        light_test = light.Light(color=(255, 0, 0))
        self.engine.load_light(light_test, identifier="main2")
    def start(self, _range=None):
        self.clock = pygame.time.Clock()

    def loop(self):
        offset = 0.1
        while self._continue_flag is True:
            self.canvas.fill((0, 0, 0))
            self.engine.translate("teapot", [-3, -2, -10])
            self.engine.translate("teapot2", [3, -2, -10])
            self.engine.rotate_y("teapot", offset)
            self.engine.rotate_y("teapot2", offset)
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
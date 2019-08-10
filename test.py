import pygame
import engine
import light
import math
import helper


class Main():
    _continue_flag = True
    MOUSE_SENSITIVITY = 0.1
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
        self.yaw, self.pitch = 0, 0
        pygame.mouse.set_visible(False)
        self.engine = engine.Engine(self.canvas)
        self.engine.load_model("teapot.obj", "teapot")
        directional_light_kwargs = {'color': (255, 255, 255),
                                    'direction': [0, 0.5, -1],
                                    'intensity': 0.9,
                                    'type': 'directional'}
        directional_light = light.Light(**directional_light_kwargs)
        self.engine.load_light(directional_light, identifier="directional_light")

        ambient_light_kwargs = {'color': (255, 255, 255),
                                'intensity': 0.2,
                                'type': 'ambient'}
        ambient_light = light.Light(**ambient_light_kwargs)
        self.engine.load_light(ambient_light, identifier="ambient_light")
    def start(self, _range=None):
        self.clock = pygame.time.Clock()

    def loop(self):
        offset = 0.1
        w, a, s, d = [False] * 4
        pygame.mouse.set_pos(self.width / 2, self.height / 2)
        while self._continue_flag is True:
            self.canvas.fill((0, 0, 0))
            if (w):
                self.engine.camera.pos -= self.engine.camera.forward * (1 / self.clock.get_time() * 1.5)
            if (s):
                self.engine.camera.pos += self.engine.camera.forward * (1 / self.clock.get_time() * 1.5)
            if (a):
                self.engine.camera.pos[0] += (1 / self.clock.get_time() * 1.5)
            if (d):
                self.engine.camera.translate([-1 * (1 / self.clock.get_time() * 1.5), 0, 0])               
            self.engine.translate("teapot", [0, -2, -10])
            self.engine.rotate_y("teapot", offset)
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
                    if (event.key == pygame.K_w):
                        w = True
                    if (event.key == pygame.K_s):
                        s = True                      
                    if (event.key == pygame.K_a):
                        a = True
                    if (event.key == pygame.K_d):
                        d = True
                if (event.type == pygame.KEYUP):
                    if (event.key == pygame.K_w):
                        w = False
                    if (event.key == pygame.K_s):
                        s = False                      
                    if (event.key == pygame.K_a):
                        a = False
                    if (event.key == pygame.K_d):
                        d = False
                if (event.type == pygame.MOUSEMOTION):
                    rel = pygame.mouse.get_pos()
                    rel = rel[0] - self.width / 2, self.height / 2 - rel[1] 
                    pygame.mouse.set_pos(self.width / 2, self.height / 2)
                    pygame.event.clear(pygame.MOUSEMOTION)
                    self.yaw += rel[0] * self.MOUSE_SENSITIVITY
                    self.pitch += rel[1] * self.MOUSE_SENSITIVITY
                    if(self.pitch > 89):
                        self.pitch =  89
                    if(self.pitch < -89):
                        self.pitch = -89
                    if(self.yaw > 89):
                        self.yaw =  89
                    if(self.yaw < -89):
                        self.yaw = -89
                    self.engine.camera.rotate(math.radians(self.yaw), math.radians(self.pitch), False)



main = Main(600, 600)
main.start()
main.loop()
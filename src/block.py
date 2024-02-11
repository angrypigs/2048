from pygame import Surface, draw, font, transform, SRCALPHA
from pygame.math import Vector2

from src.utils import *



class Block:

    def __init__(self, 
                 screen: Surface,
                 value: int,
                 matrix_coords: tuple[int, int],
                 coords: tuple[int, int]) -> None:
        self.ANIM_LIMIT = 6
        self.FRAME_LIMIT = 8
        self.anim = False
        self.screen = screen
        self.origin = Surface((BLOCK_SIZE, BLOCK_SIZE), SRCALPHA)
        self.origin.set_colorkey((255, 0, 255))
        self.origin.fill((255, 0, 255))
        self.font = font.Font(res_path("assets/ClearSans-Regular.ttf"), 100)
        self.val = value // 2
        self.__increase_value()
        self.surf = self.origin.copy()
        self.coords = Vector2(coords)
        self.matrix_coords = Vector2(matrix_coords)
        self.counter = 0
        self.mode = "normal"
        self.action = ""
        for i in range(self.ANIM_LIMIT):
            self.__decrease()
        self.action = "increase"
    
    def __bool__(self) -> bool:
        return self.anim

    def __increase(self) -> None:
        self.counter += 1
        self.surf = transform.smoothscale(self.surf, tuple([x + 3 for x in self.surf.get_size()]))
        self.surf.set_colorkey((255, 0, 255))
        self.__set_coords(self.coords.x, self.coords.y)
    
    def __decrease(self) -> None:
        self.counter -= 1
        self.surf = transform.smoothscale(self.surf, tuple([x - 3 for x in self.surf.get_size()]))
        self.surf.set_colorkey((255, 0, 255))
        self.__set_coords(self.coords.x, self.coords.y)

    def __set_coords(self, x: int, y: int) -> None:
        self.blit_coords = Vector2(x - (self.surf.get_width() // 2),
                                y - (self.surf.get_height() // 2))

    def __increase_value(self) -> None:
        self.val *= 2
        draw.rect(self.origin, get_color(self.val), (0, 0, BLOCK_SIZE, BLOCK_SIZE),
                  0, 8)
        self.font = font.Font(res_path("assets/ClearSans-Regular.ttf"), 65 // (len(str(self.val))) + 35)
        new_font : Surface = self.font.render(f"{self.val}", True, get_font_color(self.val))
        self.origin.blit(new_font, (
            (BLOCK_SIZE - new_font.get_width()) // 2,
            (BLOCK_SIZE - new_font.get_height()) // 2
        ))
    
    def draw(self) -> None:
        self.screen.blit(self.surf, self.blit_coords)
        match self.mode:
            case "left" | "right":
                self.counter += 1
                if self.counter < len(self.movements):
                    self.coords.x = self.movements[self.counter]
                    self.__set_coords(self.coords.x, self.coords.y)
                    self.anim = True
                    return
                else:
                    self.counter = 0
                    self.mode = "normal"
                    self.anim = False
            case "up" | "down":
                self.counter += 1
                if self.counter < len(self.movements):
                    self.coords.y = self.movements[self.counter]
                    self.__set_coords(self.coords.x, self.coords.y)
                    self.anim = True
                    return
                else:
                    self.counter = 0
                    self.mode = "normal"
                    self.anim = False
        match self.action:
            case "increase":
                self.__increase()
                self.anim = True
                if self.counter == 0:
                    self.action = ""
                    self.surf = self.origin.copy()
                    self.__set_coords(self.coords.x, self.coords.y)
                    self.anim = False
                elif self.counter == self.ANIM_LIMIT:
                    self.action = "decrease"
                    self.__increase_value()
            case "decrease":
                self.__decrease()
                self.anim = True
                if self.counter == 0:
                    self.action = ""
                    self.surf = self.origin.copy()
                    self.__set_coords(self.coords.x, self.coords.y)
                    self.anim = False
                elif self.counter == -self.ANIM_LIMIT:
                    self.action = "increase"

    def move(self, 
             direction: str, 
             steps: int,
             destination: int) -> None:
        self.mode = direction
        self.movements = lerp_quadratic_reverse(
            self.coords.x if direction in ("left", "right") else self.coords.y,
            destination, self.FRAME_LIMIT
        )
        if direction in ("left", "right"):
            self.matrix_coords.x += steps
        else:
            self.matrix_coords.y += steps
   
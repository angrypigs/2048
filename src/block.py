from pygame import Surface, draw, font
from pygame.math import Vector2

from src.utils import *



class Block:

    def __init__(self, 
                 screen: Surface,
                 value: int,
                 color: tuple[int, int, int],
                 font_color: tuple[int, int, int],
                 coords: tuple[int, int]) -> None:
        self.screen = screen
        self.origin = Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.origin.set_colorkey((255, 0, 255))
        self.origin.fill((255, 0, 255))
        self.font = font.Font(res_path("assets/ClearSans-Regular.ttf"), 30)
        self.modify_block(value, color, font_color)
        self.surf = self.origin.copy()
        self.coords = Vector2(coords)
    
    def modify_block(self,
                    val: int,
                    color: tuple[int, int, int],
                    font_color: tuple[int, int, int]) -> None:
        draw.rect(self.origin, color, (0, 0, BLOCK_SIZE, BLOCK_SIZE),
                  0, 8)
        new_font : Surface = self.font.render(f"{val}", True, font_color)
        self.origin.blit(new_font, (
            (BLOCK_SIZE - new_font.get_width()) // 2,
            (BLOCK_SIZE - new_font.get_height()) // 2
        ))
    
    def draw(self) -> None:
        self.screen.blit(self.surf, self.coords)

        
        
        
        
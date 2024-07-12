import sys
import math
import pygame
import framework as fw
from variable import Variable
import character
import random


def high_x(screen: fw.Screen, picture: pygame.Surface):
    picture_width = picture.get_width()
    picture_height = picture.get_height()
    scale = picture_width / picture_height
    scale = fw.ceil(scale * screen.MAX_Y)
    return screen.true_position_x(scale)


# ฟังก์ชันหลักของเกม
def main(pygame: pygame, 
         var: Variable, 
         screen: fw.Screen):
    
    var.set_start()
    player = character.Player(screen, 60, 80)
    map = fw.Map(var.bg_vsMons01, high_x(screen, var.bg_vsMons01), screen.height(screen.MAX_Y))
    var.all_sprites.add(player)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to exit
                    pygame.quit()
                    sys.exit()
            elif var.btnBack.click(event):
                running = False

        map.show(screen.window, screen.pack_x(0), screen.pack_y(0))
        
        player.update(var, events)
        player.magic_sprites.update()
        var.all_sprites.draw(screen.window)

        var.btnBack.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(10), screen.pack_y(10))

        pygame.display.flip()
        var.clock.tick(var.FPS)
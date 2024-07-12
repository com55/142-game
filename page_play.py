import sys
import pygame
import framework as fw
from variable import Variable
import page_play_card
import page_play_vsMons

def main(page_play_run: bool, 
         pygame: pygame, 
         var: Variable, 
         screen: fw.Screen) -> bool:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to exit
                pygame.quit()
                sys.exit()
        elif var.btnPlayCard.click(event):
            page_play_card.main(pygame, var, screen)
        elif var.btnPlayAns.click(event):
            pass
        elif var.btnPlayVsMons.click(event):
            page_play_vsMons.main(pygame, var, screen)
        elif var.btnBack.click(event):
            page_play_run = False

    screen.window.fill(var.colors.WHITE)
    var.btnPlayCard.show(screen.window, screen.width(190), screen.height(330), screen.pack_x(40), screen.pack_y(15))
    var.btnPlayAns.show(screen.window, screen.width(190), screen.height(330), screen.pack_x(240), screen.pack_y(15))
    var.btnPlayVsMons.show(screen.window, screen.width(190), screen.height(330), screen.pack_x(440), screen.pack_y(15))
    var.btnBack.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(10), screen.pack_y(10))

    pygame.display.flip()
    var.clock.tick(var.FPS)
    return page_play_run
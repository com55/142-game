import sys
import pygame
import framework as fw
from variable import Variable

def main(page_setting_run: bool, 
         pygame: pygame, 
         var: Variable, 
         screen: fw.Screen) -> bool:
    
    # ตัวแปร text ในหน้า setting
    text_screen_size = fw.Text('screen size : ', 30, var.colors.BLACK)
    text_audio_music = fw.Text('music : ', 30, var.colors.BLACK)
    text_audio_efx = fw.Text('effect : ', 30, var.colors.BLACK)
    text_audio_music_volume = fw.Text(f'{var.audio_volume_music} %', 30, var.colors.BLACK)
    text_audio_efx_volume = fw.Text(f'{var.audio_volume_efx} %', 30, var.colors.BLACK)

    # page_setting
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to exit
                pygame.quit()
                sys.exit()
        elif var.dropdownScreen.handle_event(event):
            selected_option = var.dropdownScreen.selected_option
            if selected_option == 'Full Screen':
                screen.set_fullscreen_mode()
            else:
                w, h = map(int, selected_option.split('x'))
                screen.set_screen(w, h)
        elif var.btnBack.click(event):
            page_setting_run = False
        elif var.btnReduce_1_music.click(event):
            var.volume_down_music(1)
        elif var.btnIncrease_1_music.click(event):
            var.volume_up_music(1)
        elif var.btnReduce_10_music.click(event):
            var.volume_down_music(10)
        elif var.btnIncrease_10_music.click(event):
            var.volume_up_music(10)
        elif var.btnReduce_1_efx.click(event):
            var.volume_down_efx(1)
        elif var.btnIncrease_1_efx.click(event):
            var.volume_up_efx(1)
        elif var.btnReduce_10_efx.click(event):
            var.volume_down_efx(10)
        elif var.btnIncrease_10_efx.click(event):
            var.volume_up_efx(10)
    
    # เคลียร์หน้าจอให้เป็นสีขาว
    screen.window.fill(var.colors.WHITE)
    # จัดวางปุ่มและตัวหนังสือ
    text_screen_size.show(screen.window, screen.pack_x(200), screen.pack_y(130))

    # audio_music
    text_audio_music.show(screen.window, screen.pack_x(200), screen.pack_y(160))
    var.btnReduce_1_music.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(270), screen.pack_y(160))
    var.btnReduce_10_music.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(300), screen.pack_y(160))
    text_audio_music_volume.show(screen.window, screen.pack_x(360), screen.pack_y(160) ,center_mode=True)
    var.btnIncrease_1_music.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(390), screen.pack_y(160))
    var.btnIncrease_10_music.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(420), screen.pack_y(160))
    
    # audio_efx
    text_audio_efx.show(screen.window, screen.pack_x(200), screen.pack_y(190))
    var.btnReduce_1_efx.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(270), screen.pack_y(190))
    var.btnReduce_10_efx.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(300), screen.pack_y(190))
    text_audio_efx_volume.show(screen.window, screen.pack_x(360), screen.pack_y(190) ,center_mode=True)
    var.btnIncrease_1_efx.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(390), screen.pack_y(190))
    var.btnIncrease_10_efx.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(420), screen.pack_y(190))
    
    var.dropdownScreen.show(screen.window, screen.width(100), screen.height(20), screen.pack_x(300), screen.pack_y(130))
    var.btnBack.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(10), screen.pack_y(10))

    pygame.display.flip()
    var.clock.tick(30)
    return page_setting_run
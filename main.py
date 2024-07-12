import sys
import pygame
import colors
import variable
import get_image
import get_audio
import page_play
import page_setting
import page_gacha
import framework as fw


# Initialize Pygame
pygame.init()
pygame.display.set_caption('142 game')
pygame.display.set_icon(pygame.image.load(get_image.icon))


# global variable
screen = fw.Screen(640, 360)
var = variable.Variable(pygame)
running = True

# # ตรวจสอบว่ารันอยู่บนไฟล์ EXE หรือไม่
# if getattr(sys, '_MEIPASS', None):
#     import datetime
#     # ตรวจสอบวันที่ปัจจุบัน
#     today = datetime.date.today()
#     expiry_date = datetime.date(2024, 7, 8)  # วันที่หมดอายุ (8 กรกฎาคม 2567)

#     if today >= expiry_date:
#         # ทำให้เกมเปิดไม่ได้
#         running = False
#     else:
#         print("ไฟล์ EXE ยังไม่หมดอายุ")
# else:
#     print("ไม่ได้รันอยู่บนไฟล์ EXE")

while running:
    # ตัวแปรสำหรับเข้าแต่ละหน้า
    page_play_run = False
    page_gacha_run = False
    page_setting_run = False
    # ตัวแปรอีเว้น
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to exit
                pygame.quit()
                sys.exit()
        elif var.btnPlay.click(event):
            page_play_run = True
            var.set_start()
        elif var.btnGacha.click(event):
            page_gacha_run = True
        elif var.btnSetting.click(event):
            page_setting_run = True
        elif var.btnExit.click(event):
            pygame.quit()
            sys.exit()
    
    screen.window.fill(var.colors.WHITE)
    var.show_gem(screen, 420)
    var.text_name_game.show(screen.window, screen.pack_x(10), screen.pack_y(10))
    var.text_version.show(screen.window, screen.pack_x(15), screen.pack_y(40), 'v.0.1.13')
    var.btnGacha.show(screen.window, screen.width(50), screen.height(50), screen.pack_x(580), screen.pack_y(240))
    var.btnPlay.show(screen.window, screen.width(50), screen.height(50), screen.pack_x(580), screen.pack_y(300))
    var.btnSetting.show(screen.window, screen.width(50), screen.height(50), screen.pack_x(520), screen.pack_y(10))
    var.btnExit.show(screen.window, screen.width(50), screen.height(50), screen.pack_x(580), screen.pack_y(10))
    pygame.display.flip()
    var.clock.tick(var.FPS)

    while page_play_run:
        page_play_run = page_play.main(page_play_run, pygame, var, screen)

    var.result2 = f'กดเพื่อสุ่มตู้ {var.banner_gacha_name} ได้เลย!!!'
    while page_gacha_run:
        page_gacha_run = page_gacha.main(page_gacha_run, pygame, var, screen)

    while page_setting_run:
        page_setting_run = page_setting.main(page_setting_run, pygame, var, screen)

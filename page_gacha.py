import sys
import pygame
import framework as fw
from variable import Variable
import randomGacha as gacha

def main(page_gacha_run: bool, 
         pygame: pygame, 
         var: Variable, 
         screen: fw.Screen) -> bool:
    # ดึงข้อมูลจาก db
    gacha_calculator = gacha.GachaCalculator(var.user_name)
    # ----
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
            page_gacha_run = False
        elif var.btn_1roll.click(event):
            result = gacha_calculator.multiple_pulls(var.banner_gacha_name, 1)
            item = result['Result']
            error = result['Error']
            if error is None:
                var.audio_gacha_efx.play()
                Name = item[0]['Name']
                TierName = item[0]['TierName']
                var.result1 = ''
                var.result2 = f'คุณสุ่มได้ {Name} ระดับ {TierName}'
                var.result3 = ''
                var.result4 = ''
                var.result5 = ''
        elif var.btn_10roll.click(event):
            var.result1 = ''
            var.result2 = ''
            var.result3 = ''
            var.result4 = ''
            var.result5 = ''
            result = gacha_calculator.multiple_pulls(var.banner_gacha_name, 10)
            item = result['Result']
            error = result['Error']
            result = ''
            if error is None:
                var.audio_gacha_efx.play()
                for i in range(len(item)):
                    Name = item[i]['Name']
                    TierName = item[i]['TierName']
                    if i < 2:
                        var.result1 += f'คุณสุ่มได้ {Name} ระดับ {TierName}, '
                    elif i < 4:
                        var.result2 += f'คุณสุ่มได้ {Name} ระดับ {TierName}, '
                    elif i < 6:
                        var.result3 += f'คุณสุ่มได้ {Name} ระดับ {TierName}, '
                    elif i < 8:
                        var.result4 += f'คุณสุ่มได้ {Name} ระดับ {TierName}, '
                    elif i < 9:
                        var.result5 += f'คุณสุ่มได้ {Name} ระดับ {TierName}, '
                    else:
                        var.result5 += f'คุณสุ่มได้ {Name} ระดับ {TierName}'

        click_scroll_gacha = var.scroll_gacha.handle_event(event)
        if click_scroll_gacha is not None:
            var.banner_gacha_name = click_scroll_gacha
            var.result1 = ''
            var.result2 = f'กดเพื่อสุ่มตู้ {var.banner_gacha_name} ได้เลย!!!'
            var.result3 = ''
            var.result4 = ''
            var.result5 = ''

    # กำหนดการแสดงผลปุ่ม 1 โรล
    if gacha_calculator.checkGem(1, return_gem=False):
        var.btn_1roll.change_color_button(var.colors.GREEN)
    else:
        var.btn_1roll.change_color_button(var.colors.RED)

    # กำหนดการแสดงผลปุ่ม 10 โรล
    if gacha_calculator.checkGem(10, return_gem=False):
        var.btn_10roll.change_color_button(var.colors.GREEN)
    else:
        var.btn_10roll.change_color_button(var.colors.RED)
    
    # text
    text_gacha_result1 = fw.Text(f'{var.result1}', 30, var.colors.BLACK)
    text_gacha_result2 = fw.Text(f'{var.result2}', 30, var.colors.BLACK)
    text_gacha_result3 = fw.Text(f'{var.result3}', 30, var.colors.BLACK)
    text_gacha_result4 = fw.Text(f'{var.result4}', 30, var.colors.BLACK)
    text_gacha_result5 = fw.Text(f'{var.result5}', 30, var.colors.BLACK)
    
    screen.window.fill(var.colors.WHITE)
    var.show_gem(screen)
    text_gacha_result1.show(screen.window, screen.pack_x(400), screen.pack_y(105) ,center_mode=True)
    text_gacha_result2.show(screen.window, screen.pack_x(400), screen.pack_y(135) ,center_mode=True)
    text_gacha_result3.show(screen.window, screen.pack_x(400), screen.pack_y(165) ,center_mode=True)
    text_gacha_result4.show(screen.window, screen.pack_x(400), screen.pack_y(195) ,center_mode=True)
    text_gacha_result5.show(screen.window, screen.pack_x(400), screen.pack_y(225) ,center_mode=True)
    var.btn_1roll.show(screen.window, screen.width(100), screen.height(20), screen.pack_x(400), screen.pack_y(300))
    var.btn_10roll.show(screen.window, screen.width(100), screen.height(20), screen.pack_x(510), screen.pack_y(300))
    
    var.scroll_gacha.show(screen.window, screen.width(160), screen.height(screen.MAX_Y), screen.pack_x(15), screen.pack_y(0), screen.height(20))

    var.btnBack.show(screen.window, screen.width(20), screen.height(20), screen.pack_x(10), screen.pack_y(10))

    pygame.display.flip()
    var.clock.tick(var.FPS)
    return page_gacha_run

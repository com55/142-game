import sys
import os
import ctypes
import pygame
from math import ceil


class Screen():
    def __init__(self, x: int, y: int):
        # กำหนดการแบ่งหน้าจอ
        self.MAX_X = x
        self.MAX_Y = y
        # ตั้งค่าให้เต็มจอเป็นค่าเริ่มต้น
        self.set_fullscreen_mode()

    def set_fullscreen_mode(self):
        # ตั้งค่าโหมดการแสดงผลเป็นเต็มหน้าจอ
        self.window = pygame.display.set_mode((0, 0))
        pygame.display.toggle_fullscreen()
        # ตรวจจับความละเอียดหน้าจอปัจจุบัน
        self.__get_screen_info()
        # แบ่งหน้าจออกเป็น grid
        self.__set_axis()

    def set_screen(self, width: int, height: int):
        # ตั้งค่าโหมดการแสดงผลเป็นค่าที่กำหนด
        self.window = pygame.display.set_mode((width, height))
        # ตรวจจับความละเอียดหน้าจอปัจจุบัน
        self.__get_screen_info()
        # แบ่งหน้าจออกเป็น grid
        self.__set_axis()
        self.set2center_window()

    def set2center_window(self):
        # ดึงข้อมูลของจอภาพ
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        # คำนวณตำแหน่งของหน้าต่างเพื่อให้อยู่ตรงกลาง
        x = (screen_width - self.SCREEN_WIDTH) // 2
        y = (screen_height - self.SCREEN_HEIGHT) // 2

        # ตั้งค่าตำแหน่งของหน้าต่าง
        hwnd = pygame.display.get_wm_info()['window']
        user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)

    def true_position_x(self, scale: int):
        # อนุญาตให้ตำแหน่งติดลบหรือเกินตำแหน่งสูงสุดได้
        return ceil(self.x_axis * scale)

    def true_position_y(self, scale: int):
        # อนุญาตให้ตำแหน่งติดลบหรือเกินตำแหน่งสูงสุดได้
        return ceil(self.y_axis * scale)

    def pack_x(self, box_x: int) -> int:
        return self.__resize2x(box_x)
    
    def pack_y(self, box_y: int) -> int:
        return self.__resize2y(box_y)
    
    def width(self, scale: int) -> int:
        return self.__resize2x(scale)
    
    def height(self, scale: int) -> int:
        return self.__resize2y(scale)
    
    def __resize2x(self, scale: int):
        scale = min(self.MAX_X, scale)
        scale = max(scale, 0)
        return ceil(self.x_axis * scale)
    
    def __resize2y(self, scale: int):
        scale = min(self.MAX_Y, scale)
        scale = max(scale, 0)
        return ceil(self.y_axis * scale)

    def __set_axis(self):
        self.x_axis = self.SCREEN_WIDTH / self.MAX_X
        self.y_axis = self.SCREEN_HEIGHT / self.MAX_Y

    def __get_screen_info(self):
        screen_info = pygame.display.Info()
        self.SCREEN_WIDTH = screen_info.current_w
        self.SCREEN_HEIGHT = screen_info.current_h


class Map(pygame.sprite.Sprite):
    def __init__(self, texture: pygame.Surface, width: int, height: int):
        super().__init__()
        self.image = texture
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def show(self, 
             screen_draw: pygame.Surface, 
             x: int, y: int,
             width: int = None, 
             height: int = None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        self.set_position(x, y)
        
        screen_draw.blit(self.image, self.rect)

    def set_position(self, x: int, y: int):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        return self
    

class TimeGame:
    def __init__(self):
        self.__time_start = self.get_current_time()
        self.__old_time = 0
        self.__now_time = 0
        # การนับเวลา
        self.__minutes = 0
        self.__seconds = 0
        # ถ้าต้องการให้หยุดจับเวลาให้ใส่เป็น True
        self.is_stop = False
        # การตรวจสอบเวลาเมื่อหยุดนับเวลา
        self.__old_stop = 0
        self.__now_stop = 0
        self.__timeStop_milli = 0
        #  1 วินาที = 1000 มิลลิวินาที
        self.__ONE_SECOND = 1000

    @property # แปลงเมธอดให้เป็นแอตทริบิวต์
    def minutes(self) -> int:
        # ป้องกันการถูกแทนค่าจากภายนอก
        # แต่ให้สามารถส่งออกข้อมูลไปนอก class ได้
        return self.__minutes

    @property # แปลงเมธอดให้เป็นแอตทริบิวต์
    def seconds(self) -> int:
        # ป้องกันการถูกแทนค่าจากภายนอก
        # แต่ให้สามารถส่งออกข้อมูลไปนอก class ได้
        return self.__seconds

    def reset_time(self):
        # เปลี่ยนทุกค่าเป็นค่าเริ่มต้น
        self.__time_start = self.get_current_time()
        self.__old_time = 0
        self.__now_time = 0
        self.__minutes = 0
        self.__seconds = 0
        self.is_stop = False
        self.__old_stop = 0
        self.__now_stop = 0
        self.__timeStop_milli = 0

    def update_time(self):
        if self.__timestop():
            return
        
        sum_second = int((self.get_current_time() - self.__time_start) / self.__ONE_SECOND)
        self.__now_time = sum_second

        if self.__old_time != self.__now_time:
            self.__seconds += 1
            if self.__seconds >= 60:
                self.__minutes += 1
                self.__seconds = 0
            self.__old_time = self.__now_time

    def check_elapsed_time(self, time_check: int, is_Second = True) -> bool:
        # ตรวจสอบว่าเวลาผ่านไปเท่ากับจำนวน วินาที หรือ มิลลิวินาที ที่ระบุหรือไม่

        if time_check < 0:
            # เวลาสำหรับตรวจสอบไม่ควรน้อยกว่า 0
            raise ValueError("Time check value must be non-negative")
        
        if self.__timestop():
            # หากเวลาหยุดอยู่ไม่ควรทำงาน
            return
        
        if is_Second:
            diff = int((self.get_current_time() - self.__time_start) / self.__ONE_SECOND)
            stop = self.__timeStop_milli / self.__ONE_SECOND
        else:
            diff = int(self.get_current_time() - self.__time_start)
            stop = self.__timeStop_milli

        if (diff - stop) >= time_check:
            return True
        else:
            return False

    def get_elapsed_time(self, is_Second = True) -> int:
        # ส่งค่าเวลาตั้งแต่เริ่มสร้าง object จนถึงปัจจุบัน
        if self.__timestop():
            return
        if is_Second:
            diff = int((self.get_current_time() - self.__time_start) / self.__ONE_SECOND)
            self.__now_time = diff
            return self.__now_time - self.__old_time
        else:
            diff = int((self.get_current_time() - self.__time_start))
            return diff - (self.__old_time * self.__ONE_SECOND)
        
    def get_current_time(self):
        # ใช้ดึงเวลาในปัจจุบัน
        return pygame.time.get_ticks()

    def __timestop(self):
        if not self.is_stop:
            return self.is_stop
        self.__now_stop = int((self.get_current_time() - self.__time_start) / self.__ONE_SECOND)
        if self.__old_stop != self.__now_stop:
            self.__timeStop_milli += self.__ONE_SECOND
            self.__old_stop = self.__now_stop

        return self.is_stop


class FontSystem():
    def __init__(self,
                 font_path: str,
                 font_size: int,
                 font_color: tuple):
        if font_path is None:
            self.font_path = self.__get_font()
        else:
            self.font_path = font_path
        # สมมติว่าเราออกแบบ UI สำหรับความสูง 720 pixels
        self.standard_window_size = 720
        self.base_font_size = font_size  # เก็บขนาด font เริ่มต้น
        self.font_size = font_size
        self.font_color = font_color
        self.create_font()
    
    def create_font(self):
        # สร้าง font
        self.font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)
    
    def set_font_size(self, window: pygame.Surface):
        # ดึงค่าความสูงของหน้าจอออกมา
        window_height = window.get_height()
        
        # คำนวณขนาด font ใหม่ตามสัดส่วนของความสูงหน้าจอ
        scale_factor = window_height / self.standard_window_size
        new_font_size = int(self.base_font_size * scale_factor)
        
        # ถ้าขนาด font เปลี่ยน ให้สร้าง font ใหม่
        if new_font_size != self.font_size:
            self.font_size = new_font_size
            self.create_font()
    
    def __get_font(self):
        # ตรวจสอบว่าอยู่ใน onefile mode หรือไม่
        if getattr(sys, '_MEIPASS', None):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        # สร้าง path ไปยังไฟล์ font
        return os.path.join(base_path, "Assets", "font", "Mali-Regular.ttf")


class Button(FontSystem):
    def __init__(self, 
                 text: str, 
                 font_size: int, 
                 font_color: tuple, 
                 color_button: tuple, 
                 radius=20, 
                 name_button=None, 
                 font_path=None):
        super().__init__(font_path, font_size, font_color)
        self.text = text
        if name_button is None:
            self.name_button = self.text
        else:
            self.name_button = name_button
        self.text_surface = self.font.render(text, True, font_color)
        self.set_button()
        self.color_button = color_button
        self.radius = radius
        # สถานะทั้งหมดได้แก่ "normal", "hover", "pressed"
        self.state = "normal"  

    def show(self, 
             screen_draw: pygame.Surface, 
             width_button: int, 
             height_button: int, 
             x: int, y: int):
        self.set_font_size(screen_draw)
        self.set_button(width_button, height_button, x, y)
        button_color = self.color_button
        text_color = self.font_color
        
        # เมื่อเมาส์ลอยอยู่เหนือปุ่ม
        if self.state == "hover":
            button_color = [min(255, c + 120) for c in self.color_button] # ทำให้ปุ่มสว่างขึ้น
            text_color = [min(255, c + 20) for c in self.font_color]
        
        pygame.draw.rect(screen_draw, button_color, self.button, 0, self.radius)

        # render text surface ใหม่
        text_surface = self.font.render(self.text, True, text_color)
        
        # คำนวณตำแหน่งกึ่งกลางของปุ่มใหม่ทุกครั้ง
        text_rect = text_surface.get_rect(center=self.button.center)
        
        screen_draw.blit(text_surface, text_rect)

    def change_color_button(self, color_button: tuple):
        self.color_button = color_button

    def set_button(self, 
                   width_button=1,
                   height_button=1,
                   x=1, y=1):
        self.button = pygame.Rect(x, y, width_button, height_button)
    
    def click(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            if self.button.collidepoint(event.pos):
                self.state = "hover"
            else:
                self.state = "normal"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.collidepoint(event.pos) and event.button == 1:  # ตรวจสอบว่าเป็นปุ่มซ้าย
                self.state = "pressed"
                return True  # ส่งคืนค่าว่ากดปุ่มซ้ายแล้ว
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.state == "pressed":
                self.state = "normal"
        return False


class ImageButton(Button):
    def __init__(self, 
                 text: str, 
                 font_size: int, 
                 font_color: tuple, 
                 image_path: str, 
                 name_button=None,
                 font_path=None):
        super().__init__(text, font_size, font_color, (0, 0, 0), 0, name_button, font_path)  # ส่งค่าที่ไม่ใช้ไปยัง super
        self.image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.image.copy()  # เก็บสำเนาภาพเดิมเพื่อการทำให้สว่างขึ้น
        self.image_rect = self.image.get_rect()

    def lighten_image(self, image, amount=50):
        """เพิ่มความสว่างให้กับรูปภาพ"""
        lighten = pygame.Surface(image.get_size()).convert_alpha()
        lighten.fill((amount, amount, amount, 0))
        lightened_image = image.copy()
        lightened_image.blit(lighten, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return lightened_image

    def show(self, 
             screen_draw: pygame.Surface, 
             width_button: int, 
             height_button: int, 
             x: int, y: int):
        self.set_font_size(screen_draw)
        self.set_button(width_button, height_button, x, y)
        self.image = pygame.transform.scale(self.original_image, (width_button, height_button))
        text_color = self.font_color
        image = self.image
        
        # เมื่อเมาส์ลอยอยู่เหนือปุ่ม
        if self.state == "hover":
            image = self.lighten_image(self.image)  # ทำให้ปุ่มสว่างขึ้น

        # วาดรูปภาพลงบนปุ่ม
        self.image_rect = image.get_rect(topleft=(x, y))
        screen_draw.blit(image, self.image_rect)

        # วาดข้อความบนปุ่ม
        screen_draw.blit(self.font.render(self.text, True, text_color), self.text_rect)

    def set_button(self, 
                   width_button=1,
                   height_button=1,
                   x=1, y=1):
        self.image_rect = pygame.Rect(x, y, width_button, height_button)
        self.text_rect = self.text_surface.get_rect(center=self.image_rect.center)
        self.button = self.image_rect


class Text(FontSystem):
    def __init__(self, 
                 text_default: str, 
                 font_size: int, 
                 font_color: tuple, 
                 font_path=None):
        super().__init__(font_path, font_size, font_color)
        # สร้างออบเจกต์ Text สำหรับแสดงข้อความบนหน้าจอ
        self.text = text_default
        # ตรวจสอบความสูงของออบเจกต์
        self.height = self.font.get_height()

    def show(self, 
             screen_draw: pygame.Surface, 
             x: int, y: int,
             text=None,
             center_mode=False):
        self.set_font_size(screen_draw)
        if text is not None:
            self.text = text
        text_surface = self.font.render(self.text, True, self.font_color)
        if center_mode:
            text_rect = text_surface.get_rect()  # สร้าง text_rect ก่อน
            text_rect.centerx = x  # กำหนดตำแหน่งกึ่งกลางในแนวแกน x
            text_rect.top = y     # กำหนดตำแหน่ง y ตามที่ต้องการ
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        screen_draw.blit(text_surface, text_rect)


class ImageText(Text):
    def __init__(self, 
                 text_default: str, 
                 font_size: int, 
                 font_color: tuple, 
                 image_path: str, 
                 font_path=None):
        super().__init__(text_default, font_size, font_color, font_path)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.image.copy()  # เก็บสำเนาภาพเดิมเพื่อการทำให้สว่างขึ้น
        self.image_rect = self.image.get_rect()

    def show(self, 
             screen_draw: pygame.Surface, 
             x: int, y: int,
             width: int, height: int,
             text=None, 
             center_mode=False):
        self.set_font_size(screen_draw)
        if text is not None:
            self.text = text

        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect()

        # กำหนดตำแหน่งของรูปภาพ
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y

        # กำหนดตำแหน่งของข้อความที่อยู่ใต้รูปภาพ
        if center_mode:
            text_rect.centerx = self.image_rect.centerx
            text_rect.centery = self.image_rect.centery
        else:
            text_rect.x = x
            text_rect.centery = self.image_rect.centery

        # วาดรูปภาพและข้อความลงบนหน้าจอ
        screen_draw.blit(self.image, self.image_rect)
        screen_draw.blit(text_surface, text_rect)


class Dropdown(FontSystem):
    def __init__(self, 
                 options: list, 
                 font_size: int,
                 font_color: tuple, 
                 color_dropdown: tuple, 
                 font_path=None):
        super().__init__(font_path, font_size, font_color)
        self.__options = options
        self.__color_dropdown = color_dropdown
        self.__active = False
        self.selected_option = options[0]
        # สถานะทั้งหมดได้แก่ "normal", "hover"
        self.__hover_option = "normal."

    def show(self,
             screen_draw: pygame.Surface, 
             width: int, 
             height: int, 
             x: int, y: int):
        self.set_font_size(screen_draw)
        self.rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen_draw, self.__color_dropdown, self.rect)
        text_surface = self.font.render(self.selected_option if self.selected_option else self.__options[0], True, self.font_color)
        text_rect = text_surface.get_rect(center=(x+(width/2)-10, y+(height/2)))
        screen_draw.blit(text_surface, text_rect)

        # วาดลูกศรชี้ลง (หรือชี้ขึ้นถ้า Dropdown เปิดอยู่)
        arrow_direction = 1 if self.__active else -1
        arrow_points = [
            (self.rect.right - 20, self.rect.centery - 5 * arrow_direction),
            (self.rect.right - 10, self.rect.centery + 5 * arrow_direction),
            (self.rect.right - 30, self.rect.centery + 5 * arrow_direction)
        ]
        pygame.draw.polygon(screen_draw, self.font_color, arrow_points)

        if self.__active:
            for i, option in enumerate(self.__options):
                rect = pygame.Rect(self.rect.x, self.rect.y + (i+1) * self.rect.height, self.rect.width, self.rect.height)
                if self.__hover_option == i:
                    color_dropdown = [min(255, c + 20) for c in self.__color_dropdown] # ทำให้สว่างขึ้น
                else:
                    color_dropdown = [max(0, c - 55) for c in self.__color_dropdown] # ทำให้มืดลง
                pygame.draw.rect(screen_draw, color_dropdown, rect)
                text_surface = self.font.render(option, True, self.font_color)
                text_rect = text_surface.get_rect(center=(rect.x+(width/2), rect.y+(height/2)))
                screen_draw.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION and self.__active:
            for i, option in enumerate(self.__options):
                rect = pygame.Rect(self.rect.x, self.rect.y + (i+1) * self.rect.height, self.rect.width, self.rect.height)
                if rect.collidepoint(event.pos):
                    self.__hover_option = i
                    break
                else:
                    self.__hover_option = -1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and event.button == 1:  # ตรวจสอบว่าเป็นปุ่มซ้าย
                self.__active = not self.__active
            elif self.__active:
                for i, option in enumerate(self.__options):
                    rect = pygame.Rect(self.rect.x, self.rect.y + (i+1) * self.rect.height, self.rect.width, self.rect.height)
                    if rect.collidepoint(event.pos) and event.button == 1:  # ตรวจสอบว่าเป็นปุ่มซ้าย
                        self.selected_option = option
                        self.__active = False
                        # ส่งคืนค่า True เมื่อมีการเลือกตัวเลือก
                        return True
                    else:
                        self.__active = False
        # ส่งคืนค่า False เมื่อไม่มีการเลือกตัวเลือกใด ๆ
        return False
    

class ScrollableMenu:
    def __init__(self, 
                 options: list, 
                 fade_away=False, 
                 cut_frame=False, 
                 line_division=5):
        self.options = options
        self.obj_height = 0
        self.rect = None
        # เก็บค่า True เมื่อเมาส์ถูกกด
        self.mouse_key_down = False
        # ตัวแปรในการเลื่อน
        self.scroll_y = 0
        self.speed_scroll = 10
        # ใช้เก็บระยะห่างของแต่ละวัตถุ
        self.line_spacing = 0
        # ใช้สำหรับแบ่งอัตราส่วนในแต่ละแถว
        self.line_division = line_division + 1
        # ใช้เก็บตัวเลือกที่กำลังแสดงบนหน้าจอ
        self.visible_options = []
        # กำหนดเป็น True หากต้องการให้ object ค่อย ๆ จางหายไป
        self.fade_away = fade_away
        # กำหนดให้ตัด object เมื่อ object เลยกรอบที่กำหนด
        self.cut_frame = cut_frame

    def show(self, 
             screen_draw: pygame.Surface, 
             width: int, height: int, 
             x: int, y: int, 
             line_spacing: int, 
             show_area=False):
        # กำหนด rect ของ ScrollableMenu
        self.rect = pygame.Rect(x, y, width, height)
        # กำหนดระยะห่างวัตถุ
        self.line_spacing = line_spacing
        if show_area:
            pygame.draw.rect(screen_draw, (255, 255, 255), self.rect, 2)

        if self.cut_frame:
            # เก็บค่า clip rectangle ดั้งเดิมไว้
            original_clip = screen_draw.get_clip()
            screen_draw.set_clip(self.rect)
        
        self.visible_options.clear()

        for i, option in enumerate(self.options):
            if not hasattr(option, 'height'):
                # แบ่งอัตราส่วนในแต่ละแถว
                self.obj_height = height // self.line_division
            else:
                self.obj_height = option.height

            option_y = self.rect.y + (i+1) * (self.obj_height + self.line_spacing) - self.scroll_y

            # คำนวณขอบเขตของ option ที่จะแสดงผล
            if option_y + self.obj_height > self.rect.y and option_y < self.rect.y + self.rect.height:
                
                # สร้าง surface ชั่วคราวที่โปร่งใส
                temp_surface = pygame.Surface((width, self.obj_height), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 0, 0))  # ทำให้พื้นหลังโปร่งใส
                
                self._show_option(temp_surface, option, self.rect.x, option_y, width, self.obj_height)
                
                # วาด temp_surface ลงบน screen_draw โดยใช้ clip rect ของเมนู
                if self.fade_away:
                    self._blit_with_fade(screen_draw, temp_surface, self.rect.x, option_y)
                else:
                    screen_draw.blit(temp_surface, (self.rect.x, option_y))

        # กำหนดความเร็วในการเลื่อนตามความสูงเศษ 1 ส่วน 4 ของ object 
        self.speed_scroll = max(self.speed_scroll, (self.obj_height // 4))

        if self.cut_frame:
            # คืนค่า clip rectangle เดิม
            screen_draw.set_clip(original_clip)

    def _show_option(self, surface, option, option_x, option_y, width, height):
        x = 0
        y = 0
        if isinstance(option, (Button, ImageButton)):
            # แก้ไขขนาดหน้าต่างมาตรฐานให้พอดีกลับขนาดของปุ่ม
            option.standard_window_size = height * 2
            # แสดงผลปุ่มตาม surface ปัจจุบัน
            # rect ของ ปุ่มจะถูกเปลี่ยนไปตาม surface ไม่ใช่ตำแหน่งจริง ๆ ของหน้าจอ
            option.show(surface, width, height, x, y)
            # กำหนดตำแหน่งจริง ๆ บนหน้าจอของ option
            option_rect = pygame.Rect(option_x, option_y, width, self.obj_height)  # กำหนดตำแหน่ง rect
            # บันทึกตัวเลือกที่แสดง ณ ขณะนั้น เพื่อจดจำตำแหน่งจริง ๆ ของปุ่ม
            self.visible_options.append((option, option_rect))
        elif isinstance(option, Text):
            # แก้ไขขนาดหน้าต่างมาตรฐานให้พอดีกลับขนาดของตัวหนังสือ
            option.standard_window_size = height * 2
            option.show(surface, (width // 2), y, center_mode=True)
        else:
            pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height))

    def _blit_with_fade(self, screen_draw, temp_surface, x, y):
        fade_height = self.rect.height // 6  # ความสูงของบริเวณที่เฟด
        for i in range(temp_surface.get_height()):
            alpha = 255
            if y + i < self.rect.y + fade_height:
                alpha = max(0, 255 - int(255 * (self.rect.y + fade_height - (y + i)) / fade_height))
            elif y + i > self.rect.y + self.rect.height - fade_height:
                alpha = max(0, 255 - int(255 * ((y + i) - (self.rect.y + self.rect.height - fade_height)) / fade_height))
            line_surface = temp_surface.subsurface(pygame.Rect(0, i, temp_surface.get_width(), 1))
            line_surface.set_alpha(alpha)
            screen_draw.blit(line_surface, (x, y + i))

    def handle_event(self, event: pygame.event.Event):
        if self.rect is None:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.mouse_key_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_key_down = False
        elif event.type == pygame.MOUSEMOTION and self.mouse_key_down:
            self.scroll_y -= event.rel[1]  # เลื่อนตามการเคลื่อนที่ของเมาส์ในแกน Y
            self.scroll_y = self._get_max_scroll()
        
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.scroll_y -= event.y * self.speed_scroll  # ปรับความเร็วการเลื่อนได้ตามต้องการ
                self.scroll_y = self._get_max_scroll()

        for option, option_rect in self.visible_options:
            # ใช้งานได้กับ option ประเภทปุ่มเท่านั้นถึงจะมีเมธอด click
            if hasattr(option, 'click'):
                # เปลี่ยน rect ของ ปุ่มให้เป็น ตำแหน่งจริงบนหน้าจอ
                option.button = option_rect
                if option.click(event):
                    # ส่งคือชื่อปุ่มที่กำลังถูกคลิ๊ก
                    return option.name_button
                
        return None

    def _get_max_scroll(self):
        option_height = (self.obj_height + self.line_spacing)
        # จำนวนทั้งของ option บวก 2 เพื่อไม่ให้ส่วนหัวและท้ายติดกับขอบจนเกินไป
        quantity_option = (len(self.options) + 2)
        max_scroll = (quantity_option * option_height) - self.rect.height
        return max(0, min(self.scroll_y, max_scroll))

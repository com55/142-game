import pygame
import colors
import get_image
import get_audio
import framework as fw

class Variable():
    def __init__(self, pygame: pygame):
        self.clock = pygame.time.Clock()
        # ตัวแปร
        self.result = 'Random Now!!'
        self.count_gacha = 0
        # Colors
        self.colors = colors.Colors()
        # ตัวแปรของเพลง
        self.audio_volume = 10
        self.audio_background_music = pygame.mixer.Sound(get_audio.debirun_sound)
        self.audio_gacha = pygame.mixer.Sound(get_audio.gacha_sound)
        self.set_audio_volume()
        self.audio_background_music.play(-1)
        # ตัวแปรข้อความ
        self.text_name_game = fw.Text('142 Game', 50, self.colors.BLACK)
        self.text_normal = fw.Text('', 30, self.colors.BLACK)
        # ตัวแปรของปุ่ม
        self.btnPlay = fw.Button('play', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnGacha = fw.Button('gacha', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnSetting = fw.Button('setting', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnExit = fw.Button('exit', 20, self.colors.WHITE, self.colors.RED)
        self.btnPrevious = fw.Button('<', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnNext = fw.Button('>', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnReduce_1 = fw.Button('-1', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnIncrease_1 = fw.Button('+1', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnReduce_10 = fw.Button('-10', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnIncrease_10 = fw.Button('+10', 20, self.colors.WHITE, self.colors.DARK_BLUE)
        self.btnRandom = fw.Button('random', 20, self.colors.WHITE, self.colors.GOLD)
        # ตัวแปรของ dropdown
        self.dropdownScreen = fw.Dropdown(['Full Screen', '1920x1080', '1280x720', '854x480'], 24, self.colors.WHITE, self.colors.DARK_BLUE)
        # set ค่าเริ่มต้น
        self.set_start()

    def set_start(self):
        pass

    def set_audio_volume(self):
        audio_volume = self.audio_volume / 100
        self.audio_background_music.set_volume(audio_volume)
        self.audio_gacha.set_volume(audio_volume)

    def volume_up(self, key):
        self.audio_volume += key
        if self.audio_volume > 100:
            self.audio_volume = 100
        self.set_audio_volume()

    def volume_down(self, key):
        self.audio_volume -= key
        if self.audio_volume < 0:
            self.audio_volume = 0
        self.set_audio_volume()
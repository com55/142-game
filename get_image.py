import sys
import os

# ตรวจสอบว่าอยู่ใน onefile mode หรือไม่
if getattr(sys, '_MEIPASS', None):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# สร้าง path ไปยังไฟล์รูป
# icon game
icon = os.path.join(base_path, "Assets", "icon.png")
# ปุ่มต่าง ๆ
btnPlay = os.path.join(base_path, "Assets", "picture", "button", "btnPlay.png")
btnGacha = os.path.join(base_path, "Assets", "picture", "button", "btnGacha.png")
btnSetting = os.path.join(base_path, "Assets", "picture", "button", "btnSetting.png")
btnExit = os.path.join(base_path, "Assets", "picture", "button", "btnExit.png")
btnBack = os.path.join(base_path, "Assets", "picture", "button", "btnBack.png")
btnPlayCard = os.path.join(base_path, "Assets", "picture", "button", "btnPlayCard.png")
btnPlayAns = os.path.join(base_path, "Assets", "picture", "button", "btnPlayAns.png")
btnPlayVsMons = os.path.join(base_path, "Assets", "picture", "button", "btnPlayVsMons.png")
# gacha banner
banner_AMI = os.path.join(base_path, "Assets", "picture", "gacha",  "banner", "banner_AMI.png")
banner_Ashyra = os.path.join(base_path, "Assets", "picture", "gacha",  "banner", "banner_Ashyra.png")
banner_Debirun = os.path.join(base_path, "Assets", "picture", "gacha",  "banner", "banner_Debirun.png")
banner_MildR = os.path.join(base_path, "Assets", "picture", "gacha",  "banner", "banner_Mild-R.png")
banner_Tsururu = os.path.join(base_path, "Assets", "picture", "gacha",  "banner", "banner_Tsururu.png")
banner_Xonebu = os.path.join(base_path, "Assets", "picture", "gacha",  "banner", "banner_Xonebu.png")
# Assets Background
bg_gem = os.path.join(base_path, "Assets", "picture", "background",  "gem.png")
bg_text_area = os.path.join(base_path, "Assets", "picture", "background",  "text_area.png")
bg_vsMons01 = os.path.join(base_path, "Assets", "picture", "background",  "bg_vsMons01.png")
# card
back_card = os.path.join(base_path, "Assets", "picture", "character",  "card", "back_card.png")
c_ami = os.path.join(base_path, "Assets", "picture", "character",  "card", "c_ami.png")
c_ashy = os.path.join(base_path, "Assets", "picture", "character",  "card", "c_ashy.png")
c_bu = os.path.join(base_path, "Assets", "picture", "character",  "card", "c_bu.png")
c_del = os.path.join(base_path, "Assets", "picture", "character",  "card", "c_del.png")
c_mild = os.path.join(base_path, "Assets", "picture", "character",  "card", "c_mild.png")
c_suru = os.path.join(base_path, "Assets", "picture", "character",  "card", "c_suru.png")
# chibi
def chibi_debirun_normal(action, key_frame):
    return os.path.join(base_path, "Assets", "picture", "character",  "chibi", "debirun", "skins_normal", f"{action}", f"{key_frame}.png")
import tkinter as tk
import pyautogui

data = []

class CardBotAppPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Card")

        # สร้างปุ่มสำหรับ screenshot
        self.btn_screenshot = tk.Button(self.root, text="Screenshot", command=self.screenshot)
        self.btn_screenshot.pack(pady=10)

        # สร้างปุ่มสำหรับ play
        self.btn_play = tk.Button(self.root, text="Play", command=self.play)
        self.btn_play.pack(pady=10)

    def screenshot(self):
        global data  # เรียกใช้ตัวแปร global ที่ประกาศไว้นอกคลาส
        global pos   # เรียกใช้ตัวแปร global ที่ประกาศไว้นอกคลาส
        pos = []
        data = []

        sc = pyautogui.screenshot()

        # ค้นหาภาพและเก็บตำแหน่งที่พบลงใน data
        for img_file in ["./Assets/picture/character/card/_del.png", 
                         "./Assets/picture/character/card/_ami.png", 
                         "./Assets/picture/character/card/_ashy.png", 
                         "./Assets/picture/character/card/_bu.png", 
                         "./Assets/picture/character/card/_mild.png", 
                         "./Assets/picture/character/card/_tsuru.png"]:
            for position in pyautogui.locateAll(img_file, sc, confidence=0.95):
                pos.append(position)
                if len(pos) >= 2:
                    break
            for p in pos:
                data.append(p)
            pos = []

        # พิมพ์ตำแหน่งทั้งหมดที่พบ
        for i in data:
            print(i)

    def play(self):
        global data  # เรียกใช้ตัวแปร global ที่ประกาศไว้นอกคลาส

        # คลิกที่ทุกตำแหน่งที่พบ
        for position in data:
            pyautogui.click(position)
            # time.sleep(0.0001)  # ถ้าต้องการ delay ระหว่างการคลิก

if __name__ == "__main__":
    root = tk.Tk()
    app = CardBotAppPlayer(root)
    root.geometry("200x100")
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from pynput import mouse
import os

class mainwindow(tk.Tk):     
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
    #模式二按键位置数据
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.width, self.height = 0, 0
    #窗口设置
        self.geometry('400x170')    
        self.resizable(False, False)
        self.wm_attributes('-topmost', True) 

        self.monitor = self.create_listener(0)  #创建鼠标监视器，默认为模式一的监视器
        self.monitor.start()
        
    #组件设置
        self.tab = ttk.Notebook(self)
        self.tab.place(x = 10, y = 3, width = 380, height = 160)

        self.page1 = ttk.Frame(self.tab)
        self.page2 = ttk.Frame(self.tab)

        self.tab.add(self.page1, text = '模式1')
        self.tab.add(self.page2, text = '模式2')
        self.tab.bind('<<NotebookTabChanged>>', lambda even: self.mode_change(even))
        #模式1标签页设置
        self.label_point = ttk.Label(self.page1, text = 'X, Y坐标')
        self.label_point.place(x = 1, y = 5)

        self.text_point = tk.Text(self.page1)
        self.text_point.config(state = tk.DISABLED, font = 16)
        self.text_point.place(x = 80, y = 5, width = 150, height = 24)

        self.instruct_point = ttk.Label(self.page1, text = '提示：按下鼠标中键以获得光标位置')
        self.instruct_point.place(x = 1, y = 40)
        #模式2标签页设置
        self.label_range_start = ttk.Label(self.page2, text = 'X, Y起始坐标')
        self.label_range_start.place(x = 1, y = 5)
        self.label_range_end = ttk.Label(self.page2, text = 'X, Y终点坐标')
        self.label_range_end.place(x = 1, y = 40)
        self.label_range_size = ttk.Label(self.page2, text = 'W, H宽高信息')
        self.label_range_size.place(x = 1, y = 75)

        self.text_range_start = tk.Text(self.page2)
        self.text_range_start.config(state = tk.DISABLED, font = 16)
        self.text_range_start.place(x = 80, y = 5, width = 150, height = 24)
        
        self.text_range_end = tk.Text(self.page2)
        self.text_range_end.config(state = tk.DISABLED, font = 16)
        self.text_range_end.place(x = 80, y = 40, width = 150, height = 24)

        self.text_range_size = tk.Text(self.page2)
        self.text_range_size.config(state = tk.DISABLED, font = 16)
        self.text_range_size.place(x = 80, y = 75, width = 150, height = 24)

        self.instruct_range = ttk.Label(self.page2, text = '提示：长按鼠标中键选定范围')
        self.instruct_range.place(x = 1, y = 110)
    #窗口界面配置结束

    #功能接口设置
    def set_mode1_text(self, x, y):
        buffer = str(x) + ', ' + str(y)
        self.text_point.config(state = tk.NORMAL)
        self.text_point.delete('1.0', tk.END)
        self.text_point.insert('1.0', buffer)
        self.text_point.config(state = tk.DISABLED)

    def set_mode2_text(self, state, x, y):
        buffer = str(x) + ', ' + str(y)
        if state == 0:
            self.text_range_start.config(state = tk.NORMAL)
            self.text_range_start.delete('1.0', tk.END)
            self.text_range_start.insert('1.0', buffer)
            self.text_range_start.config(state = tk.DISABLED)
        elif state == 1:
            self.text_range_end.config(state = tk.NORMAL)
            self.text_range_end.delete('1.0', tk.END)
            self.text_range_end.insert('1.0', buffer)
            self.text_range_end.config(state = tk.DISABLED)
        else:
            self.text_range_size.config(state = tk.NORMAL)
            self.text_range_size.delete('1.0', tk.END)
            self.text_range_size.insert('1.0', buffer)
            self.text_range_size.config(state = tk.DISABLED)

    def mode_change(self, event:tk.Event):
        cur_tab = self.tab.select()
        index = self.tab.index(cur_tab)
        self.del_listener(self.monitor)
        if index == 0:
            self.monitor = self.create_listener(0)
            self.monitor.start()
        else:
            self.monitor = self.create_listener(1)
            self.monitor.start()

    def create_listener(self, mode):
        return mouse.Listener(on_click = self.call_back(mode))

    def del_listener(self, listener:mouse.Listener):
        listener.stop()

    def call_back(self, mode):
        if mode == 0:
            def click_point(x, y, button, press):
                if button == mouse.Button.middle and press == True:
                    self.set_mode1_text(x, y)
            return click_point
        elif mode == 1:
            def click_range(x, y, button, press):
                if button == mouse.Button.middle and press == True:     #按键按下
                    self.x1, self.y1 = x, y
                    self.set_mode2_text(0, x, y)
                elif button == mouse.Button.middle and press == False:  #按键释放
                    self.x2, self.y2 = x, y
                    self.width, self.height = abs(self.x1 - self.x2), abs(self.y1 - self.y2)
                    self.set_mode2_text(1, x, y)
                    self.set_mode2_text(2, self.width, self.height)
            return click_range
        
    def set_ico(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(dir, 'img\\knockout-1764646961080_256x256.ico')
        self.iconbitmap(img_dir)
    #功能接口设置结束

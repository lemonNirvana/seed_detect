# -*- coding: utf-8 -*-
# @Time    : 2018/5/15 9:32
# @Author  : lemon
# @Project : Seedling_detect
# @File    : wxGui
# @Software: PyCharm

import wx
import cv2
import numpy as np

cover = "pencilsketch_bg.jpg"

class BaseLayout(wx.Frame):
    def __init__(self, parent, id, title, fps = 0.5):
        self.fps = fps
        self.image_cover = wx.Image(cover, wx.BITMAP_TYPE_ANY).Scale(320, 240)
        super().__init__(parent, id, title, size=(1020, 480))
        self.InitUI()
        self.Center()
        self.Show()
    def InitUI(self):
        self.pnl = wx.Panel(self)
        self.grid_bag_sizer = wx.GridBagSizer(hgap=5, vgap=5)
        self.bmp_preview = wx.StaticBitmap(self.pnl, -1, wx.Bitmap(self.image_cover))
        self.grid_bag_sizer.Add(self.bmp_preview, pos=(0, 0), span=(2, 2),
                           flag=wx.EXPAND | wx.LEFT | wx.TOP, border=5)
        self.bmp_screenshot = wx.StaticBitmap(self.pnl, -1, wx.Bitmap(self.image_cover))
        self.grid_bag_sizer.Add(self.bmp_screenshot, pos=(0, 3), span=(2, 2), flag=wx.EXPAND | wx.RIGHT | wx.TOP, border=5)
        self.startButton = wx.ToggleButton(self.pnl, label='Start')
        self.startButton.SetValue(0)
        # stopButton = wx.Button(self.pnl, label='Stop')
        self.screenshotButton = wx.Button(self.pnl, label='ScreenShot')

        self.Bind(wx.EVT_TOGGLEBUTTON, self.showVideo, self.startButton)
        # self.Bind(wx.EVT_BUTTON, self.stopShow, stopButton)
        self.Bind(wx.EVT_BUTTON, self.screenShot, self.screenshotButton)

        self.grid_bag_sizer.Add(self.startButton, pos=(3, 0),
                           flag=wx.EXPAND | wx.LEFT | wx.BOTTOM, border=5)
        # self.grid_bag_sizer.Add(stopButton, pos=(3, 1),
        #                    flag=wx.EXPAND | wx.BOTTOM, border=5)
        self.grid_bag_sizer.Add(self.screenshotButton, pos=(3, 2),
                           flag=wx.EXPAND | wx.BOTTOM, border=5)

        # self.grid_bag_sizer.AddGrowableCol(0, 1)
        # self.grid_bag_sizer.AddGrowableRow(0, 1)


        self.pnl.SetSizerAndFit(self.grid_bag_sizer)

    def _showVideo(self, event):
        value = self.startButton.GetValue()
        self.startButton.SetLabel('stop')
        if(value == True):
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cnt = 0
            while (self.cap.isOpened()):
                success, frame = self.cap.read()
                self.k = cv2.waitKey(np.int(1000./self.fps))
                height, width = frame.shape[:2]
                image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.pic = wx.Bitmap.FromBuffer(width, height, image1)
                self.bmp_preview.SetBitmap(self.pic)
                self.grid_bag_sizer.Fit(self)
                value = self.startButton.GetValue()
                if value == False:
                    self.startButton.SetLabel('start')
                    self.stopShow()
                    break




    def showVideo(self, event):
        import _thread
        # 创建子线程，按钮调用这个方法，
        _thread.start_new_thread(self._showVideo, (event,))
    def stopShow(self):
        self.cap.release()
        self.bmp_preview.SetBitmap(wx.Bitmap(self.image_cover))
        self.grid_bag_sizer.Fit(self)
    def screenShot(self, event):
        if (self.cap.isOpened()):
            success, frame = self.cap.read()
            height, width = frame.shape[:2]
            image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pic = wx.Bitmap.FromBuffer(width, height, image1)
            self.bmp_screenshot.SetBitmap(pic)
            self.grid_bag_sizer.Fit(self)
            self.cnt = self.cnt + 1


class main_app(wx.App):
    # OnInit 方法在主事件循环开始前被wxPython系统调用，是wxpython独有的
    def OnInit(self):
        self.frame = BaseLayout(parent=None, id=-1, title="Test")
        self.frame.Show(True)
        return True

if __name__ == "__main__":
    app = main_app()
    app.MainLoop()


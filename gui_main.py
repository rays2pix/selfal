import os
import wx
from PIL import Image
import numpy as np
import cv2
from dataset import Dataset
 
class Labeller(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Semi-Automatic Labeling ')
        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 240
        self.dataSet = Dataset(images_dir="./data/kitti01/images/",labels_dir="./data/kitti01/labels")
        self.labels = self.dataSet.labels.items()
        self.images = self.dataSet.images.items()
        self.current_frame = self.images[0][1]
        self.next_frame = self.images[1][1]
        #self.createWidgets()
        self.frame.Show()


 
    def onPropagate(self):
        pass      

 
    def onComboSelect(self):
        pass


    def createWidgets(self):
        instructions = 'Select Data set directory'
        img = wx.EmptyImage(1242,375)
        self.wxCurrentFrame = wx.StaticBitmap(self.panel, wx.ID_ANY,wx.BitmapFromImage(img))        
        self.wxNextFrame = wx.StaticBitmap(self.panel, wx.ID_ANY,wx.BitmapFromImage(img))        

        #Creating holder to display labelled frame
        #self.wxCurrentFrame = wx.EmptyImage(self.dataSet.rows,self.dataSet.cols)
        print type(self.current_frame)
        #self.wxNextFrame = wx.EmptyImage(self.dataSet.rows,self.dataSet.cols)
        #self.wxCurrentFrame.SetData(self.current_frame.tostring())
        #self.wxCurrentFrame.SetBitMap(self.wxCurrentFrame.ConvertToBitmap())
        #self.wxNextFrame.SetData(self.next_frame.tostring())
        #self.wxNextFrame.SetBitMap(self.wxNextFrame.ConvertToBitmap())
 
        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))

        #Browse button to select directory
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        
        #Propagate button to invoke labelling algorithm
        labelBtn = wx.Button(self.panel, label='Propagate')
        labelBtn.Bind(wx.EVT_BUTTON, self.onPropagate)
        distros = ["12","3432"] 
        #Combo Box to select the object to be propagated
        cb = wx.ComboBox(self.panel, pos=(50, 30), choices=distros)
        cb.Bind(wx.EVT_COMBOBOX,self.onComboSelect)
        

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.wxCurrentFrame, 0, wx.ALL, 5)
        self.mainSizer.Add(self.wxNextFrame, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)      
        self.buttonsizer.Add(cb,0,wx.ALL,5)  
        self.buttonsizer.Add(labelBtn,0,wx.ALL,5)  

        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.buttonsizer, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
 
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "png files (*.png)|*.png"
        dialog = wx.FileDialog(None, "Choose a directory",
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.onView()
 
    def onView(self):
        self.wxCurrentFrame.SetData(self.current_frame.tostring())
        self.wxCurrentFrame.SetBitMap(self.wxCurrentFrame.ConvertToBitmap())
        self.wxNextFrame.SetData(self.next_frame.tostring())
        self.wxNextFrame.SetBitMap(self.wxNextFrame.ConvertToBitmap())
        self.panel.Refresh()

 
if __name__ == '__main__':
    app = Labeller()
    app.MainLoop()
	

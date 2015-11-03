import os
import wx
from PIL import Image
import numpy as np
import cv2
from dataset import Dataset
import  propagate_label 

def propagate_label_gmm(previmage,objmask,nextimage):
    rows = previmage.shape[0]
    cols = previmage.shape[1]
    gmm_mask = np.ones((rows,cols),np.uint8)
    gmm_mask = gmm_mask * 0
	#print np.sum(gmm_mask)
    gmm_mask[objmask[0],objmask[1]] = 3
    sure_fg = np.random.randint((objmask[0].shape[0]),size=100)
    for x in np.nditer(sure_fg):
        gmm_mask[objmask[0][x],objmask[1][x]] = 1
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    img = nextimage
    print type(img[0][0])
    tmp_mask = np.zeros((rows,cols),np.uint8)
    m1,m2 = np.where(gmm_mask==1)
    r_mask, bgdModel, fgdModel     =  cv2.grabCut(img,gmm_mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
    r_mask, bgdModel, fgdModel     =  cv2.grabCut(img,tmp_mask,(0,199,120,120),bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT| cv2.GC_INIT_WITH_MASK)
    print sure_fg
    print np.sum(gmm_mask)
    print r_mask.shape
    print objmask[1].shape
    print img.shape,r_mask.shape
    l_img =   img* r_mask[:,:,np.newaxis]
    cv2.imwrite('gmmm.png',l_img)
    rgb_np = np.zeros((self.gtframe.width,self.gtframe.height,3))
    rgb_np[np.where(r_mask)]=[0,255,0]
    data = rgb_np
    rescaled =  (255.0 / data.max() * (data - data.min())).astype(np.uint8)
    rgb_image = Image.fromarray(rescaled)
    return rgb_image





def getmasks(np_label):
    labels = {}
    labels['green'] = np.where((np_label==7) | (np_label==8) | (np_label==9))
    labels['sky'] = np.where(np_label == 1)
    labels['road'] = np.where((np_label==2) |  (np_label==4))
    labels['lane'] = np.where(np_label == 5)
    labels['building'] = np.where(np_label == 11)
    labels['vehicle'] = np.where((np_label==17) | (np_label==18) | (np_label==19))
    labels['cycle'] = np.where((np_label==23) |  (np_label==24))
    labels['cyclist'] = np.where((np_label==25) |  (np_label==26))
    return labels
 
class Labeller(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Semi-Automatic Labeling ')
        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 240
        self.dataSet = Dataset(images_dir="./data/kitti01/images/",labels_dir="./data/kitti01/labels")
        self.labels = self.dataSet.labels.items()
        self.images = self.dataSet.images.items()
        labels_desc = self.dataSet.label_desc.values()
        print labels_desc[0]
        self.objects = [ label[0] for label in labels_desc]
        self.labeldict = getmasks(self.labels[0][1])
        print "Masks are ready"
        print self.labeldict.values()
        self.objects = list(set(self.objects))
        print self.objects
        self.current_frame = self.images[0][1]
        self.next_frame = self.images[1][1]
        rgb_label=   self.dataSet.makeRGBLabelFromInt(self.labels[0][1])
        ol = self.dataSet.overlayRGBonImage(rgb_label,self.images[0][1])
        cv2.imwrite('ol.png',ol)

        self.createWidgets()
        self.frame.Show()


 
    def onPropagate(self,event):
        '''The workhorse function to experiement with. Replace propagate_label with propagate_label_xxx 
            where xxx is your experiment. '''
        propagated_label = propagate_label.algo_gmm(self.current_frame,self.mask,self.next_frame)      

 
    def onComboSelect(self,event):
        self.selected_obj =  event.GetString()
        print self.selected_obj
        rgb_np = np.zeros((self.dataSet.rows,self.dataSet.cols,3))
        self.mask = self.labeldict[self.selected_obj]
        rgb_np[self.mask]=[0,255,0]
        data = rgb_np
        rescaled =  (255.0 / data.max() * (data - data.min())).astype(np.uint8)
        rgb_image = Image.fromarray(rescaled)
        ol = self.dataSet.overlayRGBonImage(rescaled,self.images[0][1])
        cv2.imwrite('ol.png',ol)
        self.onView()



    def createWidgets(self):
        instructions = 'Select Data set directory'
        img = wx.EmptyImage(self.dataSet.cols,self.dataSet.rows)
        self.frame.Show()
        self.wxCurrentFrame = wx.StaticBitmap(self.panel, wx.ID_ANY,wx.BitmapFromImage(img))        
        self.wxNextFrame = wx.StaticBitmap(self.panel, wx.ID_ANY,wx.BitmapFromImage(img))        

        #Creating holder to display labelled frame
 

        #Browse button to select directory
        #Currently the directories are hard-coded in dataset class
        browseBtn = wx.Button(self.panel, label='Load')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        
        #Propagate button to invoke labelling algorithm
        labelBtn = wx.Button(self.panel, label='Propagate')
        labelBtn.Bind(wx.EVT_BUTTON, self.onPropagate)
        distros = ["12","3432"] 
        #Combo Box to select the object to be propagated
        cb = wx.ComboBox(self.panel, pos=(50, 30), choices=self.objects)
        cb.Bind(wx.EVT_COMBOBOX,self.onComboSelect)

        print "Creating sizers.."        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.cf_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.nf_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsizer = wx.BoxSizer(wx.HORIZONTAL)


        self.cf_sizer.Add(self.wxCurrentFrame, 0, wx.ALL, 5)
        self.nf_sizer.Add(self.wxNextFrame, 0, wx.ALL, 5)
        self.buttonsizer.Add(browseBtn, 0, wx.ALL, 5)      
        self.buttonsizer.Add(cb,0,wx.ALL,5)  
        self.buttonsizer.Add(labelBtn,0,wx.ALL,5)  

        self.mainSizer.Add(self.cf_sizer, 0, wx.ALL, 5)
        self.mainSizer.Add(self.buttonsizer, 0, wx.ALL| wx.EXPAND, 5)
        self.mainSizer.Add(self.nf_sizer, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()
 
        print "Layout done" 
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        self.onView()
 
    def onView(self):
        img = wx.Image('ol.png', wx.BITMAP_TYPE_ANY)
        self.wxCurrentFrame.SetBitmap(wx.BitmapFromImage(img))
        next_file= os.path.join(self.dataSet.images_dir,self.images[1][0])
        next_image = wx.Image(next_file, wx.BITMAP_TYPE_ANY)
        self.wxNextFrame.SetBitmap(wx.BitmapFromImage(next_image))
        self.panel.Refresh()


 
if __name__ == '__main__':
    app = Labeller()
    app.MainLoop()
	

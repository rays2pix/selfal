import cv2
from PIL import Image
import os
import numpy as np

class Frame:
    def __init__(self,image,labelled=0):
        self.image = image
        self.labelled = 0
        self.rows = image.shape[0]
        self.cols = image.shape[1]


class Dataset:
    def __init__(self,images_dir=None,labels_dir=None):
        self.images_dir = images_dir
        self.labels_dir = labels_dir
        self.images = {}
        self.labels = {}
        self.label_desc = {7:('green',[0,252,0]),
                           8:('green',[0,252,0]),
                           9:('green',[0,252,0]),
                           1:('sky',[0,0,252]),
                           2:('road',[153,102,51]),
                           2:('road',[153,102,51]),
                           5:('lane',[255,255,102]),
                           11:('building',[255,0,255]),
                           17:('vehicle',[255,0,0]),
                           18:('vehicle',[255,0,0]),
                           19:('vehicle',[255,0,0]),
                           23:('cycle',[255,50,110]),
                           24:('cyclist',[110,110,110]),
                           }
        
        for f in os.listdir(images_dir):
            print "Loading %s" % f
            image = cv2.imread(os.path.join(images_dir,f),0)
            self.images[f] = image

        for f in os.listdir(labels_dir):
            image = cv2.imread(os.path.join(labels_dir,f),0)
            self.labels[f]=image
        print "Dataset_init done"
        self.rows = self.images['001.png'].shape[0]
        self.cols = self.images['001.png'].shape[1]
 
    def makeRGBLabelFromInt(self,intLabel):
        rows = intLabel.shape[0]
        cols = intLabel.shape[1]
        rgb_label = np.zeros((rows,cols,3))
        int_labels = self.label_desc.keys()
        for k in int_labels:
            rgb_label[np.where(intLabel==k)]  = self.label_desc[k][1]
        data = rgb_label
        rgb_label =  (255.0 / data.max() * (data - data.min())).astype(np.uint8)
        cv2.imwrite('rgb.png',rgb_label)
        return rgb_label
    
    def overlayRGBonImage(self,rgblabel,image):
        pil_rgb = Image.fromarray(rgblabel)
        pil_image = Image.fromarray(image)
        background = pil_image.convert("RGBA")
        overlay  = pil_rgb.convert("RGBA")
        new_img = Image.blend(background, overlay, 0.4)
        overlayed_image = np.asarray(new_img)
        return overlayed_image




if __name__ == "__main__":
    kitti_data = Dataset(images_dir="./data/kitti01/images/",labels_dir="./data/kitti01/labels")
    labels = kitti_data.labels.items()
    images = kitti_data.images.items()
    rgb_label=    kitti_data.makeRGBLabelFromInt(labels[0][1])
    ol = kitti_data.overlayRGBonImage(rgb_label,images[0][1])
    cv2.imwrite('overlayed.png',ol)


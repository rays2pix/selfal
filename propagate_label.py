import numpy as np
import cv2

def getrectfrommask(mask):
    row_start = np.min(mask[0])
    row_end   = np.max(mask[0])
    col_start = np.min(mask[1])
    col_end   = np.max(mask[1])
    print row_start,row_end,col_start,col_end
    return [(col_start - col_start , row_start - 50 ), (col_end  ,row_end+40)]




def algo_gmm(previmage,objmask,nextimage):
    rows = previmage.shape[0]
    cols = previmage.shape[1]
    gmm_mask = np.ones((rows,cols),np.uint8)
    gmm_mask = gmm_mask * 0
    print np.sum(gmm_mask)
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

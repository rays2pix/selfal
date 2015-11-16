import numpy as np
import cv2
from sklearn.mixture import GMM

def getrectfrommask(mask):
    row_start = np.min(mask[0])
    row_end   = np.max(mask[0])
    col_start = np.min(mask[1])
    col_end   = np.max(mask[1])
    print row_start,row_end,col_start,col_end
    return [(col_start - col_start , row_start - 50 ), (col_end  ,row_end+40)]




def algo_gmm(previmage,objmask,nextimage):
    ''' 1. form a mixture model using obj pixels
        2. Classify every pixel in nextimage
        3. Threshold it and classify'''
    import sklearn
    rows = previmage.shape[0]
    cols = previmage.shape[1]
    print previmage.shape
    objpixels = previmage[objmask]
    bgpix = np.ones((rows,cols))
    bgpix[objmask]=0
    bgmask = np.where(bgpix==1)
    bgpixels = previmage[bgmask]
    print objpixels.shape
    obj_gmm_model = GMM(n_components=3)
    obj_gmm_model.fit(objpixels)
    bg_gmm_model = GMM(n_components=3)
    #bg_gmm_model.fit(bgpixels)
    print obj_gmm_model.means_
    next_ = nextimage.reshape((rows*cols,3))
    print next_.shape
    nextlabels_obj = obj_gmm_model.predict_proba(next_)
    #nextlabels_bg = bg_gmm_model.predict_proba(next_)
    nextlabels_obj = nextlabels_obj.reshape(rows,cols,3) 
    nextlabels = obj_gmm_model.predict(next_)    
    print nextlabels_obj.shape
    return nextlabels_obj


''' try out different algorithms following this parameter signature..
    the algorithm is expected to return a numpy array of the label'''
def algo_grabcut(previmage,objmask,nextimage):
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
    return rescaled


def test_algo_gmm():
    samples = np.random.randint(0,250,(5,5))
    next_samples = np.random.randint(0,250,(5,5))
    mask = np.where((samples >50) & (samples <150) ) 
    print next_samples
    algo_gmm(samples,mask,next_samples)


if __name__ == "__main__":
    test_algo_gmm()

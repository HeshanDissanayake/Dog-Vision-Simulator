import cv2
import numpy as np
import ipcamera


import time


A = None 
B = None
X = None
Kinv = None
noSignalImg = None

def cylindricalWarp(img, K):
    global A, B, X, Kinv, noSignalImg 
    if A is None: 
        noSignalImg = cv2.imread("photos/NoSignal.jpg")
        h_,w_ = img.shape[:2]
        # pixel coordinates
        y_i, x_i = np.indices((h_,w_))
        X = np.stack([x_i,y_i,np.ones_like(x_i)],axis=-1).reshape(h_*w_,3) # to homog
        Kinv = np.linalg.inv(K) 
        X = Kinv.dot(X.T).T # normalized coords
        # calculate cylindrical coords (sin\theta, h, cos\theta)
        A = np.stack([np.sin(X[:,0]),X[:,1],np.cos(X[:,0])],axis=-1).reshape(w_*h_,3)
        B = K.dot(A.T).T # project back to image-pixels plane
        # back from homog coords
        B = B[:,:-1] / B[:,[-1]]
        # make sure warp coords only within image bounds
        B[(B[:,0] < 0) | (B[:,0] >= w_) | (B[:,1] < 0) | (B[:,1] >= h_)] = -1
        B = B.reshape(h_,w_,-1)
    
    img_rgba = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA) # for transparent borders...
    # warp the image according to cylindrical coords
    return cv2.remap(img_rgba, B[:,:,0].astype(np.float32), B[:,:,1].astype(np.float32), cv2.INTER_AREA, borderMode=cv2.BORDER_TRANSPARENT)
  


def get(imgs):
    if len(imgs)!= 0:
        c_y = 80 #crop y
        c_x = 80 #crop x


        merged = np.zeros((imgs[0].shape[0], imgs[0].shape[1]*len(imgs), 4 )).astype(np.uint8)
        h, w = imgs[0].shape[:2]
        
        x_start = 0
        x_end = w - c_x

        y_start = 0
        y_end = h - c_y

        K = np.array([[500,0,w/2],[0,800,h/2],[0,0,1]]) # mock intrinsics
        
        merged = None
        for img in imgs:
            img_cyl = cylindricalWarp(img, K)
            img_cyl = img_cyl[c_y:h-c_y, c_x:w-c_x, :] 
            if merged is None:
                merged = img_cyl
            else:
                merged = np.concatenate([merged, img_cyl],axis=1)



        # merged[:, :img1.shape[1], :] = img_cyl1
        # merged[:, img1.shape[1]*1-78:img1.shape[1]*2-(178), :] = img_cyl2[:, 100:, :]
        # merged[:, img1.shape[1]*2-256:img1.shape[1]*3-(356), :] = img_cyl3[:, 100:,:]
                
        # cropped = merged[c_y:merged.shape[0]-c_y, :, :]

        return merged
    else:
        return np.zeros((250, 640, 3)).astype(np.uint8)
def run():
    img1 = cv2.imread("/home/heshds/fiverr/panaroma_video/photos/1.jpeg")
    img2 = cv2.imread("/home/heshds/fiverr/panaroma_video/photos/2.jpeg")
    img3 = cv2.imread("/home/heshds/fiverr/panaroma_video/photos/3.jpeg")

    h, w = img1.shape[:2]
    x = 0
    y = 0
    c = 0
    K = np.array([[800,0,w/2],[0,800,h/2],[0,0,1]]) # mock intrinsics
    merged = np.zeros((img1.shape[0], img1.shape[1]*3, 4 )).astype(np.uint8)
    
    while True:
        img_cyl1 = cylindricalWarp(img1, K)
        img_cyl2 = cylindricalWarp(img2, K)
        img_cyl3 = cylindricalWarp(img3, K)

        merged = np.zeros((img1.shape[0], img1.shape[1]*3, 4 )).astype(np.uint8)
        print(img_cyl1.shape, merged.shape)

        merged[:, :img1.shape[1], :] = img_cyl1
        merged[:, img1.shape[1]*1-x:img1.shape[1]*2-(x+100), :] = img_cyl2[:, 100:, :]
        merged[:, img1.shape[1]*2-y:img1.shape[1]*3-(y+100), :] = img_cyl3[:, 100:,:]
             
        cropped = merged[c:merged.shape[0]-c, :, :]
            
        print("c: %d, x: %d, y: %d"%(c,x,y))
        cv2.imshow("asd", cropped)
        key = cv2.waitKey(10)
        if key == 81:
            x = x + 2 
        if key == 82:
            y = y + 2
        if key == 83:
            c = c + 2

        if key == 27:
            break

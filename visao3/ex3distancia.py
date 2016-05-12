
import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

cap = cv2.VideoCapture('benalet.mp4')
font = cv2.FONT_HERSHEY_SIMPLEX

img1 = cv2.imread('benalet.PNG',0)  
ret, img30 = cap.read()
sift = cv2.SIFT()

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img30,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)
    img2b = cv2.polylines(img30,[np.int32(dst)],True,255,3, cv2.CV_AA)

    a1 = abs(np.int32(dst[0][0][1]) - np.int32(dst[1][0][1]))
    a2 = abs(np.int32(dst[2][0][1]) - np.int32(dst[3][0][1]))
    Ap = abs(a2 + a1)/2
    Ar = 12
    Dr = 30
    f = ((Ap*Dr)/Ar)


else:
    print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
    matchesMask = None


while(cap.isOpened()):

    ret, img2 = cap.read()
    sift = cv2.SIFT()

    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img2b = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.CV_AA)
        
        a3 = abs(np.int32(dst[0][0][1]) - np.int32(dst[1][0][1]))
        a4 = abs(np.int32(dst[2][0][1]) - np.int32(dst[3][0][1]))
        ap = abs(a4 + a3)/2

        d = (f*Ar)/ap
        print("foco:",f)
        print("Altura pixel inicial:",Ap)
        print("Altura pixel momentanea:", ap)
        print("distancia camera do objeto:",d)
        cv2.putText(img2,"{0} cm".format(str(d)),(10,30), font, 1,(255,0,0),5,cv2.CV_AA)

    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        matchesMask = None

    
    cv2.imshow('frame',img2)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

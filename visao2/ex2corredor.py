from __future__ import print_function

import numpy as np
import cv2
import sys
import math

cap = cv2.VideoCapture('hall_box_battery.mp4')


while(cap.isOpened()):
	
	s, img = cap.read()
	d,e,f = img.shape
	winName = "Movement Indicator"
	
	cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
	
	edges = cv2.Canny(img, 100, 300)
	cdst = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

	if True: 
		
		lines = cv2.HoughLinesP(edges, 1, math.pi/180.0, 40, np.array([]), 80, 90)
		
		a,b,c = lines.shape		
		
		for i in range(a):
			x = 0
			j = 0
			while x==0 :

				x1 = lines[i][j][0]
				y1 = lines[i][j][1]
				x2 = lines[i][j][2]
				y2 = lines[i][j][3]
				x3 = lines[i][j+1][0]
				y3 = lines[i][j+1][1]
				x4 = lines[i][j+1][2]
				y4 = lines[i][j+1][3]

				if abs(x1 - x2)< 70: #Nao escole linha na vertical
					j+=1
				else :
					if abs(x1-x3<20 or x2-x4<20 or x1-x4<20 or x2-x3<20):
						if j < 6:
							j+=1
							
						else:
							print("nao foi possivvel encontrar o meio do corredor")
							x=1

					else:
						cv2.line(cdst, (lines[i][j][0], lines[i][j][1]), (lines[i][j][2], lines[i][j][3]), (0, 0, 255), 3, cv2.CV_AA)
						cv2.line(cdst, (lines[i][j+1][0], lines[i][j+1][1]), (lines[i][j+1][2], lines[i][j+1][3]), (0, 0, 255), 3, cv2.CV_AA)
						cv2.line(cdst, ((x1+x2+x3+x4)/4, d), ((x1+x2+x3+x4)/4, 0), (0, 255, 0), 3, cv2.CV_AA)
						x=1
				   

	cv2.imshow('detected lines', cdst)

	if cv2.waitKey(50) & 0xff == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()


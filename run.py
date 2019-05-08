import cv2
import numpy as np
import os


gestureContourList = []

def generateContours():
	names = os.listdir("gestures/")
	gestureContourList = []
	for name in names:
		tmp = cv2.imread("gestures/"+name)
		tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
		tmp = cv2.GaussianBlur(tmp, (5,5), 0)
		_, tmp = cv2.threshold(tmp, 50, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		_, tmp, _ = cv2.findContours(tmp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		gestureContourList.append([name[:-4],tmp])
	return gestureContourList
		

def compare(contours):
	lowestNum = 1.0
	gestureShape = ""
	for cont in gestureContourList:
		gesture = cont[1]
		#print(cont[0])
		similarity = cv2.matchShapes(contours[0], gesture[0], 1, 0.0)
		if similarity < lowestNum:
			lowestNum = similarity
			gestureShape = cont[0]

	return gestureShape

def start():
	cap = cv2.VideoCapture(2)
	while(True) :
		ret,img = cap.read()
		cv2.imwrite("saved.png", img) # this is for saving pictures of ur hand to use for comparison
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray,(5,5),0)
		ret,thresh = cv2.threshold(blur,50,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	
		im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		drawing = np.zeros(img.shape,np.uint8)

		max_area=0

		for i in range(len(contours)):
			cnt=contours[i]
			area = cv2.contourArea(cnt)
			if(area>max_area):
				max_area=area
				ci=i

		cnt=contours[ci]
		hull = cv2.convexHull(cnt)
		moments = cv2.moments(cnt)

		if moments['m00']!=0:
			cx = int(moments['m10']/moments['m00'])
			cy = int(moments['m01']/moments['m00'])
				
		center=(cx,cy)
		#cv2.circle(img, center, 40, [0,255,180], 2)
		cv2.circle(img, center, 5, [0,255,255], 2)
		cv2.drawContours(drawing, [cnt], 0, (0,255,0), 2) 
		cv2.drawContours(drawing, [hull], 0, (255,100,0), 2) 
			
		cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
		hull = cv2.convexHull(cnt,returnPoints = False)
		

		try:
			defects = cv2.convexityDefects(cnt,hull)
			mind=0
			maxd=0
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(cnt[s][0])
				end = tuple(cnt[e][0])
				far = tuple(cnt[f][0])
				dist = cv2.pointPolygonTest(cnt,center,True)
				cv2.line(img,start,end,[255,100,0],2)
				
				cv2.circle(img,far,5,[0,0,255],-1)

				cv2.putText(img, str(compare(contours)), center, 0, 1.0, [255, 255, 255], 1)
			i=0
		except AttributeError:
			print("no shape")
		
		cv2.imshow('output',drawing)
		cv2.imshow('input',img)

		if(cv2.waitKey(1) & 0xFF == ord('q')):
			break

if __name__ == "__main__":
	gestureContourList = generateContours()
	#print(gestureContourList)
	start()
	cv2.destroyAllWindows
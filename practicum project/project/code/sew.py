import numpy as np
import cv2
import sys
from matchers import Sew
import time

class Stitch:
	def __init__(self, args):
		self.path = args
		fp = open(self.path, 'r')
		ImageList = [nextImage.rstrip('\r\n') for nextImage in  fp.readlines()]
		self.images = [cv2.resize(cv2.imread(nextImage),(480, 320)) for nextImage in ImageList]
		self.imagesCount = len(self.images)
		self.left_list, self.right_list = [], []
		self.matcher_obj = Sew()
		self.prepare_lists()

	def prepare_lists(self):
		self.centerIdx = self.imagesCount/2 
		for i in range(self.imagesCount):
			if(i<=self.centerIdx):
				self.left_list.append(self.images[i])
			else:
				self.right_list.append(self.images[i])
	def leftshift(self):
		startImage = self.left_list[0]
		for nextImage in self.left_list[1:]:
			Homograph = self.matcher_obj.match(startImage, nextImage)
			invHomograph = np.linalg.inv(Homograph)
			dotInvHomograph = np.dot(invHomograph, np.array([startImage.shape[1], startImage.shape[0], 1]));
			dotInvHomograph = dotInvHomograph/dotInvHomograph[-1]
			dotHomograph = np.dot(invHomograph, np.array([0,0,1]))
			dotHomograph = dotHomograph/dotHomograph[-1]
			invHomograph[0][-1] += abs(dotHomograph[0])
			invHomograph[1][-1] += abs(dotHomograph[1])
			dotInvHomograph = np.dot(invHomograph, np.array([startImage.shape[1], startImage.shape[0], 1]))
			Y_axis = abs(int(dotHomograph[1]))
			X_axis = abs(int(dotHomograph[0]))
			dotInvHomographize = (int(dotInvHomograph[0])+X_axis, int(dotInvHomograph[1]) + Y_axis)
			temp = cv2.warpPerspective(startImage, invHomograph, dotInvHomographize)
			temp[Y_axis:nextImage.shape[0]+Y_axis, X_axis:nextImage.shape[1]+X_axis] = nextImage
			startImage = temp
		self.combinedImage = temp
	def rightshift(self):
		for nextImage in self.right_list:
			Homograph = self.matcher_obj.match(self.combinedImage, nextImage)
			similar_Threshold = np.dot(Homograph, np.array([nextImage.shape[1], nextImage.shape[0], 1]))
			similar_Threshold = similar_Threshold/similar_Threshold[-1]
			dotInvHomographize = (int(similar_Threshold[0])+self.combinedImage.shape[1], int(similar_Threshold[1])+self.combinedImage.shape[0])
			temp = cv2.warpPerspective(nextImage, Homograph, dotInvHomographize)
			temp = self.mix_and_match(self.combinedImage, temp)
			self.combinedImage = temp
		cv2.imshow("tp", temp)
		cv2.waitKey()
	def mix_and_match(self, combinedImage, tempImage):
		CIH, CIW = combinedImage.shape[:2]
		TIH, TIW = tempImage.shape[:2]

		for i in range(0, CIW):
			for j in range(0, CIH):
				try:
					if(np.array_equal(combinedImage[j,i],np.array([0,0,0])) and  np.array_equal(tempImage[j,i],np.array([0,0,0]))):
						tempImage[j,i] = [0, 0, 0]
					else:
						if(np.array_equal(tempImage[j,i],[0,0,0])):
							tempImage[j,i] = combinedImage[j,i]
						else:
							if not np.array_equal(combinedImage[j,i], [0,0,0]):
								bl,gl,rl = combinedImage[j,i]
								tempImage[j, i] = [bl,gl,rl]
				except:
					pass
		return tempImage
try:
	args = sys.argv[1]
except:
	args = "txtlists/files2.txt"
finally:
	print ("Parameters : ", args)
s = Stitch(args)
s.leftshift()
s.rightshift()
gray = cv2.cvtColor(s.combinedImage,cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
ig,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
x,y,w,h = cv2.boundingRect(cnt)
crop = s.combinedImage[y:y+h,x:x+w]
ch,cw = crop.shape[:2]
print(ch,cw)
for i in range(0,cw):
	for j in range(0,ch):
		if(np.array_equal(crop[j,i],[0,0,0])):
			crop[j,i] = [255,255,255]
	
cv2.imshow("out",crop)
cv2.waitKey(0)
cv2.imwrite("output.jpg", crop)
print ("SUCCESS")
cv2.destroyAllWindows()


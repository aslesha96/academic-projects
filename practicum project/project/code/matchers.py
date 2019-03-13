import cv2
import numpy as np 

class Sew:
	def __init__(self):
		self.surf = cv2.xfeatures2d.SURF_create()
	def match(self, i1, i2, direction=None):
		image_1 = self.getSURFFeatures(i1)
		image_2 = self.getSURFFeatures(i2)
		Descriptor = cv2.DescriptorMatcher_create("BruteForce")
		matches = Descriptor.knnMatch(image_2['features'],image_1['features'],k=2)
		good = []
		for i , (m, n) in enumerate(matches):
			if m.distance < 0.75*n.distance:
				good.append((m.trainIdx, m.queryIdx))
		if len(good) > 4:
			pointsCurrent = image_2['keyPoints']
			pointsPrevious = image_1['keyPoints']

			matchedPointsCurrent = np.float32([pointsCurrent[i].pt for (__, i) in good])
			matchedPointsPrev = np.float32([pointsPrevious[i].pt for (i, __) in good])

			H, s = cv2.findHomography(matchedPointsCurrent, matchedPointsPrev, cv2.RANSAC, 4)
			return H
		return None

	def getSURFFeatures(self, im):
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		keyPoints, des = self.surf.detectAndCompute(gray, None)
		return {'keyPoints':keyPoints, 'features':des}
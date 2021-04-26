import cv2
import numpy as np
# class Stitcher:
# 	def __init__(self):
# 		# determine if we are using OpenCV v3.X and initialize the
# 		# cached homography matrix
# 		self.isv3 = imutils.is_cv3()
# 		self.cachedH = None


# cap = cv2.VideoCapture(0)

cachedH = None

def detectAndDescribe(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# return a tuple of keypoints and features

	descriptor = cv2.xfeatures2d.SIFT_create()
	(kps, features) = descriptor.detectAndCompute(image, None)

	kps = np.float32([kp.pt for kp in kps])

	return (kps, features)

def matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
	# compute the raw matches and initialize the list of actual
	# matches
	matcher = cv2.DescriptorMatcher_create("BruteForce")
	rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
	matches = []

	# loop over the raw matches
	for m in rawMatches:
		# ensure the distance is within a certain ratio of each
		# other (i.e. Lowe's ratio test)
		if len(m) == 2 and m[0].distance < m[1].distance * ratio:
			matches.append((m[0].trainIdx, m[0].queryIdx))
		# computing a homography requires at least 4 matches
	if len(matches) > 4:
		# construct the two sets of points
		ptsA = np.float32([kpsA[i] for (_, i) in matches])
		ptsB = np.float32([kpsB[i] for (i, _) in matches])
		# compute the homography between the two sets of points
		(H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
			reprojThresh)
		# return the matches along with the homograpy matrix
		# and status of each matched point
		return (matches, H, status)
	# otherwise, no homograpy could be computed
	return None

def stitch(images, ratio=0.75, reprojThresh=4.0):

	global cachedH

	# unpack the images
	(imageB, imageA) = images
	# if the cached homography matrix is None, then we need to
	# apply keypoint matching to construct it
	if cachedH is None:
		# detect keypoints and extract
		(kpsA, featuresA) = detectAndDescribe(imageA)
		(kpsB, featuresB) = detectAndDescribe(imageB)
		# match features between the two images
		M = matchKeypoints(kpsA, kpsB,
			featuresA, featuresB, ratio, reprojThresh)
		# if the match is None, then there aren't enough matched
		# keypoints to create a panorama
		if M is None:
			print('no matches')
			return None

		# cache the homography matrix
		cachedH = M[1]
	# apply a perspective transform to stitch the images together
	# using the cached homography matrix
	result = cv2.warpPerspective(imageA, cachedH,(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
	
	result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
	# return the stitched image
	return result
	

img1 = cv2.imread("/home/heshds/fiverr/panaroma_video/photos/img1.jpeg")
img2 = cv2.imread("/home/heshds/fiverr/panaroma_video/photos/img2.jpeg")
images = [img1, img2]

kpsA, featuresA = detectAndDescribe(img1)
kpsB, featuresB = detectAndDescribe(img2)

img = stitch(images)
print(img.shape)
while True:
	cv2.imshow("lol", img)
	cv2.waitKey(0)
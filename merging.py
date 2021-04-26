def stitch(self, images, ratio=0.75, reprojThresh=4.0):
		# unpack the images
		(imageB, imageA) = images
		# if the cached homography matrix is None, then we need to
		# apply keypoint matching to construct it
		if self.cachedH is None:
			# detect keypoints and extract
			(kpsA, featuresA) = self.detectAndDescribe(imageA)
			(kpsB, featuresB) = self.detectAndDescribe(imageB)
			# match features between the two images
			M = self.matchKeypoints(kpsA, kpsB,
				featuresA, featuresB, ratio, reprojThresh)
			# if the match is None, then there aren't enough matched
			# keypoints to create a panorama
			if M is None:
				return None
			# cache the homography matrix
			self.cachedH = M[1]
		# apply a perspective transform to stitch the images together
		# using the cached homography matrix
		result = cv2.warpPerspective(imageA, self.cachedH,
			(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
		result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
		# return the stitched image
		return result
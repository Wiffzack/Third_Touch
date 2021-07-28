# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
import math
import numpy as np
import cv2 as cv
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from PIL import ImageEnhance

import sys
# from PIL import Image
# import numpy as np
# from matplotlib import pyplot as plt
import math

import binascii
import struct
import scipy
import scipy.misc
import scipy.cluster
from scipy import fftpack
import os
import shutil, sys, os, glob, cv2
from scipy.stats import kurtosis,skew
from skimage.metrics import structural_similarity as compare_ssim

import argparse
#import matplotlib.pyplot as pyplot
#from shutil import copyfile
import shutil
#copyfile(src, dst)

import time
from pathlib import Path

inFile = sys.argv[1]
#img_read = cv2.imread(inFile)
#outFile = sys.argv[2]
filename=""

detail_entropy = 0

counter = 0 


detail_entropy = 0

counter = 0 

## stackoverflow
def split_image(img):
	img2 = img
	image_array=[]
	height, width = img.shape
	CROP_W_SIZE  = 2
	CROP_H_SIZE = 2
	for ih in range(CROP_H_SIZE ):
		for iw in range(CROP_W_SIZE ):

			x = (int)(width/CROP_W_SIZE * iw)
			y = (int)(height/CROP_H_SIZE * ih)
			h = (int)(height / CROP_H_SIZE)
			w = (int)(width / CROP_W_SIZE )
			img = img[y:y+h, x:x+w]
			image_array.append(img)
			img = img2
	return image_array

def image_entropy(img):
	"""calculate the entropy of an image"""
	histogram = img.histogram()
	histogram_length = sum(histogram)

	samples_probability = [float(h) / histogram_length for h in histogram]

	return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])



def estimate_noise(img):
	from scipy.signal import convolve2d
	#I = img.convert('L')
	H, W = img.shape
	M = [[1, -2, 1],
	   [-2, 4, -2],
	   [1, -2, 1]]
	sigma = np.sum(np.sum(np.absolute(convolve2d(img, M))))
	sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (W-2) * (H-2))
	return sigma

#Average Pixel Width 
def average_pixel_width(img):
	image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return image.mean(axis=0).mean()

# Image Blurrness	
def get_blurrness_score(image):
	path = image 
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = cv2.Laplacian(image, cv2.CV_64F).var()
	return fm	

def RMS_Contrast(image):
	image =np.asarray(image)	
	img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	contrast = img_grey.std()
	return contrast

	
def derivate(image):
        laplacian = cv.Laplacian(image,cv.CV_32F)
        #sobelx = cv.Sobel(image,cv.CV_32F,1,0,ksize=5)
        #sobely = cv.Sobel(image,cv.CV_32F,0,1,ksize=5)
        #meanx = np.mean(sobelx)
        #meany = np.mean(sobely)
        return np.mean(laplacian)

def color_mean(image):
        (means, stds) = cv2.meanStdDev(image)
        stat = np.concatenate([means, stds]).flatten()
        return stat[4]

def level_of_information(img):
	global detail_entropy
	img =np.asarray(img)
	gray_img  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	noise_lv = estimate_noise(gray_img)
	detail_entropy = image_entropy(Image.fromarray(img))
	avvp = average_pixel_width(img)
	blur_value = get_blurrness_score(img)
	info_lv = ((detail_entropy*avvp)/(noise_lv*blur_value))
	return info_lv

#print (level_of_information(img_read))

def variance(image):
        return np.var(image)

def skewv(image):
        return skew(image, axis=None)

def find_sub_max(arr, n):
	low_noise_counter=0
	last_max_index=0
	last_value=0
	for i in range(n-1):
		arr_ = arr
		arr_[np.argmax(arr_)] = np.min(arr)
		arr = arr_
		#print("The largest number in # arr is {}, in the {} bit".format(np.max(arr_), np.argmax(arr_)+1))
		#print (np.where(arr == np.max(arr_)))
		#if (np.argmax(arr_)<last_max_index || (last_value-np.max(arr_))>12):
			#low_noise_counter=low_noise_counter+1
		diff=abs(last_value-np.max(arr_))
		#print (diff)
		if (diff>2 and last_value!=0):
			if(diff>10):
				low_noise_counter=low_noise_counter+4
				return low_noise_counter
			low_noise_counter=low_noise_counter+1
		last_max_index=np.argmax(arr_)
		last_value = np.max(arr_)

	return low_noise_counter


#dt = 1
dt = 1 / 10

if __name__ == '__main__':
	for filename in os.listdir(inFile):
		if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"): 
			print (filename)
			os.chdir(inFile)
			filename = os.path.abspath(filename)
			img_read = cv2.imread(filename)
			img_read = cv2.resize(img_read, (800, 600), interpolation = cv2.INTER_AREA)
			gray = cv2.cvtColor(img_read, cv2.COLOR_BGR2GRAY)
			img = cv2.resize(gray, (800, 600), interpolation = cv2.INTER_AREA)
			#img = cv2.imread(filename,0)

			#img = cv2.resize(img, (800, 600), interpolation = cv2.INTER_AREA)
			f = np.fft.fft2(img)
			fshift = np.fft.fftshift(f)
			magnitude_spectrum = 20*np.log(np.abs(fshift))
			image_array=split_image(magnitude_spectrum)
			img_flip4 = np.flip(image_array[0], axis=1)
			img_flip4 = cv2.flip(img_flip4, 0)
			(score, diff) = compare_ssim(img_flip4, image_array[3], full=True)

			y = img.flatten()
			t = np.arange(0, y.shape[-1])
			sigFFT = np.fft.fft(y)/t.shape[0]
			freq = np.fft.fftfreq(t.shape[0], d=dt)
			firstNegInd = np.argmax(freq < 0)
			sigFFTPos = 2 * sigFFT[0:firstNegInd]
			count = find_sub_max(np.abs(sigFFTPos), 12)
			color_der = color_mean(img_read)
			sk = skewv(img_read)
			# ca. 1.2 is correction value for scaling
			level = level_of_information(img_read)
			#print ((score>0.03))
			#print ((count<4))
			#print ((detail_entropy>6))
			#print ((sk>-2.1))
			#print ((level>0.1))
			if(score>0.02 and level>0.1 and level<10 and count <4 and color_der>30 and detail_entropy>6 and sk>=-2.1):
				print ("Image fullfil the expectations unlike the code")
				shutil.copy2(filename, "/home/wiffzack/fft_class/"+os.path.basename(filename))
			counter=counter+1	

		else:
			continue


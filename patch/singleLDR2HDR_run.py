from src.hdr import *
import os
#import limitt
import signal
import resource
import time

image_array = []

def split_image(img):
	#np.delete(image_array)
	img_array_list = []
	newlist = image_array[2:]
	img2 = img

	height, width, channels = img.shape
	CROP_W_SIZE  = 2
	CROP_H_SIZE = 1
	for ih in range(CROP_H_SIZE ):
		for iw in range(CROP_W_SIZE ):

			x = (int)(width/CROP_W_SIZE * iw)
			y = (int)(height/CROP_H_SIZE * ih)
			h = (int)(height / CROP_H_SIZE)
			w = (int)(width / CROP_W_SIZE )
			print(x,y,h,w)
			img = img[y:y+h, x:x+w]

			img_array_list.append(img)
			img = img2
	return img_array_list



if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:  python run.py [image_path]")
		sys.exit()

	filepath = sys.argv[1]
	w = sys.argv[2]
	a = sys.argv[3]

	for filename in os.listdir(filepath):
		if filename.endswith(".jpg") or filename.endswith(".png"): 
			output_image1 = []
			v_img = []
			# Read image from file
			os.chdir(filepath)
			print (filename)
			try:
				image = cv2.imread(filename,-1)
			except:
				continue
			try:
				HDR_Filer = FakeHDR(True)
				#print (newstr)
				#try:
				img_array_list_return = split_image(image)
				output_image1 = HDR_Filer.process(img_array_list_return[0],w,a)
				output_image2 = HDR_Filer.process(img_array_list_return[1],w,a)
				v_img = cv2.hconcat([output_image1, output_image2])
				cv2.imwrite(os.path.basename(filename), 255*v_img)
			except Exception as e:
				print(e)
				#time.sleep(1)
			#except:
				#pass
			#Show_origin_and_output(image, output_image)
		else:
        		continue



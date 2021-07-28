

#!/usr/bin/bash ulimit -Sv 1000000

cd $1


echo "set memory limit uvlimit ~5.7GB"
ulimit -Sv 5708100
ulimit -m  5700000

smooth=0.3
dct=10
dct2=15
clahe_value=0.5
alpha=1.5
blur=0.30
zero=0.000
redlimit=-1.00
compare=165
hell=180

# run.py
# run_single.py
python /image/singleLDR2HDR/run.py  /home/wiffzack/bright/ 2.0 $alpha

echo "Artifact removing in bright"
for f in *.png
do
	#if [ -n "$(find "$f" -prune -size +1000000c)" ]; then
	        echo $f
		noise=$(identify -verbose $f | grep -E "deviation" | head -n 1 | awk '{ print $4 }')
		noise=$(echo $noise | cut -c2-8)
		sharp=$(python /image/sharpness.py $f)
		echo "sharpness : $sharp"
		if (( $(bc -l <<< "${noise/e/E} < ${smooth/e/E}") ))
		then
			echo "Image is smooth so no further extrem smoothing applied..."
    			dct=10
			dct2=5
			clahe_value=0.3
			alpha=1.3
		else
			dct=10
			dct2=15
			clahe_value=0.9
		fi 
		filename="${f%.*}"
		python /image/contrast/entropy_preserving/main.py $f

		bright=$(convert $f -colorspace gray -resize 1x1 -format "%[pixel:p{0,0}]" info: | tr -d -c 0-9:)
		# fft style transfer with low frequenz
                 if [ "$style_trasfer" ]
                then
                #cp $f old.$f
                #python /image/style_transfer/FDA/transfer.py 0.00000009 $f /image/styles/hdr_style.jpg
                #composite -blend 40x60 old.$f $f $f
		#rm old.$f
		 if [ "$bright" -lt "$hell" ]
                then
                        convert $f -brightness-contrast -25x20 $f
		else
			convert $f -brightness-contrast -45x15 $f
		fi
		fi
		# important brightness only with the second !
                #convert $f -alpha off  -function Sinusoid 0.40,-45  -white-threshold 95%  $f
                #convert $f -alpha off  -function Sinusoid 0.40,-55  -white-threshold 95% -brightness-contrast -35x0 $f
		convert $f -alpha off  -function Sinusoid 0.40,-45  -white-threshold 95% sin.jpg
		convert $f -alpha off -negate  -evaluate cos 0.50 -white-threshold 92%  cos.jpg
		#composite -blend 50x50 sin.jpg cos.jpg $f
                if [ "$bright" -lt "$hell" ]
                then
			composite -blend 55x45 sin.jpg cos.jpg $f
                else
			composite -blend 40x60 sin.jpg cos.jpg $f
                fi
		rm sin.jpg cos.jpg

                convert $f  -statistic Gradient 5x7  -statistic Gradient 3x5 -threshold 30%  -morphology Dilate Octagon -antialias  grad.jpg
                convert $f grad.jpg -alpha off -compose copy_opacity -composite edges.png
		dctdenoising $dct $f $f  
		composite -blend 80x20 $f edges.png $f
		# -unsharp 0x2+1+0
		cartoonv=$(identify -verbose $f  | grep skewness | tail -n 1 | awk '{print $2}')
		#echo $cartoonv
                if (( $(bc -l <<< "${cartoonv/e/E} < ${zero/e/E}") ))
                then
			# cartoon identified
			redv=$( identify -verbose $f | grep skewness | head -n 1 | awk '{print $2}')
                        if (( $(bc -l <<< "${redv/e/E} > ${redlimit/e/E}") ))
		        then
				echo "saturation push !!!!!!!!!!!!----"
		                convert  -profile hdr.icc -cdl  config_patch5.xml   -evaluate log 10  -modulate 100,120,300 -brightness-contrast -40x10 -white-threshold 92% -gaussian 4 $f - | composite  -compose overlay $f - $f
			else
		                convert  -profile hdr.icc   -evaluate log 10  -modulate 100,120,300 -brightness-contrast -40x15 -white-threshold 92% -gaussian 4 $f - | composite  -compose overlay $f - $f
			fi
		else
	                convert  -profile hdr.icc   -evaluate log 10  -modulate 100,120,300 -brightness-contrast -40x10 -white-threshold 92% -gaussian 4 $f - | composite  -compose overlay $f - $f
		fi

                #python /image/2dclahe.py $f
                python /image/contrast/entropy_preserving/main.py $f
		python /image/contrast/agcwd.py --image $f  --w $clahe_value
		#composite -blend 80x20 $f edges.png $f
                convert $f -adaptive-sharpen 1x3 -unsharp 1.0x1.0+0.5+0.1  -brightness-contrast -15x0  -background white -flatten -alpha off $filename".png"
		convert $filename".png" $f
		#convert $filename".png" $f
		new_sharp=$(python /image/sharpness.py $f)
                echo "sharpness : $new_sharp"
		if [ "$new_sharp" -lt "$sharp" ]
		then
			convert $f -adaptive-sharpen 1x3 -unsharp 1.0x1.0+0.5+0.1  $f
		fi
		echo "seven"

	#fi
done


for f in *.png
do
        python /image/EnhanceHDR/main.py --image_path  /home/wiffzack/bright/$f --filter True
	#convert $f -profile /image/hdr.icc $f
done


# stream loop for gif to loop less obvoius , 
# tmix=frames=4:weights="1 1 1 1 -15 1 1 1" create frames in between
# unsharp for sharping :_
# denoise =  hqdn3d,vaguedenoiser,removegrain,deblock=filter=weak:block=4,fftdnoiz=2:1:4:0.5:0:0
# fftdnoiz[1] > 5 create artifacts
ffmpeg -stream_loop 3 -f gif -i test.gif -vf hqdn3d,vaguedenoiser,removegrain,deblock=filter=weak:block=4,fftdnoiz=2:1:4:0.5:0:0,unsharp,eq=contrast=1.3:brightness=0.05:saturation=1.3,fps=60,tmix=frames=4:weights="1 1 1 1 -15 1 1 1"  output.mp4

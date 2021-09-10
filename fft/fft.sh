# Source : https://legacy.imagemagick.org/Usage/fourier/
convert $1 -fft  +depth \
          \( -clone 0 -write $1_magnitude.png +delete \) \
          \( -clone 1 -write $1_phase.png +delete \) \
          null:

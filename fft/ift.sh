convert $1_magnitude.png $1_phase.png -ift $1_restored.png
dim=$(identify -format '%wx%h'  $1)
convert $1_restored.png -crop $dim $1_restored.png

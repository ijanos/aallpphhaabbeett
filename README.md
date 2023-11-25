# aallpphhaabbeett

Python script to generate 3D letter intersections with blender.

![hello world](imgs/helloworld.gif)

Runing the script will make blender unresponsive for minutes, speed depends on
 CPU performance due to excessive boolean operations (I think).

## Fonts

The font can be customized in the script but picking a good font can be tricky if you want all
letter combinatios to work. Monospaced fonts have a better chance of
success because they mostly fit into a square bounding box.

Look out for `Q` and `J`. In many fonts they tend to have their defining parts below the baseline. Intersected with another
letter Q often becomes O and J becomes I.

Fonts with floating dottes zeroes are not 3D printable.


## Ideas / TODOs

- [ ] different fonts for the 2 sides
- [ ] 3 sided letters?
- [ ] detect if a letter has parts below baseline (maybe a separate script that eats a ttf and spits out bonding boxes?)
- [ ] speed up by generating many (all?) letters at once

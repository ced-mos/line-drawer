# LineDrawer
 
LineDraw recreates a given image by only drawing it by simple straight lines.

## Options
--input-path          Input image path.
--output-path         Input image path.
--num-lines           Number of lines to lines.
--line-heaviness      Line heaviness. Integer from 1 to 255, with 255 being completely heavy.
--num-lines-to-check  Number of lines to lines to check at each iteration.
--draw-type           Draw types (subtractive/additive). Subtractive means white background with black lines. Additive means black background with with lines.
--no-random-result    Will return always the same output with the same config if set.
--output-width        Output image width in pixels where higth will be adapted. Smaller width reduses computation time. "-1" will not change the size.

## Algorithm
The LineDrawer is based on greedy algorithms where for a defined number of lines the best line positions are searched, to mimic the original images as good as possible.
The algorithm works as follows:

for num-lines time
    Search darkest pixel in image
    Select randomly one of the darkest pixels

    for num-lines-to-check
        get random line through previously selected pixel
    Select best fitting and save it to list

for every selected line
    draw line in output image

## Dependencies
- python 3
- see requirements.txt

## Installation & Execution
```bash
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

python src/line_drawer.py --input-path ./example/mani_matter --output-path ./out_image.png --num-lines 10000   
```

## Unittests
```
bash test.sh
```

## Credits
- https://www.reddit.com/r/Art/comments/454joy/drawing_experiment_every_line_goes_through_the/ -> Manual Line Art
- http://linify.me/about - > Javascript implementation
- https://github.com/nathanbain314/lineDrawer --> C++ implementation
- Image from Mani Matter (Source: LP Album Cover - Mani Matter - I Han Es Zündhölzli Azündt - zytglogge Verlag)

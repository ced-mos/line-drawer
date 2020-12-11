# line-drawer
 
line-drawer recreates a given image by only drawing it by simple straight lines.
In the table below you can see the demo image which has been drawn with 10000 lines within 40 seconds, once in the subtractive mode and once in the additive mode.

<table>
  <tr>
    <th><img src="https://github.com/ced-mos/line-drawer/raw/main/example/mani_matter.png" width="200" /></th>
    <th><img src="https://github.com/ced-mos/line-drawer/raw/main/img/mani_matter_subtractive.png" width="200" /></th>
    <th><img src="https://github.com/ced-mos/line-drawer/raw/main/img/mani_matter_additive.png" width="200" /></th>
  </tr>
  <tr>
    <td style="text-align: center">original image</td>
    <td style="text-align: center">subtractive mode</td>
    <td style="text-align: center">additive mode</td>
  </tr>
</table>

## Options

<table>
    <tr>
        <td>--input-path</td>
        <td>Input image path.</td>
    </tr>
    <tr>
        <td>--output-path</td>
        <td>Output image path.</td>
    </tr>
    <tr>
        <td>--num-lines</td>
        <td>Number of lines to draw.</td>
    </tr>
    <tr>
        <td>--line-heaviness</td>
        <td>Line heaviness. Integer from 1 to 255, with 255 being completely heavy.</td>
    </tr>
    <tr>
        <td>--num-lines-to-check</td>
        <td>Number of lines to check at each iteration.</td>
    </tr>
    <tr>
        <td>--draw-type</td>
        <td>Draw types (subtractive/additive). Subtractive means white background with black lines. Additive means black background with with lines.</td>
    </tr>
    <tr>
        <td>--no-random-result</td>
        <td>Will return always the same output with the same config if set.</td>
    </tr>
    <tr>
        <td>--output-width</td>
        <td>Output image width in pixels where hight will be adapted. Smaller width reduses computation time. "-1" will not change the size.</td>
    </tr>
</table>

## Algorithm
The line-drawer is based on greedy algorithms where for a defined number of lines the best line positions are searched, to mimic the original images as good as possible.
The algorithm works as follows:

```
For num-lines times
    Search the darkest pixel in image
    Select randomly one of the darkest pixels

    For num-lines-to-check times
        Get random line through previously selected pixel
    Select best fitting and save it to list

For every selected line
    Draw line in output image
```
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

## Unit tests
```
bash test.sh
```

## Credits
- Basic idea (https://www.reddit.com/r/Art/comments/454joy/drawing_experiment_every_line_goes_through_the/)
- JavaScript implementation (http://linify.me/about)
- C++ implementation (https://github.com/nathanbain314/lineDrawer)
- Image from Mani Matter (Source: LP Album Cover — Mani Matter — I Han Es Zündhölzli Azündt — zytglogge Verlag)

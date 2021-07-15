import argparse
import sys
from enum import Enum

from PIL import Image
import numpy as np
from skimage.draw import line
from tqdm import tqdm
import drawSvg as draw

from geometry import Point, Line, Rectangle

LOGO = "\n\
   / /   (_)___  ___  / __ \_________ __      _____  _____\n\
  / /   / / __ \/ _ \/ / / / ___/ __ `/ | /| / / _ \/ ___/\n\
 / /___/ / / / /  __/ /_/ / /  / /_/ /| |/ |/ /  __/ /    \n\
/_____/_/_/ /_/\___/_____/_/   \__,_/ |__/|__/\___/_/ "


class DrawType(Enum):
    ADDITIVE = 1
    SUBTRACTIVE = 2


def draw_line_image(lines, image_shape, draw_type, line_heaviness=10):
    """Draws line image into numpy array given a list of lines.

    Args:
        lines (list: List of point pairs
        image_shape (tuple(int)): Image shape of output format
        draw_type (DrawType): Enum for draw type
        line_heaviness (int, optional): Line heaviness. Defaults to 10.

    Returns:
        np.array: Output image given as np.array.
    """    

    if draw_type == DrawType.ADDITIVE:
        fill_value = 0
        line_heaviness = line_heaviness * (-1)
    else:
        fill_value = 255

    output_image = np.full(image_shape, fill_value, dtype=np.int16)

    for line_ in lines:
        p1, p2 = line_

        yy, xx = line(p1.y, p1.x, p2.y, p2.x)

        output_image[yy, xx] -= line_heaviness

    output_image = np.clip(output_image, 0, 255)
    output_image = output_image.astype(np.uint8)
    return output_image

def draw_line_svg(lines, width, height, draw_type, stroke_width=0.1):
    """Draw lines into SVG drawing given a list of lines.

    Parameters
    ----------
        lines (list): List of point pairs
        width (int): Width of SVG document
        heigh (int): Height of SVG document
        draw_type (DrawType): Enum for draw type
        stroke_width (float, optional): Stroke width of lines. Defaults to 0.1

    Returns
    -------
        svg_drawing: Output SVG as drawSvg Drawing.
    """

    if draw_type == DrawType.ADDITIVE:
        stroke_color = 'white'
        background = 'black'
    else:
        stroke_color = 'black'
        background = 'white'

    svg_drawing = draw.Drawing(width, height, origin=(0, -height),
                displayInline=False,
                stroke=stroke_color,
                stroke_width=stroke_width)

    if draw_type == DrawType.ADDITIVE:
        svg_drawing.append(draw.Rectangle(0, -height, width, height,
            stroke='none',
            fill=background))

    for line_ in lines:
        p1, p2 = line_

        svg_drawing.append(draw.Line(p1.x, p1.y*-1, p2.x, p2.y*-1))

    return svg_drawing

def compute_image_lines(image, num_lines, num_lines_to_check, draw_type, line_heaviness=10):
    """Computes lines needed to redraw line image.

    Args:
        image (np.array): Image as numpy array.
        num_lines (int): Number of lines to draw.
        num_lines_to_check (int): Number of tries to find best line.
        draw_type (DrawType): Enum for draw type.
        line_heaviness (int, optional): Line heaviness. Defaults to 10.

    Returns:
        list(): List of point pairs
    """    
    list_of_lines = []
    debug_ = False

    for i in tqdm(range(num_lines), desc='Calculating line: '):
        # For additive draw_type find brightest point and for subtractive mode
        # search darkest point.
        if draw_type == DrawType.ADDITIVE:
            value_to_search = np.max(image)
        else:
            value_to_search = np.min(image)

        (indexes_y, indexes_x) = np.where(value_to_search == image)

        # Pick randomly one of the brightest, or darkest points depending on draw_type.
        number_of_target_pixel = indexes_x.shape[0]
        random_index = np.random.randint(0, number_of_target_pixel)

        # y-axis value is inverted because geometry library uses inverted y-axis direction.
        selected_point = Point(
            indexes_x[random_index], - indexes_y[random_index])

        if debug_:
            # Prepare white image to create
            debug_image = np.full(image.shape + (3,), 255, dtype=np.uint8)
        else:
            debug_image = None

        # Find best fitting line in current test round
        best_line, best_mean_value = find_best_line_through_point(
            num_lines_to_check, selected_point, image, debug_image, draw_type)

        if debug_:
            # Draw red point for random point.
            debug_image[indexes_y[random_index]-2:indexes_y[random_index]+2,
                        indexes_x[random_index]-2:indexes_x[random_index]+2] = [255, 0, 0]
            output_image = Image.fromarray(debug_image)
            output_image.save('./debug_output/debug_point_{}.png'.format(i))

            # print current input image state.
            output_image = Image.fromarray(image)
            output_image.save('./debug_output/debug_output.png')

        # Accumulate already drawn line to original image.
        yy, xx = line(best_line[0].y, best_line[0].x,
                      best_line[1].y, best_line[1].x)
        if draw_type == DrawType.ADDITIVE:
            image[yy, xx] -= line_heaviness
        else:
            image[yy, xx] += line_heaviness

        list_of_lines.append(best_line)
    return list_of_lines


def find_best_line_through_point(num_lines_to_check, selected_point, image, debug_image, draw_type):
    """Find best line through a given point.

    Args:
        num_lines_to_check (int): Number of tries to find best line.
        selected_point (Point): Point where line needs to go through.
        image (np.array): Image as np.array.
        debug_image (np.array): Debug_image when needed. Other value is set to None.
        draw_type (DrawType): Enum for draw type.

    Returns:
        (Point,Point): Point pair representing the best line segment.
    """    
    if draw_type == DrawType.ADDITIVE:
        best_mean_value = -sys.float_info.max
    else:
        best_mean_value = sys.float_info.max

    best_line = (Point(-9.9, -9.9), Point(-9.9, -9.9))
    (image_height, image_width) = image.shape

    for j in range(num_lines_to_check):
        angle = (np.random.rand() - 0.5) * np.pi
        direction = Point(np.cos(angle), np.sin(angle))
        line_through_point = Line(selected_point, direction)

        # Rectangle representing the image boarders is mapped to the bottom left quadrant
        # due to the different coordinate system used in the numpy arrays.
        image_rectangle = Rectangle(
            image_width - 1.0, image_height - 1.0, Point(0.0, - image_height + 1.0))
        found_line = image_rectangle.intersection_with_line(line_through_point)

        if len(found_line) == 2:
            (p1, p2) = found_line
        else:
            # Forget point - because it was an edge case.
            continue

        # Remap y-coordinate system because y-axis direction is opposite in
        # numpy arrays and the geometric lib.
        p1.y = - p1.y
        p2.y = - p2.y

        (p1, p2) = (p1.as_PointInt(), p2.as_PointInt())
        yy, xx = line(int(p1.y), int(p1.x), int(p2.y), int(p2.x))

        mean_line_intensity = np.mean(image[yy, xx])

        # DEBUG: Check if lines are correctly drawn through random point.
        if debug_image is not None:
            print("point pos: ", selected_point)
            print("angle: ", angle/np.pi*180)
            print(p1, p2)
            debug_image[yy, xx] = [0, 0, 0]

            print("j {}, angle {}, direction {}, selected_point {}, best_mean_value {}".format(
                j, angle, direction, selected_point, best_mean_value))

        if draw_type == DrawType.ADDITIVE:
            if best_mean_value < mean_line_intensity:
                best_line = (p1, p2)
                best_mean_value = mean_line_intensity
        else:
            if best_mean_value > mean_line_intensity:
                best_line = (p1, p2)
                best_mean_value = mean_line_intensity

    return best_line, best_mean_value

def print_input_params(args):
    print("\n----------------------------------------------\n")
    print("-- Input parameters --")
    print("draw_type=: ", args.draw_type)
    print("input_path: ", args.input_path)
    print("output_path: ", args.output_path)
    print("output_format: ", args.output_format)
    print("num_lines: ", args.num_lines)
    print("num_lines_to_check: ", args.num_lines_to_check)
    print("\n----------------------------------------------\n")


def main(args):
    print(LOGO)
    print_input_params(args)

    # Initialize random-seed of numpy framework to always get the same output
    # if no_random_result is set.
    if args.no_random_result == True:
        np.random.seed(42)
        print("No random result setting activated.")

    # Prepare draw_type enum to remove string comparisson.
    if str.upper(args.draw_type) == 'ADDITIVE':
        draw_type = DrawType['ADDITIVE']
    elif str.upper(args.draw_type) == 'SUBTRACTIVE':
        draw_type = DrawType['SUBTRACTIVE']
    else:
        print("Error: draw_type <{}> not supported".format(args.draw_type))
        sys.exit()

    print('Load and preprocess image...')
    img = Image.open(args.input_path)

    # Resize if wanted.
    if args.output_width > 0:
        basewidth = args.output_width
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)

    # grayscale using CIE luminance (Copied from http://linify.me)
    img_arr = np.asarray(img, dtype=float)
    img_arr = 0.21 * img_arr[:, :, 0] + 0.72 * \
        img_arr[:, :, 1] + 0.07 * img_arr[:, :, 2]
    img_arr = img_arr.astype(np.int16)

    lines = compute_image_lines(
        img_arr, args.num_lines, args.num_lines_to_check, draw_type, args.line_heaviness)
    
    if args.output_format == 'SVG':

        svg_width = img.width
        svg_height = img.height

        output_svg = draw_line_svg(
            lines, svg_width, svg_height, draw_type, args.stroke_width)
        print('Write SVG to {}'.format(args.output_path))
        output_svg.saveSvg(args.output_path)
    else:
        output_image_arr = draw_line_image(
            lines, img_arr.shape, draw_type, args.line_heaviness)
        # Write image to output
        print('Write image to {}'.format(args.output_path))
        output_image = Image.fromarray(output_image_arr)
        output_image.save(args.output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='line_drawer - Redraws image only with straight lines.')

    parser.add_argument('--input-path', type=str,
                        default='./example/mani_matter.png', help='Input image path.')
    parser.add_argument('--output-path', type=str,
                        default='./output.png', help='Output image path.')
    parser.add_argument('--num-lines', type=int, default=10000,
                        help='Number of lines to draw.')
    parser.add_argument('--line-heaviness', type=int, default=10,
                        help='Line heaviness. Integer from 1 to 255, with 255 being completely heavy.')
    parser.add_argument('--num-lines-to-check', type=int, default=10,
                        help='Number of lines to check at each iteration.')
    parser.add_argument('--draw-type', type=str, default='subtractive',
                        help='Draw types (subtractive/additive). Subtractive means white background with black lines. Additive means black background with white lines.')
    parser.add_argument('--no-random-result', action='store_true',
                        help='Will return always the same output with the same config if set.')
    parser.add_argument('--output-width', type=int, default=512,
                        help='Output image width in pixels where hight will be adapted. Smaller width reduses computation time. "-1" will not change the size.')
    parser.add_argument('--output-format', type=str.upper, default='PNG', choices=['PNG', 'SVG'],
                        help='Output image format - SVG or PNG')
    parser.add_argument('--stroke-width', type=float, default=0.1,
                        help='SVG stroke width')

    args = parser.parse_args()

    main(args)

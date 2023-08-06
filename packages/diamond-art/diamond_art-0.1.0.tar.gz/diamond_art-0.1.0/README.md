[![PyPi Release](https://img.shields.io/pypi/v/diamond_art.svg)](https://pypi.python.org/pypi/diamond_art)

# Diamond Art
## What is diamond art?

Diamond art is a way of creating textured images by attaching small plastic gems to a
canvas. The gems are facetted such that they reflect light, giving the finished product
a glitzy look.

Kits are typically sold with a pre-printed canvas covered by a grid of symbols under a
layer of double-stick tape. The symbols indicate which color diamond to adhere. Large
artworks may require adhering thousands of diamonds in dozens of colors.

## Installation

The tool can be installed from pypi. It requires python 3.7 or newer.

    pip install diamond-art

Alternately, source can be downloaded from [github](https://github.com/sbliven/diamond-art)
and installed with

    python setup.py install

## Usage

First create your image. My 6 year old son created this image of a house using a pixel
editor (scaled up for visibility).

![Pixel image of a house](examples/house_6yo_big.png)

This can be converted to a diamond painting using the command line tool:

    diamond_art examples/house_6yo.png examples/house_6yo_canvas.png

which produces this:

![Diamond art template of a house](examples/house_6yo_canvas.png)

When printed at 100% scale (approximately 300 dpi by default) the resulting canvas will
fit 2.5mm gems perfectly.

## License

Diamond-art is released under the BSD license.

## Credits

* Created by Spencer Bliven
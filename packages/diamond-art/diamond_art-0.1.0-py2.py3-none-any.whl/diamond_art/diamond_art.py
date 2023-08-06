"""Main module."""
from importlib import resources
from typing import Dict, Tuple

import numpy as np  # type: ignore
from PIL import Image, ImageDraw, ImageFont  # type: ignore

from .data.fonts import Noto_Sans_Symbols


class SymbolError(IndexError):
    pass


class DiamondArt:
    original: Image
    scale: int  # pixels per grid
    dpi: float  # output resolution, in dots/inch
    gem_size: float  # gem dimensions, in mm
    _symbols: Dict[int, Tuple[str, ImageFont.ImageFont]]

    def __init__(self, filename, gem_size=2.5, target_dpi=300):
        self.original = Image.open(filename).convert("P")
        self.gem_size = gem_size
        self.set_dpi(target_dpi)
        self._symbols = None

    def get_image(self) -> Image:
        # scale up
        big = self.original.convert("RGB").resize(
            np.dot(self.original.size, self.scale).astype(np.uint), Image.NEAREST
        )

        # fade out
        white = Image.new("RGBA", big.size, color=(255, 255, 255, 128))
        big.paste(white, (0, 0), white)

        # add grid
        draw = ImageDraw.Draw(big)
        for x in range(0, big.size[0], self.scale):
            draw.line((x, 0, x, big.size[1]), fill=(0, 0, 0, 255))
        for y in range(0, big.size[1], self.scale):
            draw.line((0, y, big.size[0], y), fill=(0, 0, 0, 255))

        # add symbols
        imdata = np.asarray(self.original)
        symbols = self.get_symbols()
        for x in range(self.original.size[0]):
            for y in range(self.original.size[1]):
                sym, font = symbols[imdata[y, x]]
                draw.text(
                    np.array([x, y]) * self.scale + 1 + (self.scale - 1) / 2,
                    sym,
                    font=font,
                    anchor="mm",
                    fill=(0, 0, 0, 255),
                )

        return big

    def save(self, filename):
        self.get_image().save(filename, dpi=(self.dpi, self.dpi))

    def set_dpi(self, target_dpi):
        self.scale = round(target_dpi / 25.4 * self.gem_size)  # px/grid
        self.dpi = self.scale * 25.4 / self.gem_size

    def get_symbols(self):
        if self._symbols is None:
            with resources.path(
                Noto_Sans_Symbols, "NotoSansSymbols-Regular.ttf"
            ) as fontpath:
                # Choose font size such that ascender+descender will fit in a box
                font_size = (self.scale - 1) * 3 // 4
                font = ImageFont.truetype(str(fontpath), font_size, encoding="unic")
                symbol_list = "🜁🝪🜶🜷🝅⚓♈⚛⚑♋⛴"
                # symbol_list = "●★✖❤✝✈☂⚓"
                if len(symbol_list) < len(self.original.getcolors()):
                    raise SymbolError(
                        f"Too many colors (max {len(symbol_list)} colors)"
                    )
                self._symbols = {
                    col: (sym, font)
                    for (n, col), sym in zip(self.original.getcolors(), symbol_list)
                }
        return self._symbols

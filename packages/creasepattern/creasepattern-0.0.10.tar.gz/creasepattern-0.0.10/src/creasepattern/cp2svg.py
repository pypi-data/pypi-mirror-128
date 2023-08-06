from .from_cp import from_cp
from .to_svg import to_svg


def cp2svg(infile: str, outfile: str, margin=10) -> None:
    cp = from_cp(infile)

    svg_string = to_svg(cp, margin)

    with open(outfile, 'w') as im:
        im.write(svg_string)

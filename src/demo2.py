from phue import Bridge
from scrape_colors import make_map
from rgbxy import Converter
import name_converter


def go():
    color_map = make_map('wikipedia_pages/colors.html')

    #Test Comment in demo2 file
    test = "."

    b = Bridge('172.31.229.35')

    b.connect()

    entry = b.lights[0]

    while (test != ""):
        test = input("Please enter a color: ")
        test = name_converter.NameConverter.convert(name_converter.NameConverter, test)
        print(test)
        if test == "Black":
            entry.on = False
        else:
            if not entry.on:
                entry.on = True
            rgb_color = color_map[test]
            print(rgb_color)
            r = rgb_color['r']
            g = rgb_color['g']
            b = rgb_color['b']
            converter = Converter()
            [x, y] = converter.rgb_to_xy(r, g, b)
            print(x, y)
            entry.xy = (x, y)


# b = Bridge('10.0.1.2')
if __name__ == '__main__':
    go()

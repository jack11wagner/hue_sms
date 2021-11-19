from thefuzz import fuzz, process
import pandas as pd

colors_list = pd.read_csv('colors.csv', names=['Color', 'R', 'G', 'B'])


def getFuzzyColor(color_name):
    # we want a 85% match for thefuzz
    fuzzyMatch = process.extractOne(color_name.title(), colors_list['Color'], scorer=fuzz.token_sort_ratio)
    fuzz_color, percent_match = fuzzyMatch[0], fuzzyMatch[1]
    if percent_match >= 85:
        return fuzz_color
    else:
        return None

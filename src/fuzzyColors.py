from thefuzz import fuzz, process
import redis

redis = redis.Redis(host='localhost', port=6379, db=0)
colors_list = []
for color in redis.hgetall('color_totals').keys():
    color = color.decode('utf-8')
    colors_list.append(color)


def getFuzzyColor(color_name):
    # we want a 85% match for thefuzz
    fuzzyMatch = process.extractOne(color_name.title(), colors_list, scorer=fuzz.token_sort_ratio)
    fuzz_color, percent_match = fuzzyMatch[0], fuzzyMatch[1]
    if percent_match >= 85:
        return fuzz_color
    else:
        return None

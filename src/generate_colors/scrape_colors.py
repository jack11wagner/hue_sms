
from bs4 import BeautifulSoup


def make_map(file_path):
    color_map = {}

    with open(file_path) as f:

        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')

    # the first table contains the standard colors
    table = soup.find('table')
    rows = table.find_all('tr')

    for row in rows:
        fields = row.find_all('td')

        # The table has a <th> row
        if len(fields) == 0:
            continue

        [color, h, s, v, r, g, b] = fields[0:7]

        color_map[color.get_text().strip()] = {'r': int(r.get_text()), 'g': int(g.get_text()), 'b': int(b.get_text())}

    return color_map


def make_file():
    with open('wikipedia_pages/colors.html') as f:

        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')

    # the first table contains the standard colors
    table = soup.find('table')
    rows = table.find_all('tr')

    with open('colors.csv', 'w') as out:

        for row in rows:
            fields = row.find_all('td')

            # The table has a <th> row
            if len(fields) == 0:
                continue

            [color, h, s, v, r, g, b] = fields[0:7]

            out.write('{},{},{},{}\n'.format(color.get_text().strip(),
                                                int(r.get_text()),
                                                int(g.get_text()),
                                                int(b.get_text())))


if __name__ == '__main__':
    make_file()



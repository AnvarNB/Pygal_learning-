import csv
import pygal
from pygal.style import LightGreenStyle
from py_lessons.Self_learn.matiz.visualis_data.jsons.country_codes\
    import get_country_code


def view_data(filename, forests_data):
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:
            country_name = row[0]
            code_key = get_country_code(country_name)
            forest_value = row[59]
            try:
                forest_value = round(float(forest_value))
            except ValueError:
                forest_value = 0.0
            if code_key:
                forests_data[code_key] = forest_value
            else:
                print(f"ERROR, no name_country such as {country_name}")


filename = 'API_AG.LND.FRST.K2_DS2_en_csv_v2_48255.csv'

forests_data = {}
view_data(filename, forests_data)
# print(forests_data)

# Группировка стран по 3-м уровням количества лесов:
cc_forests_1, cc_forests_2, cc_forests_3 = {}, {}, {}

for cc, forest in forests_data.items():
    if forest < 100000:
        cc_forests_1[cc] = forest
    elif forest < 1000000:
        cc_forests_2[cc] = forest
    else:
        cc_forests_3[cc] = forest

# Cheking forests in levels:
# print(len(cc_forests_1), len(cc_forests_2), len(cc_forests_3))

wm_style = LightGreenStyle()
wm = pygal.maps.world.World(style=wm_style)
wm.title = 'Forest area in 2015, by country'
wm.add('0-100000 sq.km', cc_forests_1)
wm.add('100000-1m sq.km', cc_forests_2)
wm.add('>1m sq.km', cc_forests_3)
wm.render_to_file('forest_area.svg')

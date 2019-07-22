import fileinput
import os
import re
import shutil
import sys
import time
import winsound


PROJECT_NAME = 'diva-redux'
RELEASE = False

NOW = time.strftime('%Y-%m%d-%H%M')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
ZIP_NAME = '%s-%s' % (PROJECT_NAME, NOW)

BUILD_PATH = os.path.join(BASE_DIR, 'build')
REDUX_PATH = os.path.join(BUILD_PATH, 'Redux')
SCRIPTS_PATH = os.path.join(REDUX_PATH, 'Scripts')
SCHEMES_PATH = os.path.join(BASE_DIR, 'color_schemes')

color_schemes = []


for root, _, files in os.walk(SCHEMES_PATH):
    for filename in files:
        full_path = os.path.join(root, filename)
        color_schemes.append(full_path)


for scheme in color_schemes:
    with open(scheme, 'r') as f:
        color_scheme = f.read()


config = {'label_font': 'RopaSans-Italic',
         'label_font_size': '12.00',
         'label_small_font': 'Viga-Regular',
         'label_small_font_size': '10.00',
         'display_font': 'RopaSans-Italic',
         'display_font_size': '13.00',
         'button_font': 'RopaSans-Italic',
         'button_font_size': '13.00',
         'slider_head_size': '2.00',
         'slider_sensitivity': '0.20',
         'redux_color_scheme': color_scheme,
         }

garbage = ['(?!#FX.)[#].*', '^[ \t]+', '[ \t]+$', '  +', '^\n']


def main():
    try:
        shutil.rmtree(REDUX_PATH)
    except Exception as e:
        print(e)

    try:
        os.makedirs(REDUX_PATH)
    except Exception as e:
        print(e)
    finally:
        shutil.copytree(os.path.join(BASE_DIR, 'scripts'), SCRIPTS_PATH)

    scripts = []

    for root, _, files in os.walk(SCRIPTS_PATH):
        for filename in files:
            full_path = os.path.join(root, filename)
            scripts.append(full_path)

    for line in fileinput.FileInput(scripts, inplace=1):
        for i, _ in enumerate(garbage):
            line = re.sub(garbage[i], '', line)

        for key in config:
            regex_string = r'\b(%s)\b' % key
            line = re.sub(regex_string, config[key], line)

        print(line, end='')

    if RELEASE:
        shutil.make_archive(os.path.join(BASE_DIR, ZIP_NAME), 'zip', BUILD_PATH)

    winsound.Beep(2000, 100)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        RELEASE = True
    main()

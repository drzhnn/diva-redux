import fileinput
import os
import re
import shutil
import sys
import time
import winsound


PROJECT_NAME = 'diva-redux'
RELEASE = False

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
NOW = time.strftime('%Y-%m%d-%H%M')
ZIP_NAME = '%s-%s' % (PROJECT_NAME, NOW)

THEMES = {
          'Redux': f'{BASE_DIR}/color_schemes/default.txt',
          'Redux Gray': f'{BASE_DIR}/color_schemes/gray.txt',
          # 'Redux White': f'{BASE_DIR}/color_schemes/white.txt',
          'Redux Black': f'{BASE_DIR}/color_schemes/black.txt'
          }


for theme in THEMES:
    try:
        shutil.rmtree(f'{BASE_DIR}/build/{theme}')
    except Exception as e:
        print(e)


for theme in THEMES:
    try:
        os.makedirs(f'{BASE_DIR}/build/{theme}')
    except Exception as e:
        print(e)
    finally:
        shutil.copytree(f'{BASE_DIR}/scripts', f'{BASE_DIR}/build/{theme}/Scripts')


for theme in THEMES:
    with open(THEMES[theme], 'r') as f:
        color_scheme = f.read()

    config = {'redux_color_scheme': color_scheme,
              'label_font': 'RopaSans-Italic',
              'label_font_size': '12.00',
              'label_small_font': 'Viga-Regular',
              'label_small_font_size': '10.00',
              'display_font': 'RopaSans-Italic',
              'display_font_size': '13.00',
              'button_font': 'RopaSans-Italic',
              'button_font_size': '13.00',
              'slider_head_size': '2.00',
              'slider_sensitivity': '0.20'}

    garbage = ['(?!#FX.)[#].*', '^[ \t]+', '[ \t]+$', '  +', '^\n']

    scripts = []

    for root, _, files in os.walk(f'{BASE_DIR}/build/{theme}/Scripts'):
        for filename in files:
            full_path = os.path.join(root, filename)
            scripts.append(full_path)

    for line in fileinput.FileInput(scripts, inplace=1):
        for key in config:
            regex_string = r'\b(%s)\b' % key
            line = re.sub(regex_string, config[key], line)

        for i, _ in enumerate(garbage):
            line = re.sub(garbage[i], '', line)

        print(line, end='')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        RELEASE = True
        shutil.make_archive(f'{BASE_DIR}/{ZIP_NAME}', 'zip', f'{BASE_DIR}/build')

    winsound.Beep(2000, 100)

import fileinput
import os
import re
import shutil
import sys
import time
import winsound


project_name = 'diva-redux'
release = False

now = time.strftime('%Y-%m%d-%H%M')
base_dir = os.path.dirname(os.path.realpath(__file__))
zip_name = '%s-%s' % (project_name, now)

build_path = os.path.join(base_dir, 'build')
redux_path = os.path.join(build_path, 'Redux')
scripts_path = os.path.join(redux_path, 'Scripts')

variables = {'label_font': 'RopaSans-Italic',
             'label_font_size': '12.00',
             'label_small_font': 'Viga-Regular',
             'label_small_font_size': '10.00',
             'display_font': 'RopaSans-Italic',
             'display_font_size': '13.00',
             'button_font': 'RopaSans-Italic',
             'button_font_size': '13.00',
             'slider_head_size': '2.00',
             'slider_sensitivity': '0.20'
             }

garbage = ['(?!#FX.)[#].*', '^[ \t]+', '[ \t]+$', '  +', '^\n']


def main():
    try:
        shutil.rmtree(redux_path)
    except Exception as e:
        print(e)

    try:
        os.makedirs(redux_path)
    except Exception as e:
        print(e)
    finally:
        shutil.copytree(os.path.join(base_dir, 'scripts'), scripts_path)

    scripts = []

    for root, _, files in os.walk(scripts_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            scripts.append(full_path)

    for line in fileinput.FileInput(scripts, inplace=1):
        for i, _ in enumerate(garbage):
            line = re.sub(garbage[i], '', line)

        for key in variables:
            regex_string = r'\b(%s)\b' % key
            line = re.sub(regex_string, variables[key], line)

        print(line, end='')

    if release:
        shutil.make_archive(os.path.join(base_dir, zip_name), 'zip', build_path)

    winsound.Beep(2000, 100)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        release = True
    main()

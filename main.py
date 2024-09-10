import os
import json
from args import parse_cmd_args


def main():
    SETTINGS_FILE = 'settings.json'

    if os.path.isfile(SETTINGS_FILE):
        settings = json.load(open(SETTINGS_FILE, 'r', encoding='utf-8'))
    else:
        settings = {'projects': {}}
        json.dump(settings, open(SETTINGS_FILE, 'w', encoding='utf-8'), indent=4)

    parse_cmd_args()


if __name__ == "__main__":
    main()

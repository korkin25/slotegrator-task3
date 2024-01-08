#!/usr/bin/env python3
import yaml
import pprint
import json
from pygments import highlight, lexers, formatters

def main(config_path='config.yaml'):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    json_config = json.dumps(config, indent=4, sort_keys=True)
    colorful_json = highlight(
        json_config,
        lexers.JsonLexer(),
        formatters.TerminalFormatter()
    )
    print(colorful_json)

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    main(*args)


import os
import sys
from flask import Flask, request, render_template
import yaml
import logging

app = Flask(__name__)

if len(sys.argv) < 2:
    sys.exit("Usage: python app.py <config_path>")

config_path = sys.argv[1]

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

log_file = config['log_file']
log_format = '%(asctime)s %(message)s'
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.template_folder = config['template_dir']

def read_last_lines(file_path, num_lines):
    with open(file_path, 'r') as file:
        return file.readlines()[-num_lines:]

@app.route('/', methods=['GET'])
def show_data():
    headers = request.headers
    headers_list = [(k, v) for k, v in headers.items()]
    app.logger.info(' '.join([f'{k} {v}' for k, v in headers.items()]))

    log_lines = read_last_lines(log_file, 10)
    return render_template('headers.html', headers_list=headers_list, log_lines=log_lines)

if __name__ == '__main__':
    app.run(port=config['port'], debug=True, use_reloader=False, extra_files=[config_path])

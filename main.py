import argparse
import json
from os import listdir
from os.path import abspath, join
from classes import jekyll_parser as jp
from classes import wordpress_handler as wph

with open("config.json") as json_data_file:
    config = json.load(json_data_file)


parser = argparse.ArgumentParser(description='Process a directory of Jekyll Markdown posts and create them in a WordPress instance')
parser.add_argument('--directory', help='the directory with all the posts')
args = parser.parse_args()


files = [abspath(join(args.directory, f)) for f in listdir(args.directory)]
for i, file in enumerate(files):
    read_file = open(file, 'r')
    content = read_file.read()
    handler = wph.WordpressHandler(jp.JekyllParser(), config)
    handler.post_to_wordpress(content)


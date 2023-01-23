import argparse
import json
from os import listdir
from os.path import abspath, join
from classes import jekyll_parser as jp
from classes import wordpress_handler as wph

# Load configuration file
with open("config.json") as json_data_file:
    config = json.load(json_data_file)


# Set up command line arguments
parser = argparse.ArgumentParser(description='Process a Jekyll Markdown file or directory of Jekyll Markdown posts and create them in a WordPress instance')
parser.add_argument('--file', help='The absolute path of a single post file')
parser.add_argument('--directory', help='The absolute path of the directory with all the posts')
args = parser.parse_args()

# Global Wordpress Handler
handler = wph.WordpressHandler(jp.JekyllParser(), config)

if (args.file):
    handler.post_to_wordpress_from_file(args.file)
elif (args.directory):
    # Post file content to wordpress
    files = [abspath(join(args.directory, f)) for f in listdir(args.directory)]
    for i, file in enumerate(files):
        handler.post_to_wordpress_from_file(file)


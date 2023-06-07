from abc import ABC, abstractmethod
from classes import wordpress_api as wpa
import requests
 
class Handler(ABC):

    def __init__(self, parser):
        self.parser = parser

    @abstractmethod
    def post_to_wordpress(self, content):
        pass

class WordpressHandler(Handler):
    def __init__(self, parser, config):
        super().__init__(parser)
        self.api = wpa.WordPressAPI(config)
    
    # This function only works if there is a slug in the frontmatter
    # TODO: handle missing data parameters: categories and tags
    def post_to_wordpress(self, content, pubDate=None, post_type=None):
        metadata, html_content = self.parser.parse(content)
        self.api.create_post(metadata, html_content, pubDate, post_type)
       
    def post_to_wordpress_from_file(self, file, post_type=None):
        read_file = open(file, 'r')
        content = read_file.read()
        pubDate = self.parser.parse_date_from_filename(file)
        self.post_to_wordpress(content, pubDate, post_type)
        

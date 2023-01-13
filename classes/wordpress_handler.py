from abc import ABC, abstractmethod
import requests
import json

 
class Handler(ABC):

    def __init__(self, parser):
        self.parser = parser
 
    @abstractmethod
    def post_to_wordpress(self):
        pass

class WordpressHandler(Handler):
    def __init__(self, parser, config):
        super().__init__(parser)
        self.config = config
    
    # This function only works if there is a slug in the frontmatter
    # TODO: handle missing data parameters: slug, publication date, categories
    def post_to_wordpress(self, content):
        metadata, html_content = self.parser.parse(content)
        data = {
            "title": metadata["title"],
            "content": html_content,
            "status": "publish",
            "slug": metadata["slug"]
        }
        response = requests.post(url=self.config['wordpress_url'], 
                                 auth=(self.config['wordpress_auth_username'], self.config['wordpress_auth_password']), 
                                 json=data, 
                                 headers={'Content-Type': 'application/json'})
        print(response)
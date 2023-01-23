from abc import ABC, abstractmethod
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
        self.config = config
    
    # This function only works if there is a slug in the frontmatter
    # TODO: handle missing data parameters: categories and tags
    def post_to_wordpress(self, content, pubDate=None):
        metadata, html_content = self.parser.parse(content)
        data = {
            "title": metadata["title"],
            "content": html_content,
            "status": "publish",
            "slug": metadata["slug"]
            # TODO: programmatically handle assignment of
            #       categories and tags. Currently, the categories
            #       and tags are manually created in WordPress,
            #       and the user has to know which ID to use
            # "categories": [3],
            # "tags": [4]
        }

        if pubDate:
            data['date'] = pubDate

        response = requests.post(url=self.config['wordpress_url'], 
                                auth=(self.config['wordpress_auth_username'], self.config['wordpress_auth_password']), 
                                json=data, 
                                headers={'Content-Type': 'application/json'})

        if (response.status_code >= 200):
           print("{} was created in Wordpress".format(metadata["title"]))
       
    def post_to_wordpress_from_file(self, file):
        read_file = open(file, 'r')
        content = read_file.read()
        pubDate = self.parser.parse_date_from_filename(file)
        self.post_to_wordpress(content, pubDate)
        

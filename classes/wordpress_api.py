import requests

class WordPressAPI:
    def __init__(self, config):
        self.config = config

        # Cache categories and tags
        self.categories = self.get_categories()
        self.tags = self.get_tags()

    def get_categories(self):
        response = requests.get(url="{}/wp-json/wp/v2/categories".format(self.config['wordpress_url']),
                                auth=(self.config['wordpress_auth_username'], 
                                      self.config['wordpress_auth_password']))
        
        categories = {}
        for category in response.json():
            categories[category['slug']] = { 'id': category['id'], 'slug': category['slug'] }

        return categories

    def get_tags(self):
        response = requests.get(url="{}/wp-json/wp/v2/tags".format(self.config['wordpress_url']),
                                auth=(self.config['wordpress_auth_username'], 
                                      self.config['wordpress_auth_password']))
        tags = {}
        for tag in response.json():
            tags[tag['slug']] = { 'id': tag['id'], 'slug': tag['slug'] }

        return tags
    
    def create_category(self, name):
        data = {
            'name': name,
            'slug': name
        }
        response = requests.post(url="{}/wp-json/wp/v2/categories".format(self.config['wordpress_url']),
                                auth=(self.config['wordpress_auth_username'],
                                      self.config['wordpress_auth_password']),
                                json=data,
                                headers={'Content-Type': 'application/json'})
        json_data = response.json()
        self.categories[json_data['slug']] = { 'id': json_data['id'], 'slug': json_data['slug']}

    def create_post(self, metadata, html_content, pubDate):
        data = {
            "title": metadata["title"],
            "content": html_content,
            "status": "publish",
            "slug": metadata["slug"]
        }

        if pubDate:
            data['date'] = pubDate
            

        if "category" in metadata and metadata['category']:
            if metadata['category'] in self.categories:
                data['categories'] = [self.categories[metadata['category']]['id']]
            else:
                print("Creating new category: {}".format(metadata['category']))
                self.create_category(metadata['category'])

        if "tags" in metadata and metadata['tags']:
            if metadata['tags'] in self.tags:
                data['tags'] = [self.tags[metadata['tags']]['id']]
            else:
                raise NotImplementedError('Create new tag: {} for slug {}'.format(metadata['tags'], metadata['slug']))
        
        response = requests.post(url="{}/wp-json/wp/v2/posts".format(self.config['wordpress_url']),
                                auth=(self.config['wordpress_auth_username'],
                                      self.config['wordpress_auth_password']),
                                json=data,
                                headers={'Content-Type': 'application/json'})

        if (response.status_code >= 200):
           print("\"{}\" was created in Wordpress".format(metadata["title"]))
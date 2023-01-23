1. In WordPress Settings, set permalinks to post name.
2. Install the [Basic Auth Plugin](https://github.com/WP-API/Basic-Auth) to WordPress
2. Install the required packages: `pip3 install -r requirements.txt`
3. Copy `config.template.json` to `config.json` and fill in the details.

This tool does not handle:
- Checking for post existence. Therefore, multiple CLI calls
  with the same parameters will yield the multiple of the same
  posts.

from abc import ABC, abstractmethod
import frontmatter
import datetime
import markdown
 
class Parser(ABC):
 
    @abstractmethod
    def parse(self, content):
        pass

class JekyllParser(Parser):

    def parse(self, content):
        metadata, content = frontmatter.parse(content)
        html_content = markdown.markdown(content)
        return metadata, html_content

    def parse_date_from_filename(self, filename):
        if ("-" in filename):
            pubDateData = filename.split('/')[-1].split('-', 3) # This assumes that the filenames are in YYYY-MM-DD-title-string.md format
            pubDate = datetime.datetime(int(pubDateData[0]), int(pubDateData[1]), int(pubDateData[2]))
            return str(pubDate)
        return None


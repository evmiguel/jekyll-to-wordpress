from abc import ABC, abstractmethod
import frontmatter
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


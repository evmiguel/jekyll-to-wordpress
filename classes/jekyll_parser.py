from abc import ABC, abstractmethod
import frontmatter
 
class Parser(ABC):
 
    @abstractmethod
    def parse(self, content):
        pass

class JekyllParser(Parser):

    def parse(self, content):
        metadata, content = frontmatter.parse(content)
        return metadata, content


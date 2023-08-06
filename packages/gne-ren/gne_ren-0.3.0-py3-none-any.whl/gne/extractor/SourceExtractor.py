import re
from gne.utils import config
from lxml.html import HtmlElement
from ..defaults import SOURCE_PATTERN


class SourceExtractor:
    def __init__(self):
        self.source_pattern = SOURCE_PATTERN

    def extractor(self, element: HtmlElement, source_xpath=''):
        source_xpath = source_xpath or config.get('source', {}).get('xpath')
        if source_xpath:
            source = ''.join(element.xpath(source_xpath))
            return source
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.source_pattern:
            source_obj = re.search(pattern, text)
            if source_obj:
                return source_obj.group(1)
        return ''

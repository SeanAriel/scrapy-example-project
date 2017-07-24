import re


class TestPipeline(object):
    def process_item(self, item, spider):
        item['birth_date'] = re.findall('Born on (.*) at', item['birth_date'])[0]
        return item

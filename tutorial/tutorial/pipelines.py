# https://stackoverflow.com/questions/44481615/python-scrapy-renaming-downloaded-images

import os
from urllib.parse import urlparse

from scrapy.pipelines.files import FilesPipeline


class MyFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        return 'files/' + item['code'] + '_' + os.path.basename(urlparse(request.url).path + '.jpg')

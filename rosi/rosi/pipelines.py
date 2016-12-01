# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re
class RosiPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        #import pdb;pdb.set_trace()
        for image_url in item['image_urls']:
            if 'img1.mmxyz.net' not in image_url:
                continue
            else:
            	if '-150x150' in image_url:
            		image_url = re.sub('\-150x150','',image_url)
            		yield scrapy.Request(image_url.strip())

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

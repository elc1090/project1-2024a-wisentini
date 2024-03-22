from scrapy.pipelines.images import ImagesPipeline


class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["slug"]}.jpeg'

import scrapy
from scrapy.crawler import CrawlerProcess


class CateCourseSpider(scrapy.Spider):
    name = 'cate_course'

    def start_requests(self):
        yield scrapy.Request('https://shop.ccl.org/eu/leadership-programs')

    def parse(self, response):
        categories = response.css('div.pagebuilder-column')
        for category in categories:
            cate_name = category.css('h3::text').get()
            courses = category.css('p')
            for course in courses:
                course_name = course.css('a::text').get()
                course_url = course.css('a::attr(href)').get()
                course_info =  {
                    'name': course_name,
                    'url': course_url,
                    'category': [cate_name],
                    'category_url': [response.url],
                    'parent_url': response.url
                }
                yield course_info







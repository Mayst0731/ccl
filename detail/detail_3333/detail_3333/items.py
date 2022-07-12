# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Detail3333Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    category_tags = scrapy.Field()
    url = scrapy.Field()
    version = scrapy.Field()
    desc = scrapy.Field()
    active = scrapy.Field()
    priority = scrapy.Field()
    publish = scrapy.Field()
    is_advanced_management_program = scrapy.Field()
    schedule = scrapy.Field()
    type = scrapy.Field()
    location = scrapy.Field()
    currency = scrapy.Field()
    tuition_number = scrapy.Field()
    tuition_note = scrapy.Field()
    Repeatable = scrapy.Field()
    effective_date_start = scrapy.Field()
    effective_date_end = scrapy.Field()
    duration_days = scrapy.Field()
    duration_desc = scrapy.Field()
    duration_consecutive = scrapy.Field()
    languages = scrapy.Field()
    credential = scrapy.Field()
    course_takeaways = scrapy.Field()
    who_attend_desc = scrapy.Field()
    who_attend_params = scrapy.Field()
    exec_ed_inquiry_cc_emails = scrapy.Field()
    course_faculties = scrapy.Field()
    testimonials = scrapy.Field()
    overview = scrapy.Field()
    region = scrapy.Field()


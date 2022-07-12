import scrapy
import json
from ..items import Detail3333Item


class DetailSpider(scrapy.Spider):
    name = 'detail'
    handle_httpstatus_list = [404]

    def start_requests(self):
        start_url = 'https://shop.ccl.org/eu/leadership-programs'
        yield scrapy.Request(start_url, callback=self.parse_cates)

    def clean_cates(self, courses):
        course_dict = dict()
        for course in courses:
            course_name = course['name']
            if course_name not in course_dict:
                course_dict[course_name] = course
            else:
                course_dict[course_name]['category'] += course['category']
                course_dict[course_name]['url'] = course['url']

        return list(course_dict.values())

    def parse_cates(self, response):
        res_courses = []
        categories = response.css('div.pagebuilder-column')
        for category in categories:
            cate_name = category.css('h3::text').get()
            courses = category.css('p')
            for course in courses:
                course_name = course.css('a::text').get()
                course_url = course.css('a::attr(href)').get()
                course_info = {
                    'name': course_name,
                    'url': course_url,
                    'category': [cate_name],
                    'parent_url': response.url
                }
                res_courses.append(course_info)

        cleaned_courses = self.clean_cates(res_courses)
        count = 1
        for course_info in cleaned_courses:
            self.logger.info(f'{count} - {course_info["name"]} start')
            count += 1
            yield scrapy.Request(course_info['url'], callback=self.parse_detail, meta=course_info, dont_filter=True)

    def parse_detail(self, response):
        if response.status == 404:
            yield self.package_404_detail(response.meta)
        who_attend = ''
        try:
            who_attend = response.css('div#best-selling>div>p::text').get()
        except:
            pass
        desc = ''
        try:
            desc = response.xpath('//*[@id="maincontent"]//p/text()').get()
        except:
            pass
        try:
            desc_lis = response.xpath('//*[@id="maincontent"]//li/text()').getall()
            if desc_lis:
                lis_text = ''
                for li in desc_lis:
                    if '\n' not in li:
                        lis_text += ' * ' + li
                desc += lis_text
            other_ps = response.xpath('//*[@id="maincontent"]//p[2]/text()').get()
            if other_ps:
                desc += ' ' + other_ps
        except:
            pass

        america_link = response.xpath('//li[@data-label="Americas"]/a/@href').extract_first()
        europe_link = response.xpath('//li[@data-label="Europe, Middle East and Africa"]/a/@href').extract_first()
        asia_link = response.xpath('//li[@data-label="Asia-Pacific"]/a/@href').extract_first()
        region_links = [(america_link, "Americas"), (europe_link, "EMEA"), (asia_link, "APAC")]
        self.logger.info(f'region links: {response.meta["name"]} ----- \n {region_links}')
        for region_link, region_name in region_links:
            if region_link == "#":
                yield scrapy.Request(response.meta['url'],
                                     callback=self.parse_version_info,
                                     meta={
                                         'name': response.meta['name'],
                                         'desc': desc,
                                         'category': response.meta['category'],
                                         'url': response.url,
                                         'who_attend_desc': who_attend,
                                         'region': region_name
                                     },
                                     dont_filter=True)
            elif region_link != "#":
                yield scrapy.Request(region_link,
                                     callback=self.parse_version_info,
                                     meta={
                                         'name': response.meta['name'],
                                         'desc': desc,
                                         'category': response.meta['category'],
                                         'url': response.url,
                                         'who_attend_desc': who_attend,
                                         'region': region_name
                                     },
                                     dont_filter=True)

    def parse_version_info(self, response):
        if response.status != 404:
            location_set = set()
            table = response.css('table.events-table>tbody')
            msg_empty = response.xpath('//div[contains(text(),"We can\'t find products")]')
            if not msg_empty:
                trs = table.css('tr')
                for tr in trs:
                    tds = tr.css('td')
                    if tds:
                        location = tr.css('td.col.location>span::text').get()
                        if location not in location_set:
                            location_set.add(location)
                            detail = Detail3333Item()
                            detail['name'] = response.meta['name']
                            detail['url'] = response.url
                            detail['category'] = response.meta['category']
                            detail['desc'] = response.meta['desc']
                            dates = tr.css('td.date>span::text').get()
                            detail['languages'] = tr.css('td.language>span::text').get()
                            detail['currency'] = tr.css('td.cost>span::text').get()
                            detail['tuition_number'] = tr.css('td.cost>div>span>span::attr("data-price-amount")').get()
                            detail['location'] = location
                            detail['active'] = True
                            detail['effective_date_start'] = dates
                            detail['Repeatable'] = True
                            detail['who_attend_desc'] = response.meta['who_attend_desc']
                            detail['region'] = response.meta['region']
                            self.logger.info(detail)
                            yield detail

    def package_404_detail(self, response_meta):
        detail = Detail3333Item()
        detail['name'] = response_meta['name']
        detail['url'] = response_meta['url']
        detail['category'] = response_meta['category']
        detail['active'] = False
        detail['Repeatable'] = False
        detail['desc'] = ''
        detail['languages'] = ''
        detail['currency'] = 'USD'
        detail['tuition_number'] = 0
        detail['version'] = 1
        detail['location'] = ''
        return detail

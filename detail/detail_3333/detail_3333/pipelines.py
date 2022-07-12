# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
import re
from datetime import datetime


class Detail3333Pipeline:
    # file = '../../file_store/detail.json'
    def process_item(self, item, spider):
        item['url'] = self.format_url(item['url'])
        item.setdefault('testimonials', [])
        item.setdefault('priority', 0)
        item.setdefault('publish', 100)
        item.setdefault('tuition_note', '')
        item.setdefault('is_advanced_management_program', False)
        item.setdefault("credential", "")
        item.setdefault('course_faculties', [])
        item.setdefault('course_takeaways', '')
        item.setdefault('who_attend_params', {
            "working experience": "",
            "background knowledge": ""
        })
        item['desc'] = self.get_desc(item['desc'])
        item['effective_date_end'] = self.get_end_date(
            item.get('effective_date_start', ''))
        item['effective_date_start'] = self.get_start_date(
            item.get('effective_date_start', ''))

        item['overview'] = {
            'desc': item['desc'],
            'video_title': '',
            'video_url': ''}
        location = item["location"]
        duration_days = self.get_duration_days(
            item['effective_date_start'], item['effective_date_end'])
        if duration_days != '':
            item['duration_days'] = int(duration_days)
            item['schedule'] = [[item['effective_date_start'], item['effective_date_end'], str(duration_days),
                                 "formal"]]
        else:
            item['schedule'] = [[item['effective_date_start'], item['effective_date_end'], '',
                                 "formal"]]
        if item['name'] == "Leadership at the Peak" or item['name'] == "Leading for Organizational Impact":
            return item
        else:
            item['category'].append("Online Leadership Training")
            item['category'] = list(set(item['category']))
            return item

    def format_url(self, url):
        if url.endswith("\'"):
            url = url.replace("\'", '')
        return url

    def get_desc(self, desc):
        desc = desc.replace('\n', ' ')
        desc = re.sub(r'\s+', ' ', desc)
        desc = desc.strip()
        return desc

    def get_start_date(self, date_str):
        if not any(char.isdigit() for char in date_str):
            return ''
        else:
            months_map = {
                'Jan': '01',
                'Feb': '02',
                'Mar': '03',
                'Apr': '04',
                'May': '05',
                'Jun': '06',
                'Jul': '07',
                'Aug': '08',
                'Sep': '09',
                'Oct': '10',
                'Nov': '11',
                'Dec': '12'

            }

            date_lst = date_str.split(' ', 3)
            date = date_lst[0]
            month = months_map.get(date_lst[1])
            year = date_lst[2]
        return f'{year}-{month}-{date}'

    def get_end_date(self, date_str):
        if not any(char.isdigit() for char in date_str):
            return ''
        else:
            months_map = {
                'Jan': '01',
                'Feb': '02',
                'Mar': '03',
                'Apr': '04',
                'May': '05',
                'Jun': '06',
                'Jul': '07',
                'Aug': '08',
                'Sep': '09',
                'Oct': '10',
                'Nov': '11',
                'Dec': '12'

            }
        end_date = date_str.split('-')[1]
        end_date_str = end_date.strip()
        date_lst = end_date_str.split(' ', 3)
        date = date_lst[0]
        month = months_map.get(date_lst[1])
        year = date_lst[2]
        return f'{year}-{month}-{date}'

    def get_duration_days(self, start_date, end_date):
        if not start_date or not end_date:
            return ''
        date_format = "%Y-%m-%d"
        a = datetime.strptime(start_date, date_format)
        b = datetime.strptime(end_date, date_format)
        delta = b - a
        return delta.days

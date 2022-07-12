import collections
import json
from datetime import datetime
from pprint import pprint
from datetime import date
import requests
from bs4 import BeautifulSoup


def get_schedule_by_urls(urls):
    url_schedule_map = collections.defaultdict(list)
    for url in urls:
        # get current all schedules first
        schedules, next_url = [], url
        while next_url:
            soup = BeautifulSoup(requests.get(next_url).content)
            cur_schedules, next_url = get_schedules_and_next_url(soup)
            schedules += cur_schedules
        url_schedule_map[url] = schedules
        pprint(len(schedules))
    return url_schedule_map


def get_schedules_and_next_url(soup):
    schedules = []
    sessions = soup.select('td.col.date')
    locations = soup.select('td.col.location')
    for i, session in enumerate(sessions):
        date_str = session.text
        location_str = locations[i].find("span").text
        print(date_str)
        start_date = get_start_date(date_str)
        end_date = get_end_date(date_str)
        duration = get_duration_days(start_date, end_date)
        # location_session = session.findNext('td')
        # location = location_session.find('span').text
        schedule = [start_date, end_date, str(
            duration), 'formal', location_str]
        schedules.append(schedule)
        print(schedules)
    next_url = ''
    try:
        next_links = soup.select("a.action.next")
        next_url = [link.get('href') for link in next_links][0]
        print(next_url)
    except:
        print('no next page')
    return schedules, next_url


def get_duration_days(start_date, end_date):
    if not start_date or not end_date:
        return ''
    date_format = "%Y-%m-%d"
    # if "None" not in start_date and "None" not in end_date:
    a = datetime.strptime(start_date, date_format)
    b = datetime.strptime(end_date, date_format)
    delta = b - a
    # else:
    #     return 0
    return delta.days


def get_start_date(date_str):
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
        date = date_lst[0].strip()
        month = months_map.get(date_lst[1])
        year = date_lst[2]
    return f'{year}-{month}-{date}'


def get_end_date(date_str):
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


def extract_all_urls(file_path):
    with open(file_path, 'r') as f:
        details = json.load(f)
    urls = []
    for detail in details:
        print(detail["name"], detail["url"])
        urls.append(detail['url'])
    return urls


def no_repeating_urls(urls):
    res = set()
    for url in urls:
        if url not in res:
            res.add(url)
    return list(res)


def name_url_location():
    with open('./file_store/detail_3333_CCL_XW_1130.json', 'r') as f:
        details = json.load(f)
    for detail in details:
        print(detail['name'], detail['url'], detail['type'],
              detail['location'], len(detail["schedule"]))


def filter_schedules():
    today_date = date.today()
    today = today_date.strftime("%m%d")
    with open(f'./file_store/detail_3333_CCL_XW_{today}.json', 'r') as f:
        details = json.load(f)
    print(len(details))
    new_details = []
    for detail in details:
        schedules = detail["schedule"]
        typ = detail["type"]
        new_schedules = []
        real_location = detail["location"][0]
        for s in schedules:
            schedule_loc = s[-1]
            if typ.startswith("online") and ("Online" in schedule_loc or schedule_loc == "Self-Directed" or schedule_loc == "Virtual"):
                new_schedules.append(s)
            else:
                schedule_city = schedule_loc.split(",")[0]
                real_city = real_location.split(",")[0]
                if schedule_city.lower() == real_city.lower():
                    new_schedules.append(s)
        detail["schedule"] = new_schedules
        new_details.append(detail)
    delete_empty_schedules_new_details = []
    for d in new_details:
        if len(d["schedule"]) == 0:
            continue
        else:
            for s in d["schedule"]:
                s.pop()
            delete_empty_schedules_new_details.append(d)
    with open('./file_store/test_schedules.json', 'w') as fp:
        json.dump(new_details, fp, indent=4)

    with open('./file_store/detail_3333_CCL_XW_{today}_final.json', 'w') as fp:
        json.dump(delete_empty_schedules_new_details, fp, indent=4)


# filter_schedules()

# name_url_location()
# urls = ["https://shop.ccl.org/usa/leadership-programs/mid-level-leaders/leadership-development-program?category_id=285&store_id=1"]
# get_schedule_by_urls(urls)

import collections
import copy
import json
from datetime import date
from pprint import pprint

from test import extract_all_urls, get_schedule_by_urls, no_repeating_urls, filter_schedules


def read_json():
    with open('./file_store/detail_1.json', 'r') as f:
        details = json.load(f)
    return details


def write_json(details, path):
    with open(path, 'w') as fp:
        json.dump(details, fp, indent=4)


def add_version(details):
    new_details = []
    name_version_dict = dict()
    for detail in details:
        name = detail.get('name')
        if name not in name_version_dict:
            name_version_dict[name] = 1
        else:
            name_version_dict[name] += 1
        detail['version'] = name_version_dict[name]
        new_details.append(detail)
    return new_details


def figure_out_type(details):
    new_details = []
    for detail in details:
        location = detail.get('location', '')
        if location == 'Self-Directed':
            detail['type'] = "online-selfpaced"
        elif location == "Virtual":
            detail['type'] = "online-virtual"
        elif location == "Live Online":
            detail['type'] = 'online-virtual'
        elif location == "Moderated Online":
            detail['type'] = 'online-selfpaced'
        else:
            detail['type'] = 'onsite'
        new_details.append(detail)
    return new_details


def get_same_course_other_locations(details):
    name_loc_dict = collections.defaultdict(list)
    for detail in details:
        name = detail.get("name")
        location = detail.get("location")
        region = detail.get('region')
        if name not in name_loc_dict:
            name_loc_dict[name] = [f"{region} - {location}"]
        else:
            name_loc_dict[name].append(f"{region} - {location}")
    new_details = []
    for detail in details:
        detail["other_locations"] = name_loc_dict[detail["name"]]
        new_details.append(detail)
    return new_details


def get_valid_locations(details):
    main_campus = {
        "Americas": ["San Diego, CA, United States", "Colorado Springs, CO, United States", "St. Petersburg, FL, United States"],
        "EMEA": ["Addis Ababa, ----, Ethiopia", "Johannesburg, ----, South Africa", "Brussels, ----, Belgium"],
        "APAC": ["Singapore, ----, Singapore"]
    }
    onsite_loc_map = {'Brussels, Belgium': "Brussels, ----, Belgium",
                      'Colorado Springs, CO, USA': "Colorado Springs, CO, United States",
                      'Greensboro, NC, USA': "Greensboro, NC, United States",
                      'Saint-Nicolas de Véroce,France': "Saint-Nicolas de Véroce, ----, France",
                      'San Diego, CA, USA': "San Diego, CA, United States",
                      'Singapore': "Singapore, ----, Singapore",
                      'St. Petersburg, FL, USA': "St. Petersburg, FL, United States",
                      'The Hotel. Brussels': "Brussels, ----, Belgium",
                      'Le Negresco': "Nice, ----, France",
                      'Dubai, UAE (Sofitel Downtown Dubai)': "Dubai, ----, United Arab Emirates",
                      "Dubai, UAE": "Dubai, ----, United Arab Emirates",
                      "Nice, France": "Nice, ----, France"}
    onsite_location_set = set()
    new_details = []
    for detail in details:
        type = detail.get("type")
        if "online" in type:
            find = False
            region = detail.get("region")
            possible_campuses = main_campus[region]
            all_locations = detail.get("other_locations")
            print(detail["name"])
            print(region)
            print('cpamuses: ', possible_campuses)
            print('other_locations: ', all_locations)
            for campus in possible_campuses:
                for other_location in all_locations:
                    if campus.lower() in other_location.lower():
                        find = True
                        detail["location"] = [campus]
                        break
            if find is False:
                detail["location"] = [possible_campuses[0]]
            print('final location: ', detail['location'])
        else:
            if detail["location"] != '':
                onsite_location_set.add(detail["location"])
                detail["location"] = [onsite_loc_map[detail["location"]]]
        new_details.append(detail)
    return new_details

# def get_valid_schedule_location(details):
#     main_campus = {
#         "Americas": ["San Diego, CA, United States", "Colorado Springs, CO, United States",
#                      "St. Petersburg, FL, United States"],
#         "EMEA": ["Addis Ababa, ----, Ethiopia", "Johannesburg, ----, South Africa", "Brussels, ----, Belgium"],
#         "APAC": ["Singapore, ----, Singapore"]
#     }
#     onsite_loc_map = {'Brussels, Belgium': "Brussels, ----, Belgium",
#                       'Colorado Springs, CO, USA': "Colorado Springs, CO, United States",
#                       'Greensboro, NC, USA': "Greensboro, NC, United States",
#                       'Saint-Nicolas de Véroce,France': "Saint-Nicolas de Véroce, ----, France",
#                       'San Diego, CA, USA': "San Diego, CA, United States",
#                       'Singapore': "Singapore, ----, Singapore",
#                       'St. Petersburg, FL, USA': "St. Petersburg, FL, United States",
#                       'The Hotel. Brussels': "Brussels, ----, Belgium",
#                       'Le Negresco': "Nice, ----, France",
#                       'Dubai, UAE (Sofitel Downtown Dubai)': "Dubai, ----, Dubai",
#                       "Dubai, UAE": "Dubai, ----, Dubai",
#                       "Nice, France": "Nice, ----, France"}
#     onsite_location_set = set()
#     for detail in details:
#         schedules = detail.get('schedule')
#         type = detail.get("type")
#         for schedule in schedules:


def add_info_to_assessment_cert(details):
    for detail in details:
        if detail["name"] == "Assessment Certification":
            detail["type"] = 'online-selfpaced'
            detail["location"] = "San Diego, CA, United States"
            detail['desc'] = 'CCL’s Assessment Certification Course is a self-paced training with 10 hours (on average) of expert feedback facilitation content. The course provides the opportunity to prepare two feedback reports in a safe, low-risk environment, which will be reviewed by a Course Monitor. Participants who complete the Assessment Certification course and pass the certification exam can administer the leadership assessments in our portfolio: Benchmarks® by Design™, Benchmarks® for Managers™, Benchmarks® for Executives™, Benchmarks® for Learning Agility™, and Skillscope® — all of which include CCL Compass™, a digital tool that gathers your assessment data, interprets it, and recommends what to do next'
            detail['overview'] = {'desc': detail['desc'],
                                  'video_title': '',
                                  'video_url': ''}
            detail['tuition_number'] = 2100
            detail['languages'] = 'English'
    return details


def delete_non_import_attrs(details):
    new_details = []
    for detail in details:
        del detail["region"]
        del detail["other_locations"]
        new_details.append(detail)
    return new_details


def check_missing(details):
    attrs = ["name", "url", "languages", "location", "category", "effective_date_start", 'effective_date_end',
             'tuition_number', 'duration_desc', '']
    for detail in details:
        location = ''
        languages = ''


def write_all_categories(details):
    cates = set()
    for detail in details:
        categories = detail["category"]
        for category in categories:
            cates.add(category)
    final_cate_info = []
    for cate in list(cates):
        if "Mid-Level" in cate:
            cate = "Middle Manager Programs"
            url = 'https://www.ccl.org/leadership-challenges/middle-manager-training/'
            parent_url = ""
        elif cate == "Programs for Frontline & New Leaders":
            cate = "First-Level Manager Programs"
            url = 'https://www.ccl.org/leadership-challenges/new-manager-courses/'
        elif "Senior Executives" in cate:
            cate = 'Executive Leadership Programs'
            url = 'https://www.ccl.org/leadership-challenges/executive-leadership-programs/'
        elif cate == "Specialized Courses":
            cate = "Specialized Courses"
            url = 'https://www.ccl.org/leadership-programs/'
        else:
            cate = 'Online Leadership Training'
            url = 'https://www.ccl.org/leadership-programs/virtual-leadership-development-programs/'
        cate_info = {"category": cate,
                     "url": url,
                     "parent_url": "https://shop.ccl.org/"}
        final_cate_info.append(cate_info)
    today_date = date.today()
    today = today_date.strftime("%m%d")
    write_json(final_cate_info,
               f'./file_store/category_3333_CCL_XW_{today}.json')


def write_new_cates_to_details(details):
    for detail in details:
        categories = detail["category"]
        new_cates = []
        for cate in categories:
            new_cate = cate
            if "Mid-Level" in cate:
                new_cate = "Middle Manager Programs"
            elif cate == "Programs for Frontline & New Leaders":
                new_cate = "First-Level Manager Programs"
            elif "Senior Executives" in cate:
                new_cate = 'Executive Leadership Programs'
            elif cate == "Specialized Courses":
                new_cate = "Specialized Courses"
            else:
                new_cate = 'Online Leadership Training'
            new_cates.append(new_cate)
            detail["category"] = new_cates
    today_date = date.today()
    today = today_date.strftime("%m%d")
    write_json(details, f'./file_store/detail_3333_CCL_XW_{today}.json')
    return details


def change_location_for_specific_course(details):
    for detail in details:
        if detail["name"] == "Better Conversations & Coaching" and detail["type"] == "online-cvs":
            detail["location"] = ["Colorado Springs, CO, United States"]
            detail["type"] = "online-virtual"
    return details


def add_empty_course_to_no_plan_region(details):
    course_region_map = collections.defaultdict(set)
    course_version_map = collections.defaultdict(list)
    name_detail_map = dict()
    for detail in details:
        course_region_map[detail["name"]].add(detail['region'])
        course_version_map[detail["name"]].append(detail['version'])
        name_detail_map[detail["name"]] = detail
    new_empty_details = []
    for name, region in course_region_map.items():
        print(f'{name} -- {region} -- {course_version_map[name]}')
        add_version = 0
        if "Americas" not in region:
            add_version += 1
            location = "San Diego, CA, United States"
            new_empty_course = create_empty_course(name_detail_map[name], "Americas", max(
                course_version_map[name])+add_version, location)
            new_empty_details.append(new_empty_course)
        if "EMEA" not in region:
            add_version += 1
            location = "Brussels, ----, Belgium"
            new_empty_course = create_empty_course(name_detail_map[name], "EMEA", max(
                course_version_map[name])+add_version, location)
            new_empty_details.append(new_empty_course)
        if "APAC" not in region:
            add_version += 1
            location = "Singapore, ----, Singapore"
            new_empty_course = create_empty_course(name_detail_map[name], "APAC", max(
                course_version_map[name])+add_version, location)
            new_empty_details.append(new_empty_course)
    new_details = details + new_empty_details
    return new_details


def create_empty_course(detail, region, version, location):
    empty_detail = copy.deepcopy(detail)
    empty_detail['type'] = "onsite"
    empty_detail['active'] = False
    empty_detail['region'] = region
    empty_detail['version'] = version
    empty_detail['location'] = [location]
    empty_detail['effective_date_start'], empty_detail['effective_date_end'] = '', ''
    empty_detail['tuition_number'] = '0'
    empty_detail['schedule'] = [['', '', '', 'formal']]
    return empty_detail


def add_schedules_to_detail(file_path):
    urls = extract_all_urls(file_path)
    no_reapting_urls = no_repeating_urls(urls)
    url_schedule = get_schedule_by_urls(no_reapting_urls)
    with open(file_path, 'r') as f:
        details = json.load(f)
    for detail in details:
        url = detail['url']
        schedule = url_schedule.get(url)
        detail['schedule'] = schedule
    write_json(details, file_path)
    pprint(details)


def final_write():
    details = read_json()
    new_details = add_version(details)
    new_details = figure_out_type(new_details)
    new_details = get_same_course_other_locations(new_details)
    new_details = get_valid_locations(new_details)
    # add empty course when region does not have any plan
    print('---------')
    new_details = add_empty_course_to_no_plan_region(new_details)
    # delete region and other location
    new_details = delete_non_import_attrs(new_details)
    write_all_categories(new_details)
    new_details = change_location_for_specific_course(new_details)
    # detail write in this function is valid detail file
    write_new_cates_to_details(new_details)
    today_date = date.today()
    today = today_date.strftime("%m%d")
    add_schedules_to_detail(f'./file_store/detail_3333_CCL_XW_{today}.json')
    filter_schedules()
    # one_dSan Diego, CA, United Statesetail = [change_cate_details[0]]
    # write_json(one_detail, './file_store/test_detail_3333_CCL.json')

# details = read_json()
# new_details = add_version(details)
# new_details = figure_out_type(new_details)
# new_details = get_same_course_other_locations(new_details)
# get_valid_locations(new_details)
# # print_all_locations(details)
#
#
# # add last
# details = add_info_to_assessment_cert(details)
# #print_currency(details)

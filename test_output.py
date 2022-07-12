import collections
import json
from datetime import datetime
from pprint import pprint


def test_course_version():
    print('hi')
    with open('./file_store/detail_3333_CCL_XW_0130.json', 'r') as f:
        details = json.load(f)
    for detail in details:
        if detail["name"] == "Maximizing Your Leadership Potential":
            print(f"{detail['type']} - {detail['location']}")
            print(f"{detail['url']}")
        if detail["name"] == "Leadership at the Peak":
            print(detail["name"])
            print(len(detail["schedule"]))
            print(f"{detail['type']} - {detail['location']}")
            print(f"{detail['url']}")


# test_course_version()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import re

response = urllib.request.urlopen('https://facebook.com/facebook_username/about?section=education')#replace with real facebook username

# split the returned page by clasess that contains the work and educational history
returned_page = str(response.read())
mydata = returned_page.split('data-pnref=')

# create the json to hold all contents for work and education
work_details = []
container = []

# get only the parts that starts with " because they contain the real data we are looking for
for item in mydata:
    if item[:1] == "\"":
        capt = item[1: item.find("\"", 1)]
        if capt == 'work':
            container.append(item)

# split by the different places worked
if len(container) != 0:
    work_split = container[0].split('_3-91 _8o lfloat _ohe')

    # delete the items tht does not contain the work information
    new_container = []

    for item in work_split:
        if item[:6] == '" href':
            new_container.append(item)

    # Now lets start searching for parameters inside the each item in the new_container

    for item in new_container:

        # create an employer as dict
        work_container = {}
        work_container['employer'] = {}

        # search for the work id
        # search = re.search(r'id=(\d*)', item)
        search = re.search(r'<a href=\"https:[\S*]*/(\d+)', item)
        if search:
            work_container['employer']['id'] = search.group(1)

        # search for company name
        # search1 = re.search(r'show="1">([a-zA-Z0-9\s]+)', item) ">
        search1 = re.search(r'<a href=\"https:[\S*]*\">([\w+\s*]*)', item)
        if search1:
            work_container['employer']['name'] = search1.group(1)

        # search for the company url
        search2 = re.search(r'(www.facebook.com/\S*)\" tabindex', item)
        if search2:
            work_container['employer']['url'] = search2.group(1)

        # search for job job Position
        search3 = re.search(r'fsm fwn fcg">([a-zA-Z0-9\s]+)', item)
        if search3:
            work_container['position'] = search3.group(1)

        # search for roll description
        search4 = re.search(r'_3-8w _50f8">([a-zA-Z0-9\s,.]+)', item)
        if search4:
            work_container['job_description'] = search4.group(1)
        # search for period
        search5 = re.search(r'aria-hidden="true"> · </span>([a-zA-Z0-9\s]+)', item)
        if search5:
            work_container['period'] = search5.group(1)
            # get the start and end time
            periods = search5.group(1).split(' to ')
            work_container['start_time'] = periods[0]
            work_container['end_time'] = periods[1]

        # add this work details to our work list
        work_details.append(work_container)

print(work_details)

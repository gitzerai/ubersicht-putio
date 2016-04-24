#!/usr/bin/python
import sys, os
import json
import requests
import re
import collections
import operator
import time
from xml.dom import minidom
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

PUTIO_FOLDER_RSS = '' #example https://put.io/rss/video/12345678
PUTIO_USERNAME = '' #example username1
PUTIO_PASSWORD = '' #example password1
FROM_DATE_DAY_OFFSET = 3
SHOULD_VALIDATE_DATE = True
TIME_FORMAT = '%b %d'
ITEM_LIMIT = 10

data = {};
has_more_items = False
item_count = 0

def fetch_xml(url, username, password):
    r = requests.get(url, auth=(username, password))
    r.raise_for_status()
    return minidom.parseString(r.text)

def get_el_val(el, name):
    return el.getElementsByTagName(name)[0].childNodes[0].data

def get_show_name(orig_title):
    title = orig_title
    digit_search = re.search("\d", title)
    if digit_search:
        digit_index = digit_search.start()
        title = title[:digit_index]
        if (title[digit_index - 1] == 'S'):
            title = title[:digit_index - 1]

    return title.replace('.', ' ').title()

def get_season_episode(orig_title):
    title = orig_title
    digit_search = re.search("\d", title)
    if not digit_search:
        return title

    digit_index = digit_search.start()
    if title[digit_index - 1] == 'S':
        digit_index -= 1

    title = title[digit_index:]

    dot_search = re.search("[.]", title)

    if dot_search:
        dot_index = dot_search.start()
        title = title[:dot_index]

    return title

def get_episode(season_episode_string):
    # SxxEyy format
    if len(season_episode_string) == 6:
        return season_episode_string[4:6]

    # xxyy format
    if len(season_episode_string) == 4:
        return season_episode_string[2:4]

    # xyy format
    if len(season_episode_string) == 3:
        return season_episode_string[1:3]

    return '-'

def get_season(season_episode_string):
    # SxxEyy format
    if len(season_episode_string) == 6:
        return season_episode_string[1:3]

    # xxyy format
    if len(season_episode_string) == 4:
        return season_episode_string[:2]

    # xyy format
    if len(season_episode_string) == 3:
        return season_episode_string[0]

    return '-'

def parse_date(date_str):
    # stripping away the ' -0000' timezone info
    date_str = date_str[:(len(date_str) - 6)]
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S")

def validate_date(date_str):
    if not SHOULD_VALIDATE_DATE:
        return True

    parsed_date = parse_date(date_str)

    return get_from_date() <= parsed_date <= get_to_date()

def get_from_date():
    return datetime.now() - timedelta(days=FROM_DATE_DAY_OFFSET)

def get_to_date():
    return datetime.now()

def get_display_date(date):
    return date.strftime(TIME_FORMAT)

try:
    xml = fetch_xml(PUTIO_FOLDER_RSS, username=PUTIO_USERNAME, password=PUTIO_PASSWORD)
    items = xml.getElementsByTagName("item")

    for item in items:
        date = get_el_val(item, "pubDate")

        if not validate_date(date):
            continue

        item_count += 1

        orig_title = get_el_val(item, "title")

        title = get_show_name(orig_title)
        season_episode = get_season_episode(orig_title)

        season = get_season(season_episode)
        episode = get_episode(season_episode)

        key = title + " " + season_episode

        data[key] = {
            'name': title,
            'season': season,
            'episode': episode,
            'link': get_el_val(item, "guid")
        }

        if item_count == ITEM_LIMIT:
            has_more_items = True
            break

    if item_count == 0:
        data['message'] = 'No new shows :-('
    else:
        data = collections.OrderedDict(sorted(data.items()))
        if has_more_items:
            data['message'] = '... and more!'

    data['to_date'] = get_display_date(get_to_date())
    data['from_date'] = get_display_date(get_from_date())

except requests.ConnectionError as ce:
    data['error'] = 'Error'

print json.dumps(data) if isinstance(data, (dict, list, tuple, set)) else data.encode('utf-8')

sys.exit()

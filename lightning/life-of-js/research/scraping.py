"""
Convert monthly browser usage stats and release timelines to a standard usable representation

Usage CSV downloaded from : https://www.netmarketshare.com/browser-market-share.aspx?qprid=2&qpcustomd=0
Timeline: https://en.wikipedia.org/wiki/Timeline_of_web_browsers
"""

import collections
import csv
import datetime
import re

from bs4 import BeautifulSoup

def usage_by_browser(usage_fn):
    browser_pattern = re.compile('([^0-9.]+) ([0-9.]+)')
    stats = collections.defaultdict(dict)

    with open(usage_fn, 'r') as f:
        # skip first row
        f.readline()
        reader = csv.reader(f)
        for row in reader:
            print(row)
            browser, usage = row
            match = browser_pattern.match(browser)
            if match:
                name, version = match.groups()
            else:
                name = browser
                version = '???'

            stats[name][version] = usage

    return stats


def _find_table(soup, table_id):
    """CSS :has isn't official yet, so hack
    
    markup is ID span inside h3, and table is next sibling after that"""
    return soup.select(f'span[id="{table_id})"]')[0].parent.find_next_siblings('table')


def wikipedia_to_release_dates(wik_fn, table_id):
    """Convert the 2010s table into release dates by start of month as initial stab at release dates"""
    with open(wik_fn) as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')


if __name__ == '__main__':
    # mobile_fn = 'browser_share_mobile_apr2017.csv'
    # mobile_usage = usage_by_browser(mobile_fn)
    #
    # desktop_fn = 'browser_share_desktop_apr2017.csv'
    # desktop_usage = usage_by_browser(desktop_fn)

    # TODO: Merge usage stats/ identify better data source (netmarketshare's have many anomalies)
    # from pprint import pprint as pp
    # pp(mobile_usage)
    # pp(desktop_usage)


    wiki_fn = 'Timeline of web browsers - Wikipedia.html'
    releases = wikipedia_to_release_dates(wiki_fn, '2010s')
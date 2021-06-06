#!/usr/bin/env python3

import argparse
from datetime import date, datetime, timedelta
import requests
import urllib.parse

from bs4 import BeautifulSoup as BS4  # type: ignore
from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore

TWITTER_URL = 'https://twitter.com/search?'
TWITTER_SEARCH_URL = 'https://twitter.com/search'
TWITTER_ACCOUNT = 'debidebiru_sama'
CHANNEL_URL = 'https://www.youtube.com/channel/UCjlmCrq4TP1I4xguOtJ-31w'


def print_debiru_aa():
    print("hoge")


def make_twitter_search_query():
    """Make a URL encoded twitter search string"""
    yesterday: str = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    search_expression: str = f'from:{TWITTER_ACCOUNT} since:{yesterday}'
    query = {'q': search_expression, 'f': 'live' }
    return urllib.parse.urlencode(query, quote_via=urllib.parse.quote)

def fetch_latest_tweet():
    query_string: str = make_twitter_search_query()
    url: str = f'{TWITTER_SEARCH_URL}?{query_string}'
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # https://self-development.info/selenium%E3%81%A7twitter%E3%82%92%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0%E3%81%99%E3%82%8B%E3%80%90python%E3%80%91/
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'article')))

    html = driver.page_source.encode('utf-8')
    soup = BS4(html, 'html.parser')
    tweet = soup.select_one('main section h1 ~ div article > div > div > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) span').text
    return tweet

def decorate_word_balloon(message):
    """
      \^  ^/    +-----------------------        1st line
     <(@  @)>  <  6/6   23:00~                  2nd line
                |
                | と～ってもおそろしい
                | あくまのひ
                +-----------------------
    """
    max_length = 0

    lines = message.strip().splitlines()
    for line in lines:
        max_length = len(line) if max_length < len(line) else max_length
    prefix = '  \^  ^/    ' + '+' + '-' * max_length * 2 + '\n' + ' <(@  @)>  <  '

    decorated = prefix                  # 1st line
    decorated += (lines.pop(0) + '\n')  # 2nd line
    for line in lines:
        decorated += '            | ' + line + '\n'
    decorated += '            +' + '-' * max_length * 2 + '\n'
    return decorated



def fetch_youtube_video_url():
    pass

def main(args) -> None:
    if args.tweet:
        print(decorate_word_balloon(fetch_latest_tweet()))
    if args.video:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tweet', help='Show the latest debiru tweet', action='store_true', default=False)
    parser.add_argument('-v', '--video', help='Show the latest debiru youtube video URL', action='store_true', default=False)
    args = parser.parse_args()
    main(args)

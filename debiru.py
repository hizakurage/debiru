#!/usr/bin/env python3

import argparse
from datetime import date, datetime, timedelta
import json
import os
import re
import requests
import urllib.parse

from bs4 import BeautifulSoup as BS4  # type: ignore
import click

CHANNEL_URL = 'https://www.youtube.com/channel/UCjlmCrq4TP1I4xguOtJ-31w'


# Reference implementation: https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/master/Tweet-Lookup/get_tweets_with_bearer_token.py

TWITTER_API_ENDPOINT = 'https://api.twitter.com/2/tweets/search/recent'
TWITTER_ACCOUNT = 'debidebiru_sama'
def create_twitter_url():
    queries = {'query': f'from:{TWITTER_ACCOUNT} -is:retweet', 'max_results': 10}
    url = TWITTER_API_ENDPOINT + '?' + urllib.parse.urlencode(queries, quote_via=urllib.parse.quote)
    return url

def create_twitter_headers(bearer_token):
    return {'Authorization': f'Bearer {bearer_token}'}

def fetch_last_tweet(bearer_token: str) -> str:
    res = requests.get(create_twitter_url(), headers=create_twitter_headers(bearer_token))
    tweets = json.loads(res.content.decode('utf-8'))['data']
    return sorted(tweets, key=lambda tweet: tweet['id'], reverse=True)[0]['text']

def decorate_word_balloon(message):
    """
    (sample)

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
@click.command()
@click.option('-t', '--tweet', help='Show the last debiru-sama tweet', is_flag=True)
@click.option('-v', '--video', help='Show the last debigu-sama youtube video URL', is_flag=True)
@click.option('--bearer-token', default=lambda: os.environ.get('TWITTER_BEARER_TOKEN', ''))
def main(tweet, video, bearer_token):
    if bearer_token is '':
        click.echo('[ERROR] Twitter Bearer Token is missing.', err=True)
        exit(1)

    if tweet:
        tweet = fetch_last_tweet(bearer_token)
        click.echo(decorate_word_balloon(tweet))
    if video:
        pass

if __name__ == '__main__':
    main()

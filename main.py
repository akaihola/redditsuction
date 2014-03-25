#!/usr/bin/env python

"""Script for batch downloading comments from a subreddit"""

from __future__ import print_function

import argparse
from pprint import pprint
import requests
import textwrap

COMMENTS_URL = 'http://www.reddit.com/r/{subreddit}/comments.json'


def get_comments_before(subreddit, comment_id):
    params = {'limit': 102}

    if comment_id:
        params['before'] = 't1_{}'.format(comment_id)

    url = COMMENTS_URL.format(subreddit=subreddit)
    response = requests.get(
        url,
        params=params,
        headers={'user-agent': 'redditsuction/0.1 by akaihola'})
    return response.json()


def get_comment_data(json_response):
    return [comment['data'] for comment in json_response['data']['children']]


def print_comments(comments):
    for comment in comments:
        print()
        print('----- {} {} {} ----- {}'
              .format(comment['author'],
                      (50 - len(comment['author'])) * '-',
                      comment['created_utc'],
                      comment['id']))
        print(textwrap.fill(comment['body']))


def main():
    parser = argparse.ArgumentParser(
        epilog='example: main.py Bitcoin cg7c9ux')
    parser.add_argument('-j', '--json', action='store_true')
    parser.add_argument('subreddit')
    parser.add_argument('before', nargs='?')
    opts = parser.parse_args()
    json_response = get_comments_before(opts.subreddit, opts.before)
    if opts.json:
        pprint(json_response)
    else:
        comments = get_comment_data(json_response)
        print_comments(comments)


if __name__ == '__main__':
    main()

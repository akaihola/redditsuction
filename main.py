"""Script for batch downloading comments from a subreddit"""

import requests
import sys
import textwrap

COMMENTS_URL = 'http://www.reddit.com/r/{subreddit}/comments.json'


def get_comments_before(subreddit, comment_id):
    params = {}

    if comment_id:
        params['before'] = 't1_{}'.format(comment_id)

    url = COMMENTS_URL.format(subreddit=subreddit)
    response = requests.get(url, params=params)
    json_response = response.json()
    return [comment['data'] for comment in json_response['data']['children']]


def print_comments(comments):
    for comment in comments:
        print
        print ('----- {} {} {} ----- {}'
               .format(comment['author'],
                       (50 - len(comment['author'])) * '-',
                       comment['created_utc'],
                       comment['id']))
        print textwrap.fill(comment['body'])


def main():
    if not 2 <= len(sys.argv) <= 3:
        print 'usage: python main.py <subreddit> [before_comment_id]'
        print 'example: python main.py Bitcoin cg7c9ux'
        sys.exit(1)
    subreddit = sys.argv[1]
    if len(sys.argv) > 2:
        before = sys.argv[2]
    else:
        before = None
    comments = get_comments_before(subreddit, before)
    print_comments(comments)


if __name__ == '__main__':
    main()

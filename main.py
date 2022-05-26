#!/usr/bin/env python3

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'REPLACE_ME'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.channels().list(
    forUsername='Google',
    part='id',
    maxResults=options.max_results,
  ).execute()

  playlist = search_response['items'][0]['id']

  search_response = youtube.search().list(
    channelId=playlist,
    part='id,snippet',
    order='date',
    maxResults=options.max_results,
  ).execute()

  videos = []
  for search_result in search_response.get('items', []):
    videos.append('%s (%s)' % (search_result['snippet']['title'],
                               search_result['snippet']['thumbnails']['high']))

  print('Videos:\n', '\n'.join(videos), '\n')


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='Google')
  parser.add_argument('--max-results', help='Max results', default=50)
  args = parser.parse_args()

  try:
    youtube_search(args)
  except HttpError as e:
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content.decode()))

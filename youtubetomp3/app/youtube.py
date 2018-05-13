#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyAWUik4CH1y7aw7Df6bHQ1DQxcA89Nxio8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  title = []
  url =[]
  images = []
  
  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      
      title.append("%s" % (search_result["snippet"]["title"]))

      url.append("%s" % (str("https://www.youtube.com/watch?v=")+search_result["id"]["videoId"]))
      images.append("%s" % (search_result["snippet"]["thumbnails"]["medium"]["url"]))

  data =[]
  for val in title:
    for urls in url:
      for img in images:
        data.append({"url": urls,
                    "title": val,
                    "image": img})
  print data

  
print("search keywords")
search = raw_input()
print('Waiting for results')

if __name__ == "__main__":

  argparser.add_argument("--q", help="", default=search)
  argparser.add_argument("--max-results", help="Max results", default=2)
  args = argparser.parse_args()

  try:

    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

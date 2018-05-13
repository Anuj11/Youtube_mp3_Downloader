from django.shortcuts import render, redirect
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from django.template.loader import get_template
from django.template import Context
from collections import OrderedDict

# from __future__ import unicode_literals
import youtube_dl

DEVELOPER_KEY = "AIzaSyAWUik4CH1y7aw7Df6bHQ1DQxcA89Nxio8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(q, max_results=10):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=q,
    part="id,snippet",
    maxResults=max_results,
    
  ).execute()

  data = []
  

  for search_result in search_response.get("items", []):
    
    if search_result["id"]["kind"] == "youtube#video":
      
      data.append({
          "title": (search_result["snippet"]["title"]),
          "url": (str("https://www.youtube.com/watch?v=")+search_result["id"]["videoId"]),
          "images": (search_result["snippet"]["thumbnails"]["high"]["url"])
          })

  return data


def search_result(request):
  if request.method == 'GET':
    keyword =request.GET.get("value", None) 
    
    if keyword is None:
      return render(request, "search_result.html")
    else:
      if keyword is not None:
        print("llllllllllllllllll", keyword)
        search_data = youtube_search(q=keyword)
        print('search_data', search_data)
        return render(request, "search_keyword1.html", {'search_data': search_data})

        

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')



def renderView(d, video_id):
  with youtube_dl.YoutubeDL(d) as ydl:
        filename = ydl.download([video_id])
  

def convertTomp3(video_id):

  if video_id is not None:

    d = {
      'format': 'bestaudio/best',
      'progress_hooks': [my_hook],
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '128',
          
      }],
    }
    
    renderView(d, video_id)

            
def search_list(request):
  print('15455')
  video_id =request.GET.get("video_id", None)
  convertTomp3(video_id)
  return render(request, 'convertTomp3.html', {"filename":"Done downloading"})
  








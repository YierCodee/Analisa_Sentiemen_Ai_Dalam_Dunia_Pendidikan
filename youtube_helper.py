import os 
import pandas as pd
import google_auth_oauthlib.flow 
import googleapiclient.discovery
import googleapiclient.errors

from IPython.display import JSON
import json
import pprint
from dateutil import parser

#visualization packages
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
api_key = ""

# Penghubung API YouTube 
def get_youtube_client():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    return googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Set up YouTube API credentials
def get_channel(idChannel = "UCNJ1Ymd5yFuUPtn21xtRbbw"): #-> Channel ID defaultnya adalah channel CrashCourse
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    
    # Get credentials and create an API client
    youtube =  get_youtube_client()
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=idChannel
    )
    response = request.execute()
    return response

#Ambil 50 video terbaru dari channel
def get_video_ids(playlistID,   target_count = 50):
            video_ids = []
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
            next_page_token = None
            #api_service_name = "youtube"
            #api_version = "v3"
            #get credentials and create an API client
            youtube =  get_youtube_client()
            print(f"-> Mulai mengunduh daftar video... Target: {target_count}")
            while len(video_ids) < target_count:
                try:
                    request = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlistID,
                    maxResults=50,
                    pageToken=next_page_token
                    )
                    response = request.execute()
                    for item in response['items']: 
                        video_ids.append(item['snippet']['resourceId']['videoId'])
                        if len(video_ids) >= target_count:
                         break
                    #Halaman Selanjutnya
                    print(f"   [Proses] Berhasil menghimpun {len(video_ids)} Video ID...")

                    #update page 
                    next_page_token = response.get('nextPageToken')
                    if not next_page_token:
                        print("   [Info] Semua video yang tersedia di channel ini sudah berhasil ditarik.")
                        break
                except Exception as e:
                    print(f"❌ Terjadi kendala saat menarik halaman daftar video: {e}")
                break
            return video_ids

def get_video_ids2(playlistID = ""):
            video_ids = []
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
            api_version = "v3"
            api_service_name = "youtube"
            #get credentials and create an API client
            youtube = get_youtube_client()
            request = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlistID,
                    maxResults=50
            )
            response = request.execute()
            for item in response['items']:
                video_ids.append(item['snippet']['resourceId']['videoId'])
                next_page_token = response.get('nextPageToken')
            return video_ids
          
def get_video_details(video_ids):
    """Fungsi 3: Mengambil Statistik Detail dengan Cara yang Lebih Aman"""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = get_youtube_client()

    # Menggabungkan list ID menjadi string panjang dipisah koma
    id_string = ",".join(video_ids)
    
    request = youtube.videos().list(
        part="snippet,statistics",
        id=id_string
    )
    response = request.execute()
    all_video_info = []
    
    # Ekstrak langsung secara manual tanpa loop bertingkat agar aman
    for video in response.get("items", []):
        snippet = video.get("snippet", {})
        statistics = video.get("statistics", {})
        
        video_info = {
            "video_id": video.get("id"),
            "channelTitle": snippet.get("channelTitle"),
            "title": snippet.get("title"),
            "publishedAt": snippet.get("publishedAt"),
            "viewCount": statistics.get("viewCount", 0),
            "likeCount": statistics.get("likeCount", 0),
            "commentCount": statistics.get("commentCount", 0)
        }
        all_video_info.append(video_info)
        
    return pd.DataFrame(all_video_info)

def get_video_comments(video_id, target_count = 100):
    """Fungsi 4: Mengambil Komentar Video dengan Penanganan Pagination"""
    youtube = get_youtube_client()
    komentar_list = []
    next_page_token = None
    try: 
          while len(komentar_list) < target_count:
                sisa_ambil = target_count - len(komentar_list)
                max_results = min(100, sisa_ambil)  # Maksimal API youtube
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=max_results,
                    pageToken=next_page_token
                )
                response = request.execute()
                for item in response.get("items", []):
                      top_comment = item["snippet"]["topLevelComment"]["snippet"]
                      komentar_list.append({
                            "video_id": video_id,
                            "comment_id": item["id"],
                            "author": top_comment.get("authorDisplayName"),
                            "comment_mentah": top_comment.get("textDisplay"),
                            "likeCount": top_comment.get("likeCount", 0),
                            "publishedAt": top_comment.get("publishedAt")
                      })
                      if len(komentar_list) >= target_count:
                         break
                print(f"   [Proses] Berhasil mengunduh {len(komentar_list)} komentar...")
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                      print("   [Info] Semua komentar yang tersedia di video ini sudah diambil.")
                      break  # Tidak ada halaman berikutnya, keluar dari loop
    except googleapiclient.errors.HttpError as e:
          print(f"Terjadi error saat mengambil komentar: {e}")

    print(f"🎉 Selesai! Total komentar yang berhasil dihimpun: {len(komentar_list)}")
    return komentar_list

import requests
import os
import json

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
#returns a json of a single youtube video
def youtubeSearch(query, max_results=1):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        results.append({
            "title": item["snippet"]["title"],
            "video_url": f"https://www.youtube.com/watch?v={video_id}"
        })
    #print(results[0])
    # output: {'title': 'DRAKE - FAMILY MATTERS', 'video_url': 'https://www.youtube.com/watch?v=ZkXG3ZrXlbc'}
    return json.dumps(results[0])

#Example
if __name__ == "__main__":
    print(youtubeSearch("Euler's Constant"))
        
    '''
    for video in youtube_search("kendrick lamar not like us"):
        print(f"{video['title']} — {video['video_url']}")
    '''

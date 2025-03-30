import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def youtubeSearch(query, max_results=1):
    """
    Search for YouTube videos and return information about them.
    
    Args:
        query (str): The search query
        max_results (int): Maximum number of results to return
        
    Returns:
        dict: Information about the first video found
    """
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set")
    
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        data = response.json
        
        results = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            results.append({
                "title": item["snippet"]["title"],
                "video_url": f"https://www.youtube.com/watch?v={video_id}"
            })
        
        if not results:
            return {"error": "No videos found for this query"}
            
        # Return the first result as a dictionary (not as JSON string)
        return results[0]
    
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except (KeyError, IndexError) as e:
        return {"error": f"Error parsing response: {str(e)}"}

# Example
# if __name__ == "__main__":
#     result = youtubeSearch("Euler's Constant")
#     print(json.dumps(result, indent=2))  # Pretty print the JSON result
        
#     '''
#     for video in youtube_search("kendrick lamar not like us"):
#         print(f"{video['title']} — {video['video_url']}")
#     '''

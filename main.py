import requests,os,configparser,praw,sys,json
from reddit_video_downloader.apivideo_ import upload_video

"""
To download video from a reddit when called in the comments.
1. Bot is called when username comments SUMMONING_WORDS in a particular subreddit.
2. Download the audio and video from .json files.          
3. Upload the output.mp4 to a streaming platform like api.video        
4. Post the link of the uploaded file as a comment under the submission            
5. Delete the video.mp4, audio.mp3 and output.mp4 files from the system
"""

SUMMONING_WORDS = "!save_video"
def download_video(url):
    
    """"
    Gets the permalink from the main() and  downloads the audio and video.
    Then combines them using ffmpeg.
    """
    
    url_json = url + '.json'
    r = requests.get(url_json, headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"})
    data = r.json()[0]
    try:
        video_url = data["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"]
        audio_url = video_url[:31] + "/DASH_audio.mp4"
        with open("video.mp4","wb") as f:
            g = requests.get(video_url,stream=True)
            f.write(g.content)

        with open("audio.mp3","wb") as f:
            g = requests.get(audio_url,stream=True)
            f.write(g.content)

        os.system("ffmpeg -loglevel warning -i video.mp4 -i audio.mp3 -c copy -y output.mp4")

    except Exception as e:
            print("Could not download video.", e)
            
def delete_files():
    
    """delete file after uploading them on a platform"""
    
    parent_path = "S:\PythonProgs\sadagg\\reddit_video_downloader"
    paths = [parent_path + x for x in ["\\video.mp4","\\audio.mp3","\\output.mp4"]]
    for path in paths:
        os.remove(path)
def main():
    
    """
    fetches the information from auth.ini and creates a reddit instance.
     It then checks if the SUMMONING_WORDS were used in the streaming comments
     and also checks whether the submission is a reddit hosted video.
     If the criteria satisfies, it sends the url to download_video()
     """
    
    config = configparser.ConfigParser()
    config.read('auth.ini')
    r = praw.Reddit(
        client_id=config.get('credentials', 'reddit_client_id'),
        client_secret= config.get('credentials', 'reddit_client_secret'),
        password=config.get('credentials', 'reddit_password'),
        username=config.get('credentials', 'reddit_username'),
        user_agent= config.get('credentials', 'reddit_user_agent')
    )

    sub = r.subreddit("perfectlycutscreams")
    for comment in sub.stream.comments(skip_existing=True):
        try:
            if SUMMONING_WORDS in comment.body.lower() and comment.submission.is_video:
                print("Downloading video...")
                permalink = "https://reddit.com" + comment.submission.permalink
                download_video(permalink)
                mp4_url = upload_video(comment.submission.title)
                my_reply = comment.reply(body=f"Special delivery for {comment.author}: {mp4_url}")
                print("Replied.\nhttps://reddit.com{}".format(my_reply.permalink))
                delete_files()
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    main()

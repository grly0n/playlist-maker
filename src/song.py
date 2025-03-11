import requests

class Song:
    def __init__(self, url: str):
        self.url = url

    def fetch_information(self):
        url = 'https://api.spotify.com/tracks/11dFghVXANMlKmJXsNCbNl'
        access_token = '1a988aa2690a454d838d6522726b8d65'
        request = requests.get(url, headers={
            "Authorization": 'Bearer' + access_token
        })
        print(request.json())
        

if __name__=="__main__":
    song = Song('www.google.com')
    song.fetch_information()

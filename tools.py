import asyncio
import assist
from icrawler.builtin import GoogleImageCrawler
import requests
import os
#import spot




async def get_weather(city_name):
    url = f"http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q={city_name}"
    data = requests.get(url).json()
    weather = f"{data['location']['name']} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    return weather


def search(query):
    google_Crawler = GoogleImageCrawler(storage={"root_dir": r'./'})
    google_Crawler.crawl(keyword=query, max_num=1)


def parse_command(command):
    if "weather" in command:
        weather_description = asyncio.run(get_weather("Hyderabad"))
        query = "System information: " + str(weather_description)
        print(query)
        response = assist.ask_question_memory(query)
        assist.TTS(response)

    if "search" in command:
        query = command.split("-")[1]
        search(query)
'''
    if "play" in command:
        spot.start_music()

    if "pause" in command:
        spot.stop_music()

    if "skip" in command:
        spot.skip_to_next()

    if "previous" in command:
        spot.skip_to_previous()

    if "spotify" in command:
        spotify_info = spot.get_current_playing_info()
        query = "System information: " + str(spotify_info)
        print(query)
        response = assist.ask_question_memory(query)
        assist.TTS(response)

'''


#!/usr/bin/python
# -*- coding: utf-8 -*-

# **************************************************** #
#                                                      #
#                     TweetBoxBot                      #
#                                                      #
#             ***************************              #
#                                                      #
#     Created by ShevAbam (@shevabam | shevarezo.fr)   #
#     https://github.com/shevabam/TweetBoxBot          #
#     Example with @TweetBoxBot                        #
#                                                      #
# **************************************************** #

import urllib, urlparse, json, random, os, time, sys

from twython import Twython


# **************************************** #
# *              [ CONFIG ]              * #
# **************************************** #

# Twitter app keys
CONSUMER_KEY        = ""
CONSUMER_SECRET     = ""
ACCESS_TOKEN        = ""
ACCESS_TOKEN_SECRET = ""

# Categories to search for retrieve GIF from giphy.com
GIF_CATEGORIES = ["funny", "cat", "reaction", "falling", "excited"]

# Name of the gif retrieved
TMP_FILE = "/tmp/tbb_tmp"

# OpenWeatherMap API key
OWM_APIKEY = "9ffc8e8d9b6cdf53f8bf6b2168b7d7b5"

# TheMovieDb.org API key
TMDB_APIKEY = "84aff0198a9e4786d15f054cb2d4eafa"

# Hosts to ping (random)
PING_HOSTS = ["facebook.com", "google.com", "twitter.com"]

# Add what you want at the end of the tweet
TWITTER_SUFFIX = " #raspberrypi #TweetBoxBot"

# Debug log
DEBUG = False # True or False
DEBUG_FILE = "TweetBoxBot.log"


# Returns human size
def sizeToHuman(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)


# Uptime
def uptime():
    try:
        f = open("/proc/uptime")
        contents = f.read().split()
        f.close()
    except:
        return

    total_seconds = float(contents[0])

    # Helper vars
    MINUTE  = 60
    HOUR    = MINUTE * 60
    DAY     = HOUR * 24

    # Get the days, hours, etc
    days    = int(total_seconds / DAY)
    hours   = int((total_seconds % DAY) / HOUR)
    minutes = int((total_seconds % HOUR) / MINUTE)
    seconds = int(total_seconds % MINUTE)

    # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
    uptime = ""
    if days > 0:
        uptime += str(days) + " day" + (days > 1 and "s" or "") + ", "
    if len(uptime) > 0 or hours > 0:
        uptime += str(hours) + " hour" + (hours > 1 and "s" or "") + ", "
    if len(uptime) > 0 or minutes > 0:
        uptime += str(minutes) + " minute" + (minutes > 1 and "s" or "") + ", "
    uptime += str(seconds) + " second" + (seconds > 1 and "s" or "")

    content = "I'm up since "+uptime+" #uptime"
    media = ""

    return content, media;


# CPU Load
def cpu_load():
    nb_cores = int(os.popen('cat /proc/cpuinfo | grep "^processor" | wc -l').read().strip())
    load = os.getloadavg()

    load1 = (load[0] * 100) / nb_cores
    if load1 > 100:
        load1 = 100

    load5 = (load[1] * 100) / nb_cores
    if load5 > 100:
        load5 = 100

    load15 = (load[2] * 100) / nb_cores
    if load15 > 100:
        load15 = 100

    content = "CPU Load : \nSince 1 minute: "+str(int(load1))+"%\nSince 5 minutes: "+str(int(load5))+"%\nSince 15 minutes: "+str(int(load15))+"%"
    media = ""

    return content, media;


# CPU Frequency
def cpu_freq():
    cpu_freq = ""
    cpu_freq = os.popen('cat /proc/cpuinfo | grep -i "^cpu MHz" | awk -F": " \'{print $2}\' | head -1').read().strip()

    # For Raspberry Pi
    if not cpu_freq and os.path.isfile('/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq'):
        cpu_freq = os.popen('cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq').read().strip()
        cpu_freq = float(cpu_freq) / 1000

    if not cpu_freq:
        cpu_freq = "??"

    content = "Current CPU frequency: "+str(cpu_freq)+" MHz"
    media = ""

    return content, media;


# CPU Temp
def cpu_temp():
    cpu_temp = ""

    # Raspberry Pi
    if os.path.isfile("/sys/class/thermal/thermal_zone0/temp"):
        cpu_temp = os.popen('cat /sys/class/thermal/thermal_zone0/temp').read().strip()
        cpu_temp = round(float(cpu_temp) / 1000, 2)

    # If lm-sensors is installed
    elif os.path.isfile("/usr/bin/sensors"):
        cpu_temp = os.popen('/usr/bin/sensors | grep -E "^(CPU Temp|Core 0)" | cut -d \'+\' -f2 | cut -d \'.\' -f1').read().strip()

    if not cpu_temp:
        cpu_temp = "??"

    content = "Current CPU temperature: "+str(cpu_temp)+" °C"
    media = ""

    return content, media;


# RAM Load
def mem_load():
    # total
    total = os.popen('grep MemTotal /proc/meminfo | awk \'{print $2}\'').readline().strip()
    total = long(total) * 1024
    
    # free = free + buffers + cached
    free    = os.popen('grep MemFree /proc/meminfo | awk \'{print $2}\'').readline().strip()
    buffers = os.popen('grep Buffers /proc/meminfo | awk \'{print $2}\'').readline().strip()
    cached  = os.popen('grep Cached /proc/meminfo | awk \'{print $2}\'').readline().strip()
    
    free = long(free) + long(buffers) + long(cached)
    free = free * 1024

    # return "Memory load :\nFree: "+str(sizeToHuman(free))+"\nUsed: "+str(sizeToHuman(used))+"\nTotal: "+str(sizeToHuman(total))
    content = "I have "+str(sizeToHuman(free))+" free RAM of "+str(sizeToHuman(total))
    media = ""

    return content, media;


# Kernel version
def kernel():
    kernel = os.popen("uname -r").read().strip()
    
    content = "My #kernel is "+kernel
    media = ""

    return content, media;


# Speedtest
def speedtest():
    speedtest = os.popen("speedtest-cli --simple --timeout 90")
    
    content = speedtest.read().strip()+"\n"
    media = ""

    return content, media;


# Ping
def ping():
    host = random.choice(PING_HOSTS)

    ping = os.popen("/bin/ping -qc 1 "+host+" | awk -F/ '/^rtt/ { print $5 }'").read().strip()

    content = host+": "+ping+" ms #ping"
    media = ""

    return content, media;


# City time
def time_city():
    city_time = ''
    city = ''
    country_name = ''

    # Gets all coutries
    countries = json.loads(urllib.urlopen("https://restcountries.herokuapp.com/api/v1").read())

    while not city_time:
        country = random.choice(countries)
        country_name = country['name']['common']

        city = country['capital']

        lat = str(country['latlng'][0])
        lng = str(country['latlng'][1])

        # Gets the real time in the capital of the country
        time = json.loads(urllib.urlopen("http://api.geonames.org/timezoneJSON?lat="+lat+"&lng="+lng+"&username=tweetboxbot").read())

        if 'time' in time:
            city_time = time['time']

    content = "In "+city.encode("utf8")+" ("+country_name.encode("utf8")+"), it's "+str(city_time.split()[1])+" ("+str(city_time.split()[0])+") #time"
    media = ""

    return content, media;


# Temperature of a randomly city
def weather():
    city_temp = ''
    city = ''
    country_name = ''

    # Gets all countries
    countries = json.loads(urllib.urlopen("https://restcountries.herokuapp.com/api/v1").read())

    while not city_temp:
        country = random.choice(countries)
        country_name = country['name']['common']

        city = country['capital']

        # Gets the weather in the capital of the country
        weather = json.loads(urllib.urlopen("http://api.openweathermap.org/data/2.5/weather?APPID="+OWM_APIKEY+"&q="+urllib.quote_plus(city.encode("utf8"))+"&mode=json&units=metric").read())

        if 'main' in weather:
            if 'temp' in weather['main']:
                city_temp = int(weather['main']['temp'])

    content = "It is "+str(city_temp)+"°C to "+city.encode("utf8")+" ("+country_name.encode("utf8")+") #weather"
    media = ""

    return content, media;


# Get random Gif from giphy.com
def gif():
    category = random.choice(GIF_CATEGORIES)

    datas = json.loads(urllib.urlopen("http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag="+category).read())
    random_gif = datas['data']['image_original_url']
    
    urllib.urlretrieve(random_gif, TMP_FILE+'.gif')

    content = "Random GIF from @giphy"
    media = TMP_FILE+'.gif'

    return content, media;


# Get random Chuck Norris quote from icndb.com
def chuck_quote():
    quote_len = 200

    while quote_len > 100: # 100 is the maximum length of the quote for the tweet
        datas = json.loads(urllib.urlopen("http://api.icndb.com/jokes/random").read())
        quote = datas['value']['joke']

        quote_len = len(quote)

    content = quote+" @chucknorris #quote"
    media = ""

    return content, media;


# Get random Ron Swanson quote from https://github.com/jamesseanwright/ron-swanson-quotes
def ron_quote():
    quote_len = 300

    while quote_len > 200: # 200 is the maximum length of the quote for the tweet
        datas = json.loads(urllib.urlopen("http://ron-swanson-quotes.herokuapp.com/v2/quotes").read())
        quote = datas[0]

        quote_len = len(quote)

    content = quote+" @RonUSwanson #quote"
    media = ""

    return content, media;


# Get random popular movie title and image from themoviedb.org
def movie():
    configuration = json.loads(urllib.urlopen("http://api.themoviedb.org/3/configuration?api_key="+TMDB_APIKEY).read())
    images_path = configuration['images']['base_url']+configuration['images']['backdrop_sizes'][1]

    popular = json.loads(urllib.urlopen("http://api.themoviedb.org/3/movie/popular?api_key="+TMDB_APIKEY).read())
    movies = popular['results']

    movie = random.choice(movies)
    movie_title = movie['title']
    movie_link  = "http://themoviedb.org/movie/"+str(movie['id'])
    movie_image = images_path+movie['backdrop_path']

    filename, file_ext = os.path.splitext(os.path.basename(urlparse.urlsplit(movie_image).path))
    urllib.urlretrieve(movie_image, TMP_FILE+file_ext)

    content = movie_title+" "+movie_link+" @themoviedb"
    media = TMP_FILE+file_ext

    return content, media;


 # Get Astronomy Picture Of the Day (NASA)
def apod():
    datas = json.loads(urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY").read())
    picture = datas['hdurl']
    title = datas['title']
    date = datas['date']

    filename, file_ext = os.path.splitext(os.path.basename(urllib.parse.urlsplit(picture).path))

    urllib.request.urlretrieve(picture, TMP_FILE+file_ext)

    content = "NASA APOD of "+date+" - "+title+" @apod"
    media = TMP_FILE+file_ext

    return content, media;
  
# Get some number fact with numbersapi.com
def numbers():
    datas = json.loads(urllib.urlopen("http://numbersapi.com/random/trivia?json").read())
    text = datas['text']

    content = "Number fact: "+text+" #numbers #numbersapi"
    media = ""

    return content, media;


# Get random Breaking Bad quote from https://breakingbadquotes.xyz
def breakingbadquote():
    quote_len = 300

    while quote_len > 200: # 200 is the maximum length of the quote for the tweet
        datas = json.loads(urllib.urlopen("https://api.breakingbadquotes.xyz/v1/quotes").read())
        quote = datas[0]

        quote_len = len(quote['quote'])

    content = "\""+quote['quote']+"\" - "+quote['author']+" #BreakingBadQuotes #BreakingBad #quote"
    media = ""

    return content, media;


# Get random Game of Thrones quote from https://gameofthronesquotes.xyz
def gameofthronesquote():
    quote_len = 300

    while quote_len > 200: # 200 is the maximum length of the quote for the tweet
        datas = json.loads(urllib.urlopen("https://api.gameofthronesquotes.xyz/v1/random").read())
        quote = datas

        quote_len = len(quote['sentence'])

    content = "\""+quote['sentence']+"\" - "+quote['character']['name']+" #GameOfThronesQuote #GameOfThrones #quote"
    media = ""

    return content, media;


# Debug log
if DEBUG is True:
    log_file = open(DEBUG_FILE, 'ab+')
    log_file.write("--- START "+time.strftime("%Y-%m-%d %H:%M:%S")+" ---\n")


# Available functions. You can remove or comment some if you want (the last item has no ",")
options = [
    "uptime", 
    "cpu_load", 
    "cpu_freq", 
    "cpu_temp", 
    "mem_load", 
    "kernel", 
    "speedtest", 
    "ping", 
    "time_city", 
    "weather", 
    "gif", 
    "chuck_quote",
    "ron_quote",
    "movie",
    "apod",
    "numbers",
    "breakingbadquote",
    "gameofthronesquote"
]


# If argument is passed
if len(sys.argv) > 1:
    for key, item in enumerate(options):
        if item == sys.argv[1]:
            choice = key

# If not, generate random number for what choice
if not 'choice' in locals():
    choice = random.randint(0, int(len(options))-1)


# Get datas depending on the choice
content, media = locals()[options[choice]]()


# Debug log
if DEBUG is True:
    log_file.write("Choice : "+str(choice)+"\n")
    log_file.write("Function : "+options[choice]+"\n")
    log_file.write("Content : "+content+"\n")
    log_file.write("--- END "+time.strftime("%Y-%m-%d %H:%M:%S")+" ---\n\n")
    log_file.close()


# Publish on Twitter
if content and content.strip() != "":
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    if media:
        photo = open(media, 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=content+TWITTER_SUFFIX, media_ids=[response['media_id']])
        os.remove(media)
    else:
        twitter.update_status(status=content+TWITTER_SUFFIX)

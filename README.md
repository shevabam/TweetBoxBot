TweetBoxBot is a script written in Python that automatically tweets random informations from a Linux machine.

The initial idea was to "speak" a Raspberry Pi on Twitter. The script tweets several information such as:

- uptime
- CPU load
- CPU frequency
- CPU temperature
- available memory
- kernel version
- speedtest datas
- ping
- local time in a random city
- the temperature of a random city
- random GIF
- random Chuck Norris quote
- random Ron Swanson quote
- random popular movie title and picture
- the Astronomy Picture Of the Day from NASA
- NumberAPI, an API of intersting number facts
- random Breaking Bad quote
- random Game of Thrones quote

TweetBoxBot is used on my Raspberry Pi 2 with the dedicated Twitter account  [@TweetBoxBot](https://twitter.com/tweetboxbot).

![](TweetBoxBot.jpg)

# Prerequisites

You must have Python installed.

The script uses the **speedtest-cli** package to test the Internet connection. To install it, use your package manager (on Debian, do `apt-get install speedtest-cli`).  
However, if the package is not found, go through the Python package manager. Here are the commands:

	apt-get install python-pip

	pip install speedtest-cli

Once installation is complete, test with `speedtest-cli --simple`.

If you do not run the script on a Raspberry Pi, you have to install `lm-sensors` to retreive CPU temperature.

TweetBoxBot uses the **Twython** package, which is a simple interface to communicate with Twitter in Python. To install it, just do:

	pip install twython

# Creating a Twitter application

To communicate on Twitter from the script with the Twitter API, you must create a Twitter application. Nothing complicated well. To do this, go on [https://apps.twitter.com/](https://apps.twitter.com/).

Click on "Create new app" button. Just put a name and a description. You can put anything in the *Website* field.

By default, the app is set to read-only, so you won't be able to publish tweets. Go to the "Permissions" tab and modify access to **"Read, Write and Access direct messages"**.

Once saved, go to the "Keys and Access Tokens" tab and click the button at the bottom ("Create my access token").

Leave the page open for later, we will need to copy paste some of those keys in the script.


# The TweetBoxBot script

Download the script via the "[Download ZIP](https://github.com/shevabam/TweetBoxBot/archive/master.zip)" button to the right or do `git clone https://github.com/shevabam/TweetBoxBot.git` directly on your machine.

The script is pretty simple. Each information transmitted over Twitter is a function. At the end of the script, I generate a random number having the maximum number of available functions. Thus, once found the number, the script launches the corresponding function and publishes on Twitter the content returned!

At the beginning of the script, you must change the following variables that correspond to the keys present in the page of the Twitter app:

- `CONSUMER_KEY` by your *Consumer Key (API Key)*
- `CONSUMER_SECRET` by your *Consumer Secret (API Secret)*
- `ACCESS_TOKEN` by your *Access Token*
- `ACCESS_TOKEN_SECRET` by your *Access Token Secret*

Then, you have several others variables that you can edit:

- `GIF_CATEGORIES` : contains search keywords to a random GIF on giphy.com
- `TMP_FILE` : is the name of the recovered file from the Giphy API or TheMovieDb API (deleted after you send the tweet)
- `OWM_APIKEY` : API key from openweathermap.org. This is my own key, but you can leave it
- `TMDB_APIKEY` : API key from themoviedb.org
- `PING_HOSTS` : array containing the hosts to ping randomly
- `TWITTER_SUFFIX` : the content of this variable will be added to the final tweet, at the end
- `DEBUG` : change to `True` to enable the debug log
- `DEBUG_FILE` : filename used to log

Finally, do this command to make the script executable:

	chmod u+x TweetBoxBot.py

To test, simply run the following command in the script directory:

	./TweetBoxBot.py

You should have a tweet on your Twitter account!


By default, if you run `./TweetBoxBot.py`, the script will choose a random function to be executed.  
However, you can perform a especially function, in argument : `./TweetBoxBot.py uptime`.

Here are the available arguments :

- uptime
- cpu_load
- cpu_freq
- cpu_temp 
- mem_load
- kernel
- speedtest
- ping
- time_city
- weather
- gif
- chuck_quote
- ron_quote
- movie
- apod
- numbers
- breakingbadquote
- gameofthronesquote


# Sending tweets automatically

For sending tweets automatically, you need to add a cron job on your machine.

The difficulty was to make sending tweets randomly. For my part, I chose a send period each about 1.5 and 11.5 hours using the following cron job:

	0 5,17 * * * sleep $(( 100 +  $(od -vAn -N2 -tu4 /dev/urandom) \% 600 ))m ; /usr/bin/python /root/TweetBoxBot.py

To explain briefly, every 12 hours (at 5 and 17), the task starts the command `sleep  $((...))m`. It allows to wait a random number of minutes between 100 and 700, so between 1.5 and 11.5 hours!

Finally, after waiting a random delay, the task launches the script TweetBoxBot.py that launch itself a random function and tweets the result!


# The end

You can see the result on Twitter, on [@TweetBoxBot](https://twitter.com/tweetboxbot).

If you have any ideas for improving the script or to add features, please fork the project and do a pull request!

Thanks for reading me ;)

*Twitter account of the creator : [@shevabam](http://twitter.com/shevabam)*

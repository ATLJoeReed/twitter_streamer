# twitter_streamer

This program taps into the Twitter Streaming API and allows you to define keyword(s) to pull out tweets in near realtime. I build this to learn about the twitter API and work with SQLAlchemy. I am saving the extracted tweets into a Postgres database.

To use this program you need to install the requirements and setup a Twitter Developer Account along with a Twitter application. This will get you the four items (see below) you need to access the Twitter Streaming API.

Final setup is to have a file /config/settings.py with the following items.

DB_URL = 'postgres://xxxxxxxx'

TWITTER_APP_KEY = 'xxxxxxxx'
TWITTER_APP_SECRET = 'xxxxxxxx'
TWITTER_KEY = 'xxxxxxxx'
TWITTER_SECRET = 'xxxxxxxx'

You then adjust the keyword(s) in the file /config/twitter_filer.py and then run the streamer.py. As it's running it will be inserting records into the database you are pointing at via the DB_URL.

This is running on Python 3.5.2

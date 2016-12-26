from sqlalchemy import create_engine, MetaData, Table
import tweepy

from config import settings, twitter_filter


metadata = MetaData()

engine = create_engine(settings.DB_URL)

tweets = Table('tweets', metadata, autoload=True, autoload_with=engine)

connection = engine.connect()


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        ins = tweets.insert().values(text=status.text)
        connection.execute(ins)

    def on_error(self, status_code):
        if status_code == 420:
            return False


auth = tweepy.OAuthHandler(
    settings.TWITTER_APP_KEY,
    settings.TWITTER_APP_SECRET
)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=twitter_filter.TRACK_TERMS)

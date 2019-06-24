from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table
import tweepy

from config import settings, twitter_filter


metadata = MetaData(schema='raw')

engine = create_engine(settings.DB_URL)

tweets = Table('dem_debate_20190626', metadata, autoload=True, autoload_with=engine) # noqa

connection = engine.connect()


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        retweeted = False
        tweet = status.text
        original_tweet = None
        if hasattr(status, 'retweeted_status'):
            retweeted = True
            try:
                original_tweet = status.retweeted_status.extended_tweet["full_text"] # noqa
            except AttributeError:
                original_tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text

        try:
            name = status.user.name
            screen_name = status.user.screen_name
            followers_count = status.user.followers_count
            location = status.user.location
            description = status.user.description
            verified_account = status.user.verified
        except AttributeError:
            name = None
            screen_name = None
            followers_count = None
            location = None
            description = None
            verified_account = None

        ins = tweets.insert().values(
            ymd=datetime.now(),
            name=name,
            screen_name=screen_name,
            followers_count=followers_count,
            location=location,
            description=description,
            verified_account=verified_account,
            tweet=tweet,
            retweeted=retweeted,
            original_tweet=original_tweet,
        )
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
stream = tweepy.Stream(
    auth=api.auth,
    listener=stream_listener,
    tweet_mode='extended',
)
stream.filter(track=twitter_filter.TRACK_TERMS)

from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, Text, DateTime, Boolean
)

from config import settings


engine = create_engine(settings.DB_URL)

metadata = MetaData(schema='raw')

tweets = Table(
    'kamala_harris_tweets', metadata,
    Column('ukey', Integer(), primary_key=True),
    Column('ymd', DateTime(timezone=True)),
    Column('name', Text(), nullable=True),
    Column('screen_name', Text(), nullable=True),
    Column('followers_count', Integer(), nullable=True),
    Column('location', Text(), nullable=True),
    Column('description', Text(), nullable=True),
    Column('verified_account', Boolean(), default=False),
    Column('tweet', Text(), nullable=False),
    Column('retweeted', Boolean(), default=False),
    Column('original_tweet', Text(), nullable=True),

)

metadata.create_all(engine)

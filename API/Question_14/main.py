from pathlib import Path
from Question_14.src.tweet import get_tweets
from Question_14.src.sentiment import add_scores
from Question_14.src.util import connect
import pandas as pd

def run(keyword:str,n:int):
    print("Fetching Tweets")
    df=get_tweets(keyword,n)
    
    if df.empty:
        print("Sorry Mate, No Tweets Found!!")
        return 0
    
    print("Runnning Sentiment Analysis........")
    clean_tweet=add_scores(df)

    out=Path("Cleaned_Tweets")
    clean_tweet.to_csv(out,index=False)
    print("Sentiment of the Tweets are extracted!")

    # ======= Data Sent into SQL Server ==============

    try:
        engine=connect()
        columns_to_insert = [col for col in clean_tweet.columns if col != 'RowVer']
        clean_tweet[columns_to_insert].to_sql("X_Sentiment_Data",con=engine,if_exists='append',index=False)
        print("Tweets sent into SQL Server")
    except Exception as e:
        print("Almost there, Just work upon it!",e)


if __name__ == "__main__":
    run("Cricket",10)
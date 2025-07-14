from Question_14.src.twitter import get_client
import re
import pandas as pd

Urls=re.compile(r"http\S+")
Mentions=re.compile(r"@\w+")
Not_Texts=re.compile(r"[^\w\s]")
Multi_Space=re.compile(r"\s+")

def clean(text:str):
    text=Urls.sub("",text)
    text=Mentions.sub("",text)
    text=Not_Texts.sub(" ",text)
    text=Multi_Space.sub(" ",text)
    text=text.replace("#","")

    return text.strip()  #====== Used to remove the headspace and the tailspace from tweet ==========

def get_tweets(keyword:str,n:int):
    client=get_client()

    result=client.search_recent_tweets(
        query=keyword,
        tweet_fields=['created_at','lang'],
        max_results=n
    )   

    rows=[]
    if result.data:
        for tweet in result.data:
            if (tweet.lang =='en'):
                rows.append(
                    {
                        "Tweet_Id":tweet.id,
                        "Tweet":tweet.text,
                        "Clean_Tweet":clean(tweet.text),
                        "Tweet_Posted_At":tweet.created_at
                    }
                )
    return pd.DataFrame(rows) 
                

import pandas as pd
from nltk.sentiment  import SentimentIntensityAnalyzer

analyzer=SentimentIntensityAnalyzer()

def add_scores(df:pd.DataFrame):

    scores=df["Clean_Tweet"].apply(analyzer.polarity_scores)

    scores_df=scores.apply(pd.Series)

    def classify(c):
        if c>0.05:
            return "Positive"
        elif c <-0.05:
            return "Negative"
        else:
            return "Neutral"
    
    scores_df["Sentiment"]=scores_df["compound"].apply(classify)

    return pd.concat([df.reset_index(drop=True),scores_df],axis=1)
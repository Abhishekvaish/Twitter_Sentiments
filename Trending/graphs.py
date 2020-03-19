import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud,STOPWORDS
from io import BytesIO
import base64
from textblob import TextBlob

def get_dataset():
    from urllib import request
    link_csv = 'https://drive.google.com/uc?id=1BY0SXU2zltM2eyKfT8gHUQRElAjx1P1W&export=download'
    response = request.urlopen(link_csv)
    content = response.read().decode('utf8')
    with open('tweets.csv','w',encoding='utf-8',newline='') as f:
        f.write(content)
    return pd.read_csv('tweets.csv')

def getweetstxt():
    with open('tweets.txt','w',encoding='utf-8') as f:
        for i in range(dataset.shape[0]):
            f.write(dataset['topic'][i]+dataset['full_text'][i]+'\n')
    return open('tweets.txt','r',encoding="ascii",errors='ignore').read()

def get_topics():
    context ={}
    for i in dataset['topic'].unique():
        context[i] = dataset[dataset['topic']==i].count()[0]

    return sorted(context.items() ,key=lambda x:x[1])[::-1]


def getIndia():


    twitter_mask=np.array(Image.open('trial2.jfif'))
    twitter_wc = WordCloud(background_color='black', max_words=10000, mask=twitter_mask, stopwords=stopwords,collocations=False)

    # generate the word cloud
    twitter_wc.generate(tweetstxt)

    # display the word cloud
    fig = plt.figure()
    fig.set_figwidth(12) # set width
    fig.set_figheight(12) # set height
    plt.imshow(twitter_wc, interpolation='bilinear')
    plt.axis('off')
    return graphic(fig)
    #return uri(fig)

def getPieChart():
    dataset['count']=1
    piedf=dataset.groupby('topic').sum().sort_values(['count'],ascending=False).head(6)
    dataset.drop(['count'],axis=1,inplace=True)
    colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen','pink']
    explode_list = [0.1, 0.1, 0.1, 0, 0,0]
    piedf['count'].plot(kind='pie',
                            figsize=(15, 6),
                            autopct='%1.1f%%',
                            startangle=90,
                            shadow=True,
                            colors=colors_list,
                            explode=explode_list,
                            labels=None
                            )

    fig=plt.Figure()
    plt.title('TOP HASHTAGS', y=1.12)
    plt.axis('equal')
    plt.ylabel('')
    plt.legend(labels=piedf.index, loc='upper left')

    return graphic(fig)

def graphic(figure):
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close(figure)
    return graphic

def getBar():
    fig=plt.figure()
    fig.set_figwidth(15)
    fig.set_figheight(6)
    ax=dataset['topic'].value_counts().head(10).plot(kind='bar',figsize=(15,6),color='yellow')
    ax.set_xlabel('Hashtags')
    ax.set_ylabel('Tweets')
    return graphic(fig)


def  topic_wordcloud(topic):
    dfc=pd.DataFrame()
    dfc=dataset[dataset['topic']==topic]
    dfc.groupby('topic').sum()
    topictweets=str(dfc['full_text'])
    twitter= WordCloud(background_color='white',    max_words=1000,stopwords=stopwords ,collocations=False)
    twitter.generate(topictweets)
    fig = plt.figure()
    fig.set_figwidth(12)
    fig.set_figheight(12)
    plt.imshow(twitter, interpolation='bilinear')
    plt.axis('off')
    return graphic(fig)

def topic_sentiment(topic):
    cdf=dataset[dataset['topic']==topic]
    cdf.reset_index(inplace=True)
    possitive=0
    negative=0
    neutral=0
    for i in range(cdf.shape[0]):
        analysis = TextBlob(cdf['full_text'][i])
        if analysis.sentiment.polarity > 0:
            possitive=possitive+1
        elif analysis.sentiment.polarity == 0:
           neutral=neutral+1
        else:
            negative=negative+1
    sentdf=pd.DataFrame()
    sentdf['type']=['possitive','neutral','negative']
    sentdf.set_index('type',inplace=True)
    sentdf['count']=[possitive,neutral,negative]
    fig=plt.figure()
    fig.set_figwidth(12)
    fig.set_figheight(12)
    sentdf.plot(kind='bar',figsize=(10, 6),color=('lightblue','orange','red'))
    plt.xlabel('emotion')
    plt.ylabel('No of tweets')
    plt.title(f"Sentiments for {cdf['topic'][0]}")
    return graphic(fig)

#if __name__ == '__main__':
dataset = pd.read_csv('tweets.csv')#get_dataset()
tweetstxt = getweetstxt()
stopwords=set(STOPWORDS)
stopwords.add('amp')
stopwords.add('will')

india = getIndia()
piechrat = getPieChart()
bargraph = getBar()



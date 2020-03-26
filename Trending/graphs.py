import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud,STOPWORDS
from io import BytesIO
import base64
from textblob import TextBlob


#########prerequisite############
def get_dataset():
    from urllib import request
    link_csv = 'link'
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
def graphic(figure):
    buffer = BytesIO()
    plt.savefig(buffer, format='png',bbox_inches = 'tight',pad_inches = 0)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.clf()
    return graphic

########topics###############
def get_topics():
    context ={}
    for i in dataset['topic'].unique():
        context[i] = dataset[dataset['topic']==i].count()[0]

    return sorted(context.items() ,key=lambda x:x[1])[::-1]

########Home################
def getIndia():

    twitter_mask=np.array(Image.open('trial2.jfif'))
    twitter_wc = WordCloud(background_color='black', max_words=10000, mask=twitter_mask, stopwords=stopwords,collocations=False)
    # generate the word cloud
    twitter_wc.generate(tweetstxt)

    # display the word cloud
    fig = plt.figure()
    fig.set_figwidth(9) # set width
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
                            figsize=(10,6),
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
def getBar():
    fig=plt.figure()
    ax=dataset['topic'].value_counts().head(10).plot(kind='bar',figsize=(10.5,4),color='blue')
    ax.set_xlabel('Hashtags')
    ax.set_ylabel('Tweets')
    return graphic(fig)

########topicgraph#########
def topic_graph(topic):
    context = {}
    dfc=dataset[dataset['topic']==topic]
    dfc.reset_index(inplace=True)
    #################wordcloud######################
    topictweets=str(dfc['full_text'])
    twitter= WordCloud(background_color='black',    max_words=1000,stopwords=stopwords ,collocations=False)
    twitter.generate(topictweets)
    fig = plt.figure()
    fig.set_figwidth(12)
    fig.set_figheight(12)
    plt.imshow(twitter, interpolation='bilinear')
    plt.axis('off')
    context['fig1'] = graphic(fig)
    ##################SENTIMENTS#####################
    possitive,negative,neutral=0,0,0
    for i in range(dfc.shape[0]):
        analysis = TextBlob(dfc['full_text'][i])
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
    ####################BARGRAPH########################
    fig=plt.figure()
    sentdf.plot(kind='bar',figsize=(10, 6),color=('lightblue','orange','red'))
    plt.xlabel('emotion')
    plt.ylabel('No of tweets')
    plt.title(f"Sentiments for {topic}")
    context['fig2'] = graphic(fig)
    ####################PIECHART##########################
    sentdf['count'].plot(kind='pie',autopct='%1.1f%%',startangle=90,figsize=(10,6),
                            shadow=True,
                            colors=['skyblue','yellow','red'],
                            explode=[0.1,0,0],
                             labels=None)

    fig = plt.Figure()
    plt.title('Overall Sentiment', y=1.12)
    plt.axis('equal')
    plt.ylabel('')
    plt.legend(labels=sentdf.index, loc='upper left')
    context['fig3'] = graphic(fig)
    ###################DAYBARGRAPGH########################
    listhour=[int(i[3:5]) for i in dfc['time'].tolist()]
    listhour=sorted(listhour)
    binsh=np.arange(listhour[0],listhour[len(listhour)-1],1)

    fignewhour=plt.figure()
    plt.hist(listhour, bins=binsh, alpha=0.5)
    plt.title('hour graph for'+topic)
    plt.xlabel('hour')
    plt.ylabel('No of tweets')
    context['fig4'] = graphic(fignewhour)
    return context


dataset = pd.read_csv('tweets.csv')#get_dataset()
tweetstxt = getweetstxt()
stopwords=set(STOPWORDS)
stopwords.add('amp')
stopwords.add('will')

india = getIndia()
piechrat = getPieChart()
bargraph = getBar()
topics = get_topics()



from django.shortcuts import render
import plotly
import plotly.tools as tls
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from . import graphs
List= graphs.topics


def index(request):
    context = {'fig2': graphs.bargraph,'fig1':graphs.india,'fig3':graphs.piechrat}
    return render(request, 'Trending/index.html',context)


def topics(request):
    context ={'context':List}
    return render(request,'Trending/topics.html', context)


def about(request):
    fig, ax = plt.subplots()
    ax.plot([1, 3, 4], [3, 2, 5])
    plotly_fig = tls.mpl_to_plotly(fig)
    graph_div = plotly.offline.plot(plotly_fig, auto_open=False, output_type="div")
    return render(request,'Trending/about.html', {'fig':graph_div})


def detail(request, id):
    topic = List[id-1][0]
    g = graphs.topic_day(topic)
    context = {
        'topic':topic,
        'fig1':graphs.topic_wordcloud(topic),
        'fig2':graphs.topic_sentiment(topic),
        'fig3':g[0],'fig4':g[1],

    }
    return render(request,'Trending/detail.html',context)


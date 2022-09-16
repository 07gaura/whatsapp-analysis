from urlextract import URLExtract
from wordcloud import WordCloud
from english_words import english_words_set
from stop_words import get_stop_words
import emoji
stop_words = get_stop_words('en')
stop_words = get_stop_words('english')
extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df["user"] == selected_user]
    num_messages = df.shape[0]
    num_media = df[df["msg"] == ' <Media omitted>'].shape[0]
    words = []
    for message in df["msg"]:
        words.extend(message.split())

    links=[]
    for message in df["msg"]:
        links.extend(extract.find_urls(message))
    return num_messages,len(words),num_media,len(links)

def most_busy_user(df):
    x = df["user"].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={"index":"name","user":'percent'}
    )
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    df.drop(df[df['msg'] ==' <Media omitted>'].index, inplace=True)
    words = []
    for message in df["msg"]:
        for i in message.lower().split(" "):
            if len(i) > 2 and i in english_words_set and i not in stop_words:
                words.append(i)
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['msg'].str.cat(sep=" "))
    return df_wc,words

def emoji_count(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    emojis = []
    for message in df['msg']:
        for c in message:
            if emoji.is_emoji(c):
                emojis.extend(c)
    return emojis

def msg_timeline(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['msg'].reset_index()
    line=[]
    for i in range(timeline.shape[0]):
        line.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=line
    return timeline

def daily_timeline(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    daily_time=df.groupby('only_date').count()['msg'].reset_index()
    return daily_time

def hour_timeline(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    hour_time=df.groupby('hour').count()['msg'].reset_index()
    return hour_time

def weeekly_activity(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def monthly_activity(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
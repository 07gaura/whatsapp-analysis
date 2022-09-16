import pandas as pd
import streamlit as st
from preprocessing import data_extraction
from collections import Counter
import helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = data_extraction(data)
    st.dataframe(df)
    user_list = df["user"].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        total_msg,words,media,links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total_msg)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(media)
        with col4:
            st.header("Total Links Shared")
            st.title(links)
        if selected_user =="Overall":
            st.title('Most Busy Users')
            x,y= helper.most_busy_user(df)
            fig,ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(y.head())
        #word analysis
        st.title("Mostly Used Words")
        df_wc,word_data = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)
        word_df = pd.DataFrame(Counter(word_data).most_common(20))
        word_df = word_df.rename(
            columns={0: "word", 1: 'count'}
        )
        fig,ax = plt.subplots()
        ax.barh(word_df["word"],word_df["count"])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emojis analysis
        emoji_data = helper.emoji_count(selected_user,df)
        emoji_df = pd.DataFrame(Counter(emoji_data).most_common(len(Counter(emoji_data))))
        emoji_df = emoji_df.rename(columns={0:"emojis",1:"count"})

        col1,col2 = st.columns(2)
        with col1:
            st.title("Mostly used Emojis DataFrame")
            st.dataframe(emoji_df)
        with col2:
            st.title("Mostly used Emojis")
            emoji_df = emoji_df.head()
            fig, ax = plt.subplots()
            ax.pie(emoji_df["count"],labels=emoji_df["emojis"])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title("Monthly Time Line")
        timeline = helper.msg_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline["time"],timeline['msg'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Time Line")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily["only_date"], daily['msg'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Time Line")
        hour = helper.hour_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(hour["hour"], hour['msg'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Weekly Activity")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weeekly_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Day")
            busy_month = helper.monthly_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
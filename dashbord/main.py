import streamlit as st
from dataset import dataset
import streamlit as st
import plotly.graph_objects as go    
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_visual_pie(value,label,title):
    fig = go.Figure(data=[go.Pie(labels=label,values=value)])
    fig.update_layout(title=title)
    return fig

def create_visual_bar(value,label,title):
    fig=go.Figure(data=[go.Bar(x=label,y=value)])
    fig.update_layout(title=title)
    return fig

def generate_wordcloud(text,background_color:str='white',title=None):
    if title==None:
        st.title("gak tahu")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    wordcloud=WordCloud(background_color=background_color).generate(str(text.values))
    image = wordcloud.to_image()
    st.image(image)

def get_genre(row, pilih_genre):
    for i in range(1, 11):
        genre_col = 'genre' + str(i)
        genre = row[genre_col]
        if genre == pilih_genre:
            return genre
        elif pd.isnull(genre):
            break
    return None


def main():
    df=dataset('../mentahan.csv')
    df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce')
    tag=dataset('../gabung_tag.csv')
    genre_count=df['genre1'].value_counts().reset_index()
    genre_count.columns=['genre','Count']
    genre_pie=create_visual_pie(genre_count['Count'],genre_count['genre'],"Percentage Genre")
    genre_bar=create_visual_bar(genre_count['Count'],genre_count['genre'],"Genre Count")
    st.set_page_config(layout='wide')
    st.markdown("<h1 style='text-align: center;'>Movie Lens Dashboard</h1>"
                , unsafe_allow_html=True)
    genre_plot1,genre_plot2=st.columns([2,2])
    with genre_plot1:
        st.plotly_chart(genre_pie,width=300)  

    with genre_plot2:
        st.plotly_chart(genre_bar,width=300)

    unique_tag=df['genre1'].unique()
    pilih_genre=st.selectbox("Genre",unique_tag)
    text_tag=tag[tag['genre1']== pilih_genre]['tag']
    

    # ini untuk genre populer
    genre_pop=df.groupby(['genre1','year'])['avg_rating'].mean().reset_index()
    genre_pop = pd.DataFrame(genre_pop)
    choice_pop=genre_pop[genre_pop['genre1']== pilih_genre]
    choice1,choice2=st.columns([2,2])
    with choice1:
        generate_wordcloud(text_tag,title=pilih_genre)   
    with choice2:
        st.line_chart(data=choice_pop,x='year',y='avg_rating')
    # tho show film
    top10_mov = df.sort_values(by='rating_count', ascending=False)
    top10mov = top10_mov[top10_mov.apply(lambda row: True if get_genre(row, pilih_genre) is not None else False, axis=1)]
    cols = ['movieId', 'title']
    choice_top = top10mov[cols]
    st.dataframe(choice_top)
    
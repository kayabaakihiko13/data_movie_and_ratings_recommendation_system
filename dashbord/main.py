import streamlit as st
from dataset import dataset
import streamlit as st
import plotly.graph_objects as go    
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
    plt.imshow(wordcloud)
    st.pyplot()

def main():
    df=dataset('../mentahan.csv')
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
    
    unique_tag=tag['genre1'].unique()
    pilih_genre=st.selectbox("Genre",unique_tag)
    text_tag=tag[tag['genre1']== pilih_genre]['tag']
    
    if st.button("Buat Wordcloud"):
        generate_wordcloud(text_tag,title=pilih_genre)   

import streamlit as st
import pandas as pd 
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import statistics as stats
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.switch_page_button import switch_page
import sys
import math as m
#sys.path.insert(1,'//Users//reema//Desktop//Grad Project//Streamlit//app.py//streamlit_option_menu')
from streamlit_option_menu import option_menu
import flagpy as fp


st.set_page_config(page_title='iCanViz',page_icon='//Users//reema//Desktop//Grad Project//Streamlit//Logos//logo_rotated.png',layout='wide')

DSUC9=pd.read_csv('//Users//reema//Desktop//Grad Project //Streamlit//pages//DSUC9.csv')

def spaces(num):
  for i in range(num):
    st.write('\n')

def calc(df):
  lst=[]
  site=df.cause_name.unique()
  for i in site:
      lst.append(df[df['cause_name']==i]['val'].sum(skipna=True))
  return lst,site


a1,a2=st.columns(2)
with a1:
    image = Image.open('//Users//reema//Desktop//Grad Project //Streamlit//new.png')
    st.image(image,width=300) #Logo
with a2:
    s1,s2,s3=st.columns([0.1,0.1,0.1])
    with s1:
          #spaces(2)
          image = Image.open('//Users//reema//Desktop//Grad Project //Streamlit//Logos//GA4DH.jpg')
          spaces(3)
          image_r = image.resize((50, 50))
          st.image(image_r) 
    with s2: 
          spaces(3)        
          image = Image.open('//Users//reema//Desktop//Grad Project //Streamlit//Logos//psut.jpeg')
          image_r = image.resize((50, 50))
          st.image(image_r)
    with s3:
          spaces(3)
          image = Image.open('//Users//reema//Desktop//Grad Project //Streamlit//Logos//ain.png')
          image_r = image.resize((50, 50))
          st.image(image_r) 

selected= option_menu(menu_title=None,options=['Home','About','Mortality','Survivals','Risks','YLD','Login','Contact Us'],icons=['house','info-circle','graph-down','graph-up','file-medical','stopwatch','person','envelope'],orientation='horizontal',menu_icon='cast',default_index=4)
st.markdown('---')

if selected =='Home':
    switch_page('Main')
elif selected =='About':
    switch_page('Main')
elif selected =='Mortality':
    switch_page('Deaths')
elif(selected=='Survivals'):
    switch_page('Survivals')
elif(selected=='YLD'):
    switch_page('YLD')
elif selected =='Login':
    switch_page('Main')

st.write('\n')
st.markdown("<h1 style='text-align: center;'> Risks </h1>", unsafe_allow_html=True)
spaces(3)

col3,col4,col5 = st.columns(3)

with col3:
    st.metric(label="Number of Cancer Sites",value=22)
with col4:
    st.metric(label="Number Of Arab Countries",value=21)
with col5:
    st.metric(label="Risk Factors",value='HDI Index, Smoking')
style_metric_cards(border_left_color='#f04b4c')
spaces(3)

st.header('Risk Factor')
spaces(2)
tab1, tab2,  = st.tabs(["HDI", "Obesity"])
with tab1:
    spaces(2)
    st.subheader('HDI')
    spaces(2)
    col1,col2=st.columns(2)

    with col1:
        fig = px.pie(DSUC9, values=list(DSUC9['HDI_Classes'].value_counts()), names=DSUC9['HDI_Classes'].unique() , width=600, height=500,title='HDI Categories Distribution In The Arab World')
        st.plotly_chart(fig)
    with col2:
        view=st.radio('Select a view',('Cancer Sites','Countries'),horizontal=1)
        if view=='Cancer Sites':
            xx,yy=calc(DSUC9)
            fig = px.bar(DSUC9, y=yy, x=xx, orientation='h',title="Total Incidence Rate Per Cancer Site Across Arab Countries", width=600, height=500,labels={'y':'Cancer Site','x':'Total Incidence Rate'})
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig)
        else:
            total=DSUC9[DSUC9['cause_name']=='Total cancers']
            fig = px.box(total, x='Entity',y='val',hover_data=['Entity','Year'], title=f"Total Incidence Rate Per Arab Country", width=600, height=500,labels={'Avg_yrs_schooling':'Average Years of Schooling','val':'Total Incidence Rate'})
            st.plotly_chart(fig)

    fig = px.bar(DSUC9, y='val', x='cause_name',color='HDI_Classes',hover_data=['Entity'],barmode='group', title="Total Incidence Rate Per Cancer Site Across Arab Countries Factored Over HDI Categories", width=1300, height=600,labels={'cause_name':'Cancer Site','val':'Total Incidence Rate'})
    fig.update_traces(dict(marker_line_width=0))
    st.plotly_chart(fig)


    with st.expander('Per country'):
        st.write('hi')
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
from scipy.stats import sem
#sys.path.insert(1,'//Users//reema//Desktop//Grad Project//Streamlit//app.py//streamlit_option_menu')
from streamlit_option_menu import option_menu
import flagpy as fp


st.set_page_config(page_title='iCanViz',page_icon='//Users//reema//Desktop//Grad Project//Streamlit//Logos//logo_rotated.png',layout='wide')

DSUC10=pd.read_csv('//Users//reema//Desktop//Grad Project //Streamlit//pages//DSUC10.csv')

def spaces(num):
  for i in range(num):
    st.write('\n')

def calc(df,option,year):
  ycol=DSUC10.cause_name.unique()
  lst=[] 
  if year==None:
      for i in ycol:
        num=df[(df[option]==i)]['val'].mean()
        num_form="{:.2f}".format(num)
        lst.append(num_form)
      return lst,ycol
  else: 
    for i in ycol:
      num=df[(df['year']==year) & (df[option]==i)]['val_y'].mean()
      num_form="{:.2f}".format(num)
      lst.append(num_form)
    return lst,ycol

def calc_mean_site(df,site):
    sliced=df[df['cause_name']==site]
    lst=[]
    years=sliced.year.unique()
    for i in years:
        lst.append(sliced[sliced['year']==i]['val_y'].mean())
    return lst,years

def calc_mean(df,country):
  sliced=df[df['location_name']==country]
  lst=[]
  years=sliced.year.unique()
  for i in years:
    lst.append(sliced[sliced['year']==i]['Average'].mean())
  return lst,years

def error_country(df,country):
    errors=[]
    df_country=df[df['location_name']==country]
    for i in df_country.year.unique():
        errors.append(sem(df_country[(df_country['year']==i)]['val_y']))
    return errors

def error_site(df,site):
    errors=[]
    df_country=df[df['cause_name']==site]
    for i in df_country.year.unique():
        errors.append(sem(df_country[(df_country['year']==i)]['val_y']))
    return errors

def line(df,l1,l2,i):
  err=error_country(df,i)
  fig = px.scatter(df, x=l2, y=l1,error_y=err,labels={'y':'Average Number of Years Lost to Disability (YLD)','x':'Year'},height=500,width=600,
              title=f"Average Number of Years Lost to Disability (YLD) in {i} (1990-2019)")
  st.plotly_chart(fig)

def line_site(df,l1,l2,i):
  err=error_site(df,i)
  fig = px.scatter(df, x=l2, error_y=err,y=l1,labels={'y':'Average Number of Years Lost to Disability (YLD)','x':'Year'},height=500,width=600)
  st.plotly_chart(fig)

def bar(df,country,year):
    dfc=df[(df['location_name']==country) & (df['year']==year)]
    fig = px.bar( y=dfc['cause_name'], x=dfc['val_y'], orientation='h',labels={'x':'Number of Years Lost to Disability (YLD)','y':'Cancer Site'},height=600,width=600,
              title=f" Number of Years Lost to Disability (YLD) in {country} {year}")
    fig.update_layout( plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)

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
    

selected= option_menu(menu_title=None,options=['Home','About','Mortality','Survivals','Risks','YLD','Login','Contact Us'],icons=['house','info-circle','graph-down','graph-up','file-medical','stopwatch','person','envelope'],orientation='horizontal',menu_icon='cast',default_index=5)

st.markdown("-----")
if selected =='Home':
    switch_page('Main')
elif selected =='About':
    switch_page('Main')
elif selected =='Mortality':
    switch_page('Deaths')
elif(selected=='Survivals'):
    switch_page('Survivals')
elif selected =='Login':
    switch_page('Main')
elif selected =='Risks':
    switch_page('Risks')

st.write('\n')
st.markdown("<h1 style='text-align: center;'> Years Lost to Disability </h1>", unsafe_allow_html=True)
spaces(3)


st.write('\n')
st.write('\n')
col3,col4,col5 = st.columns(3)

with col3:
    st.metric(label="Number of Cancer Sites",value=30)
with col4:
    st.metric(label="Number Of Arab Countries",value=20)
with col5:
    st.metric(label="Time Period",value=f" 30 Years (1999-2019)")
style_metric_cards(border_left_color='#f04b4c')
spaces(3)

c1,c2=st.columns(2)

with c1:
    year=st.slider("Select a year", 1990, 2019,key=1)
    xx,yy=calc(DSUC10,'cause_name',year)
    fig = px.bar( x=xx, y=yy, orientation='h',labels={'y':'Cancer Sites','x':'Average Number of Years Lost to Disability'},height=500,width=600,
              title=f"Average Number of Years Lost to Disability Per Cancer Site In The Arab World In {year} ",text_auto=True)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
    st.plotly_chart(fig)
with c2:
    view=st.radio('Select a view',('Cancer Sites','Countries'),horizontal=1)
    st.write('hi')

spaces(3)
tab1,tab2,tab3=st.tabs(['Arab Countries','Cancer Sites','YLD Forecasting'])

with tab1:
    st.header('Arab Countires')
    spaces(2)
    country= st.selectbox( 'Select A Country', (DSUC10['location_name'].unique()),key=2)
    spaces(3)
    st.subheader(f'{country}')
    
    s1,s2=st.columns(2)
    with s1:
        lst,yy=calc_mean(DSUC10,country)
        spaces(5)
        line(DSUC10,lst,yy,country)
    with s2:
        year=st.slider("Select a year", 1990, 2019,key=4)
        bar(DSUC10,country,year)
with tab2:
    c1,c2=st.columns(2)
    with c1:
        st.header('Cancer Sites')
        spaces(1)
        site= st.selectbox( 'Select Cancer Site', (DSUC10['cause_name'].unique()),key=3)
        spaces(2)
    with c2:
         spaces(6)
         ans = st.selectbox('Select Country',(DSUC10.location_name.unique()),key=77)
    c3,c4=st.columns(2)    
    with c3:
        sliced=DSUC10[DSUC10['location_name']==ans]
        lst,yy=calc_mean_site(sliced,site)
        st.subheader(f'Number of Years Lost to Disability for {site} in  {ans} (1990 - 2019)')
        line_site(sliced,lst,yy,site)
        spaces(2)
    with c4:
        num=DSUC10.year.unique()
        begin=st.selectbox('Select the year you are  interested in',(num)) 
        start=st.selectbox('Select the year you want to compare it with',(num)) 
        delt= DSUC10[(DSUC10['year']==begin)& (DSUC10['location_name']==ans)][site].iloc[0] / DSUC10[(DSUC10['Year']==start) & (DSUC10['Entity']==ans)][site].iloc[0]
        change= DSUC10[(DSUC10['year']==begin)& (DSUC10['location_name']==ans)][site].iloc[0] - DSUC10[(DSUC10['Year']==start) & (DSUC10['Entity']==ans)][site].iloc[0]
        delt_r="{:.2f}".format(delt)
        change_r="{:.2f}".format(change)
        st.metric('Rate Of Change',value=f'Rate: {delt_r}',delta=change_r)
    
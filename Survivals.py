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

DSUC1=pd.read_csv('//Users//reema//Desktop//Grad Project //Streamlit//pages//DSUC1.csv')

def spaces(num):
  for i in range(num):
    st.write('\n')


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
selected= option_menu(menu_title=None,options=['Home','About','Mortality','Survivals','Risks','YLD','Login','Contact Us'],icons=['house','info-circle','graph-down','graph-up','file-medical','stopwatch','person','envelope'],orientation='horizontal',menu_icon='cast',default_index=3)

st.markdown("-----")

if selected =='Home':
    switch_page('Main')
elif selected =='About':
    switch_page('Main')
elif selected =='Login':
    switch_page('Main')
elif(selected=='Risks'):
    switch_page('Risks')
elif(selected=='YLD'):
    switch_page('YLD')
elif(selected=='Mortality'):
    switch_page('Deaths')
elif selected =='Contact Us':
    switch_page('Main')

def error(df,country):
  er=[]
  sites=['Breast','Cervix','Colon','Leukaemia',	'Liver',	'Lung'	,'Ovary',	'Prostate',	'Rectum',	'Stomach']
  if country!='Qatar':
    for y in df.Year.unique():
        er.append(stats.stdev(df[(df['Year']==y)&(df['Entity']==country)][sites].values.ravel()) / m.sqrt(len(df[(df['Year']==y) &(df['Entity']==country) ][sites].values.ravel())))
    return er

def calc(df,year):
  ycol=['Breast',	'Cervix','Colon','Leukaemia',	'Liver',	'Lung'	,'Ovary',	'Prostate',	'Rectum',	'Stomach']
  lst=[] 
  if year==None:
    
      for i in df.iloc[:,4:14].columns:
        lst.append(df[i].mean(skipna=True))
      return lst,ycol
  else: 
    for i in df.iloc[:,4:14].columns:
      lst.append(df[df['Year']==year][i].mean(skipna=True))
    return lst,ycol

def countries(countr):
  df=arab.copy()
  errors=error(df,countr)
  duration=["1995-1999","2000-2004","2005-2009"]
  country={'Algeria':[], 'Jordan':[], 'Qatar':[], 'Saudi Arabia':[]}
  for y in arab.Year.unique():
    for i in arab.Entity.unique():
      result=arab[(arab['Entity']==i) & (arab['Year']==y)]['Avg_survival_per_year']
      if  result.empty ==True:
          country[i].append(None)
      else:
          country[i].append(result.iloc[0])

  #demo=df[df['Entity']==countr]
  new=pd.DataFrame(country).T.reset_index()
  new.rename(columns={'index':'Entity',0:"1995-1999",1:"2000-2004",2:"2005-2009"},inplace=True)
  vals=new[new['Entity']==countr].values[0,1:]
  fig=px.scatter(x=duration,y=vals,labels={'y':'Average Survival Percentage','x':'Duration'}, error_y=errors,
           title=f"Average Cancer Survival Percentages In {countr} Across All Cancer Sites 1995 - 2009",width=550,height=500)
  st.plotly_chart(fig)
  st.caption('*Whiskers represent standard error')

def sites(ans,year):
  
    ycol=['Breast',	'Cervix','Colon','Leukaemia',	'Liver',	'Lung'	,'Ovary',	'Prostate',	'Rectum',	'Stomach']
    filtered2=arab[(arab['Entity']==ans) & (arab['Year']==year)].iloc[:,4:14].values.ravel()
   
    fig = px.scatter( x=ycol,y=filtered2,labels={'x':'Cancer Sites','y':'Survival Percentages'},
              title=f"Cancer Survival Percentage Per Cancer Site In {ans} From {year-4} - {year}",height=500,width=550)
    #fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
    #fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)

def box(arab):
    ycol=['Breast',	'Cervix','Colon','Leukaemia',	'Liver',	'Lung'	,'Ovary',	'Prostate',	'Rectum',	'Stomach']
    fig=px.box(arab,y=ycol, labels={'value':'Cancer Survival Percentage',"Entity":'Country','variable':'Cancer Site'}, height=400,width=500)
    st.plotly_chart(fig)

def bar(i):
  fig = px.bar(arab,y=i,x='Year',color='Entity',labels={i:f"{i} Cancer Survival Precentage","Entity":'Country'},
    title=f"Cancer Survival Percentage per Cancer Site Across Arab Countries <br><sup>iCanViz Research and Development Project 2023 - DA4DH and PSUT - Prof.Mohammad Odeh, Dr.Serin Atiani, Mahmoud Saber, Reema Maen</sup>", 
    text_auto=True)
  fig.update_xaxes(type='category')
  st.plotly_chart(fig)

arab= DSUC1[(DSUC1['Entity']=='Algeria')|(DSUC1['Entity']=='Jordan') | (DSUC1['Entity']=='Qatar') | (DSUC1['Entity']=='Saudi Arabia') ]
notarab=DSUC1[~ ((DSUC1['Entity']=='Algeria')|(DSUC1['Entity']=='Jordan') | (DSUC1['Entity']=='Qatar' )| (DSUC1['Entity']=='Saudi Arabia'))]
st.write('\n')
st.write('\n')
st.markdown("<h1 style='text-align: center;'> Survivals </h1>", unsafe_allow_html=True)
st.write('\n')
st.write('\n')

col3,col4,col5 = st.columns(3)
with col3:
    st.metric(label="Number of Cancer Sites",value=10)
with col4:
    st.metric(label="Number Of Arab Countries",value=4)
with col5:
    st.metric(label="Time Period",value=f"15 Years (1995-2009)")
style_metric_cards(border_left_color='#f04b4c')
spaces(3)

st.markdown(
    f'''
    <style>
        section[data-testid="stSlider"] .css-ng1t4o {{width: 15rem;}}
    </style>
    ''',
    unsafe_allow_html=True
)

col1,col2 = st.columns(2)
with col1:
    spaces(7)
    st.subheader('Cancer Survival Percentages Accross Cancer Sites 1995-2009')
    box(arab)

with col2:
    year2=st.slider("Select a year", 1999, 2009, step=5,key=2,)
    st.subheader(f'Cancer Survival Percentages Accross Cancer Sites From {int(year2)-4} - {year2}')
    demo=arab[arab['Year']==year2]
    box(demo)

st.write('----')
tab1, tab2,  = st.tabs(["All Countries", "Per Country"])
with tab1:
    spaces(2)
    st.subheader('Cancer Survival Percentages Accross Arab Countriies Per Cancer Site 1995-2009')
    demo=arab[arab['Entity']!='Qatar']
    ycol=['Breast',	'Cervix','Colon','Leukaemia',	'Liver',	'Lung'	,'Ovary',	'Prostate',	'Rectum',	'Stomach']
    fig=px.box(demo,y=ycol,color='Entity',labels={'value':'Cancer Survival Percentage',"Entity":'Country','variable':'Cancer Site'},height=500,width=1300)
    st.plotly_chart(fig)    
    st.caption('Please note that Qatar was not included in this graph because of its data insufficiency')
    spaces(2)

#with st.expander('Explore'):
with tab2:
    spaces(2)
    ans = st.selectbox( 'Select Country', ('Algeria','Jordan',	'Qatar', 'Saudi Arabia'))
    spaces(2)
    c1,c2=st.columns(2)

    with c1:
        st.write('\n')
        if (ans=='Jordan' ):
           st.header(f'{ans}*')
           st.caption('*Values for years 1995-1999 were extrapolated')
        elif (ans=='Saudi Arabia'):
            st.header(f'{ans}*')
            st.caption('*Values for years 2005-2009 were extrapolated')
        else:
            st.header(f'{ans}')
        st.write('\n')
        arab['Year']=arab['Year'].astype('object')
        countries(ans)
    with c2:
        year=st.slider("Select a year", 1999, 2009,step=5,key=3)
        sites(ans,year)
    
spaces(5)
st.write("-----")
st.caption('Data source: https://ourworldindata.org/grapher/five-year-survival-rates-by-cancer-type?time=latest')
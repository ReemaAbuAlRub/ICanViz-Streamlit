import streamlit as st
import pandas as pd 
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.switch_page_button import switch_page
import sys
#sys.path.insert(1,'//Users//reema//Desktop//Grad Project//Streamlit//app.py//streamlit_option_menu')
from streamlit_option_menu import option_menu
import flagpy as fp

st.set_page_config(page_title='iCanViz',page_icon='//Users//reema//Desktop//Grad Project //Streamlit//Logos//logo_rotated.png',layout='wide')

def spaces(num):
  for i in range(num):
    st.write('\n')d

a1,a2=st.columns(2)
with a1:
    image = Image.open('//Users//reema//Desktop//Grad Project //Streamlit//new.png')
    st.image(image,width=300) #Logo
with a2:
    s1,s2,s3=st.columns([0.1,0.1,0.1])
    with s1:
          image = Image.open('//Users//reema//Desktop//Grad Project //Streamlit//Logos//GA4DH.jpg')
          spaces(3)
          image_r = image.resize((50, 50))
          st.image(image_r)
          st.caption(' GA4DH')
    with s2: 
          spaces(3)        
          image = Image.open('//Users//reema//Desktop//Grad Project //Streamlit//Logos//psut.jpeg')
          image_r = image.resize((50, 50))
          st.image(image_r)
          st.caption('  PSUT')
    with s3:
          spaces(3)
          image = Image.open('//Users//reema//Desktop//Grad Project //Streamlit//Logos//ain.png')
          image_r = image.resize((50, 50))
          st.image(image_r) 
          st.caption('Al Ain University')
selected= option_menu(menu_title=None,options=['Home','About','Deaths','Survivals','Login','Contact Us'],icons=['house','info-circle','graph-down','graph-up','person','envelope'],orientation='horizontal',menu_icon='cast',default_index=2)
st.markdown("-----")

if selected =='Home':
    switch_page('Main')
elif selected =='About':
    switch_page('Main')
elif selected =='Login':
    switch_page('Main')
elif selected =='Survivals':
    switch_page('Survivals')
elif selected =='Contact Us':
    switch_page('Main')

DSUC5=pd.read_csv('//Users//reema//Desktop//Grad Project //Streamlit//pages//DSUC5.csv')

#arab= DSUC1[(DSUC1['Entity']=='Algeria')|(DSUC1['Entity']=='Jordan') | (DSUC1['Entity']=='Qatar') | (DSUC1['Entity']=='Saudi Arabia') | (DSUC1['Entity']=='Tunisia')]
#notarab=DSUC1[~ ((DSUC1['Entity']=='Algeria')|(DSUC1['Entity']=='Jordan') | (DSUC1['Entity']=='Qatar' )| (DSUC1['Entity']=='Saudi Arabia') | (DSUC1['Entity']=='Tunisia'))]
st.write('\n')
st.write('\n')
st.markdown("<h1 style='text-align: center;'> Deaths </h1>", unsafe_allow_html=True)
st.write('\n')
st.write('\n')


def calc(df,year):
  ycol=['Prostate', 'Breast', 'Uterine', 'Bladder',
       'Cervical', 'Kidney', 'Stomach', 'Nasopharynx', 'Testicular',
       'Other pharynx', 'Esophageal', 'Non-melanoma skin', 'Pancreatic',
       'Tracheal, bronchus, and lung', 'Lip and oral cavity',
       'Colon and rectum', 'Gallbladder and biliary tract', 'Liver', 'Larynx',
       'Ovarian', 'Thyroid', 'Brain and central nervous system']
  lst=[] 
  if year==None:
      for i in ycol:
        num=df[i].mean(skipna=True)
        num_form="{:.2f}".format(num)
        lst.append(num_form)
      return lst,ycol
  else: 
    for i in ycol:
      num=df[df['Year']==year][i].mean(skipna=True)
      num_form="{:.2f}".format(num)
      lst.append(num_form)
    return lst,ycol

def countries(country):
    filtered=arabs[arabs['Entity']==country]
    fig = px.line(filtered, x="Year", y='Avg_death_per', title=f"Cancer Mortality Rate in {country} From 1990 - 2019",labels={"Avg_death_per":'Average Death Rate'},height=500,width=600)
    fig.update_xaxes( dtick="M1", tickformat="%b\n%Y")
    st.plotly_chart(fig)

def sites(ans,year2):
        filtered=arabs[arabs['Entity']==ans]
        xx,yy=calc(filtered,year2)
        fig = px.bar( x=xx, y=yy, orientation='h',labels={'y':'Cancer Sites','x':'Death Rates'},
              title=f"Cancer Mortality Rate Per Cancer Site In {ans} {year2}",height=500,width=600,text_auto=True)
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig)


def line(ans,site):
    filtered=arabs[arabs['Entity']==ans]
    avg=filtered[site].mean()
    avg_form="{:.2f}".format(avg)
    fig = px.line(filtered, y=site,x='Year',width=600,height=500,labels={site:f'{site} Cancer Mortality Rate'},title=f'{site} Cancer Mortality Rates In {ans}  From 1990 - 2019 ')
    fig.add_hline(y=avg_form,line_dash="dash", line_color="#F04B4C")
    st.plotly_chart(fig)




DSUC5.columns=DSUC5.columns.str.replace(r'cancer','')
DSUC5.columns=DSUC5.columns.str.strip()
arabs= DSUC5[(DSUC5['Entity']=='Algeria')|(DSUC5['Entity']=='Bahrain')|(DSUC5['Entity']=='Egypt')|(DSUC5['Entity']=='Iraq')|(DSUC5['Entity']=='Kuwait')|(DSUC5['Entity']=='Lebanon')|(DSUC5['Entity']=='Libya')|(DSUC5['Entity']=='Mauritania')|(DSUC5['Entity']=='Morocco')|(DSUC5['Entity']=='Oman')|(DSUC5['Entity']=='Palestine')|(DSUC5['Entity']=='Somalia')|(DSUC5['Entity']=='Sudan')|(DSUC5['Entity']=='South Sudan')|(DSUC5['Entity']=='Syria')|(DSUC5['Entity']=='United Arab Emirates')|(DSUC5['Entity']=='Jordan') | (DSUC5['Entity']=='Qatar') | (DSUC5['Entity']=='Saudi Arabia') | (DSUC5['Entity']=='Tunisia')|(DSUC5['Entity']=='Yemen')]
nonarab = DSUC5[~((DSUC5['Entity']=='Algeria')|(DSUC5['Entity']=='Bahrain')|(DSUC5['Entity']=='Egypt')|(DSUC5['Entity']=='Iraq')|(DSUC5['Entity']=='Kuwait')|(DSUC5['Entity']=='Lebanon')|(DSUC5['Entity']=='Libya')|(DSUC5['Entity']=='Mauritania')|(DSUC5['Entity']=='Morocco')|(DSUC5['Entity']=='Oman')|(DSUC5['Entity']=='Palestine')|(DSUC5['Entity']=='Somalia')|(DSUC5['Entity']=='Sudan')|(DSUC5['Entity']=='South Sudan')|(DSUC5['Entity']=='Syria')|(DSUC5['Entity']=='United Arab Emirates')|(DSUC5['Entity']=='Jordan') | (DSUC5['Entity']=='Qatar') | (DSUC5['Entity']=='Saudi Arabia') | (DSUC5['Entity']=='Tunisia')|(DSUC5['Entity']=='Yemen'))]

st.write('\n')
st.write('\n')
col3,col4,col5 = st.columns(3)
with col3:
    st.metric(label="Number of Cancer Sites",value=22)
with col4:
    st.metric(label="Number Of Arab Countries",value=21)
with col5:
    st.metric(label="Time Period",value=f" 30 Years (1999-2019)")
style_metric_cards(border_left_color='#f04b4c')
spaces(3)

col1,col2 = st.columns(2)
with col1:
    year=st.slider("Select a year", 1990, 2019,key=1)
    xx,yy=calc(arabs,year)
    fig = px.bar( x=xx, y=yy, orientation='h',labels={'y':'Cancer Sites','x':'Death Rates'},height=500,
              title=f"Cancer Mortality Rate Per Cancer Site In The Arab World In {year} ",text_auto=True)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
    st.plotly_chart(fig)

with col2:
    years1=st.slider("Select a year", 1990, 2019,key=2)
    xx1,yy1=calc(nonarab,years1)
    xx2,yy2=calc(arabs,years1)
    fig = go.Figure(data=[
    go.Bar(name='Non Arab World', x=yy1, y=xx1),
    go.Bar(name='Arab World', x=yy2, y=xx2)
    ])
    fig.update_layout(barmode='group',xaxis={'categoryorder': 'total descending'},title_text=f"Cancer Mortality Rate Per Cancer Site In The Non Arab World VS The Arab World In {years1}",
                  yaxis=dict(title='Cancer Survival Percentage'),height=600)
    st.plotly_chart(fig)
    
spaces(2)
with st.expander('Explore'):
    country=arabs.Entity.unique()
    ans = st.selectbox( 'Select Country',(country))
    spaces(2)
    c1,c2=st.columns(2)

    with c1:
        st.write('\n')
        st.header(ans)
        st.write('\n')
        countries(ans)

    with c2:
        year2=st.slider("Select a year", 1990, 2019, key=4)
        sites(ans,year2)
    spaces(2)
    st.header('Cancer Sites')
    st.write('\n')
    site = st.selectbox( 'Select Cancer Site', ('Prostate', 'Breast', 'Uterine', 'Bladder',
       'Cervical', 'Kidney', 'Stomach', 'Nasopharynx', 'Testicular',
       'Other pharynx', 'Esophageal', 'Non-melanoma skin', 'Pancreatic',
       'Tracheal, bronchus, and lung', 'Lip and oral cavity',
       'Colon and rectum', 'Gallbladder and biliary tract', 'Liver', 'Larynx',
       'Ovarian', 'Thyroid', 'Brain and central nervous system'),key=5)
    
    c3,c4=st.columns(2)
    with c3:
        spaces(2)
        st.subheader(f'{site} Cancer')
        line(ans,site)
    with c4:
        spaces(5)
        # country=arabs[arabs['Entity']==ans]
        # fig=px.box(country,y=site,labels={site:f'{site} Cancer Mortality Rate'},width=600,height=500,
        #    title=f"{site} Cancer Mortality Rates In {ans}  From 1990 - 2019 ")
        # st.plotly_chart(fig)
        arabs['Year']=arabs['Year'].astype('int')
        num=[]     
        for i in range(1990,2020):
            num.append(i)
        #std=arabs[arabs['Entity']==ans][site].std()
        #std_r="{:.2f}".format(std)
        #st.metric('Standard Deviation',value=std_r)
        begin=st.selectbox('Select the year you are  interested in',(num)) 
        start=st.selectbox('Select the year you want to compare it with',(num)) 
        delt= arabs[(arabs['Year']==begin)& (arabs['Entity']==ans)][site].iloc[0] / arabs[(arabs['Year']==start) & (arabs['Entity']==ans)][site].iloc[0]
        change= arabs[(arabs['Year']==begin)& (arabs['Entity']==ans)][site].iloc[0] - arabs[(arabs['Year']==start) & (arabs['Entity']==ans)][site].iloc[0]
        delt_r="{:.2f}".format(delt)
        change_r="{:.2f}".format(change)
        st.metric('Rate Of Change',value=f'Rate: {delt_r}',delta=change_r)


spaces(3)
st.caption('Data source: https://ourworldindata.org/grapher/cancer-death-rates-by-type')

        
        

        
               

        




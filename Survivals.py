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
from gspread_pandas import Spread,Client
from google.oauth2 import service_account

st.set_page_config(page_title='iCanViz',page_icon='//Users//reema//Desktop//Grad Project //Streamlit//logo_rotated.png',layout='wide')

def spaces(num):
  for i in range(num):
    st.write('\n')

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
         
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "Database"
spread = Spread(spreadsheetname,client = client)

st.write(spread.url)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

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

selected= option_menu(menu_title=None,options=['Home','About','Deaths','Survivals','Login','Contact Us'],icons=['house','info-circle','graph-down','graph-up','person','envelope'],orientation='horizontal',menu_icon='cast',default_index=3)

def page(index):
    option_menu(menu_title=None,options=['Home','About','Deaths','Survivals','Login','Contact Us'],icons=['house','info-circle','graph-down','graph-up','person','envelope'],orientation='horizontal',menu_icon='cast',default_index=index)

st.markdown("-----")
if selected =='Home':
    switch_page('Main')
elif selected =='About':
    switch_page('Main')
elif selected =='Deaths':
    switch_page('Deaths')
elif selected =='Login':
    switch_page('Main')
    
elif selected =='Contact Us':
    switch_page('Main')

DSUC1=pd.read_csv('//Users//reema//Desktop//Grad Project //Streamlit//pages//DSUC1.csv')

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
  duration=["1995-1999","2000-2004","2005-2009"]
  country={'Algeria':[], 'Jordan':[], 'Qatar':[], 'Saudi Arabia':[], 'Tunisia':[]}
  for y in arab.Year.unique():
    for i in arab.Entity.unique():
      result=arab[(arab['Entity']==i) & (arab['Year']==y)]['Avg_survival_per']
      if  result.empty ==True:
          country[i].append(None)
      else:
          country[i].append(result.iloc[0])

  new=pd.DataFrame(country).T.reset_index()
  new.rename(columns={'index':'Entity',0:"1995-1999",1:"2000-2004",2:"2005-2009"},inplace=True)
  vals=new[new['Entity']==countr].values[0,1:]
  fig=px.bar(x=duration,y=vals,labels={'y':'Survival Percentage','x':'Duration'},text_auto=True,
           title=f"Cancer Survival Percentages In {countr} Across All Cancer Sites 1995 - 2009",width=550,height=500)
  st.plotly_chart(fig)

def sites(ans,year):
        filtered=arab[arab['Entity']==ans]
        xx,yy=calc(filtered,year)
        fig = px.bar( x=xx, y=yy, orientation='h',labels={'y':'Cancer Sites','x':'Death Rates'},
              title=f"Cancer Survival Percentage Per Cancer Site In {ans} From {year-4} - {year}",height=500,width=550,text_auto=True)
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig)



def bar(i):

  fig = px.bar(arab,y=i,x='Year',color='Entity',labels={i:f"{i} Cancer Survival Precentage","Entity":'Country'},
        title=f"Cancer Survival Percentage per Cancer Site Across Arab Countries for {i} Cancer <br><sup>iCanViz Research and Development Project 2023 - DA4DH and PSUT - Prof.Mohammad Odeh, Dr.Serin Atiani, Mahmoud Saber, Reema Maen</sup>", 
        text_auto=True)
  fig.update_xaxes(type='category')
  st.plotly_chart(fig)

arab= DSUC1[(DSUC1['Entity']=='Algeria')|(DSUC1['Entity']=='Jordan') | (DSUC1['Entity']=='Qatar') | (DSUC1['Entity']=='Saudi Arabia') | (DSUC1['Entity']=='Tunisia')]
notarab=DSUC1[~ ((DSUC1['Entity']=='Algeria')|(DSUC1['Entity']=='Jordan') | (DSUC1['Entity']=='Qatar' )| (DSUC1['Entity']=='Saudi Arabia') | (DSUC1['Entity']=='Tunisia'))]
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
st.write('\n')
st.write('\n')
st.write('\n')

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
    year=st.slider("Select a year", 1999, 2009, step=5,key=1)
    xx,yy=calc(arab,year)
    fig = px.bar(x=xx, y=yy, orientation='h',labels={'y':'Cancer Site','x':'Survival Percentage'},width=650,
              title=f"Cancer Survival Percentage Per Cancer Site In The Arab World In {year}",text_auto=True)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)

with col2:
    year2=st.slider("Select a year", 1999, 2009, step=5,key=2,)
    xx1,yy1 = calc(notarab,year2)
    xx2,yy2=calc(arab,year2)
    fig = go.Figure(data=[
    go.Bar(name='Non Arab World', x=yy1, y=xx1),
    go.Bar(name='Arab World', x=yy2, y=xx2)
    ])
    fig.update_layout(barmode='group',width=750,xaxis={'categoryorder': 'total descending'},title_text=f"Cancer Survival Percentage Per Cancer Site In The Non Arab World VS The Arab World In {year2}",
                  yaxis=dict(title='Cancer Survival Percentage'))
    st.plotly_chart(fig)

with st.expander('Explore'):
    ans = st.selectbox( 'Select Country', ('Algeria','Jordan',	'Qatar', 'Saudi Arabia'	,'Tunisia'))
    st.write('\n')
    st.write('\n')
    c1,c2=st.columns(2)

    with c1:
        st.write('\n')
        st.header(ans)
        st.write('\n')
        arab['Year']=arab['Year'].astype('object')
        countries(ans)
    with c2:
        year=st.slider("Select a year", 1999, 2009,step=5,key=3)
        sites(ans,year)
    
    st.write('\n')
    st.write('\n')
    st.header('Cancer Sites')
    st.write('\n')
    site = st.selectbox( 'Select Cancer Site',('Breast','Cervix','Colon','Leukaemia',	'Liver',	'Lung'	,'Ovary',	'Prostate',	'Rectum',	'Stomach'),key=4)

    c3,c4=st.columns(2)
    with c3:
        st.write('\n')
        st.write('\n')
        st.subheader(f'{site} Cancer In {ans}')


spaces(3)
st.caption('Data source: https://ourworldindata.org/grapher/five-year-survival-rates-by-cancer-type?time=latest')
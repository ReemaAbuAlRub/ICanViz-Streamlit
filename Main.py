import streamlit as st
import pandas as pd 
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import plotly.graph_objects as go
import sys
sys.path.insert(1,'//Users//reema//Desktop//Grad Project//Streamlit//app.py//streamlit_option_menu')
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.metric_cards import style_metric_cards
import pickle 
from pathlib import Path
import streamlit_authenticator as stauth
from gspread_pandas import Spread,Client
from google.oauth2 import service_account
from gsheetsdb import connect

import csv
import json



DSUC1=pd.read_csv('DSUC1.csv')
DSUC5=pd.read_csv('DSUC5.csv')

st.set_page_config(page_title='iCanViz',page_icon='logo_rotated.png',layout='wide')

def spaces(num):
  for i in range(num):
    st.write('\n')

a1,a2=st.columns(2)
with a1:
    image = Image.open('new.png')
    st.image(image,width=300) #Logo
with a2:
    s1,s2,s3=st.columns([0.1,0.1,0.1])
    with s1:
          image = Image.open('GA4DH.jpg')
          spaces(3)
          image_r = image.resize((50, 50))
          st.image(image_r)
          st.caption(' GA4DH')
    with s2: 
          spaces(3)        
          image = Image.open('psut.jpeg')
          image_r = image.resize((50, 50))
          st.image(image_r)
          st.caption('  PSUT')
    with s3:
          spaces(3)
          image = Image.open('ain.png')
          image_r = image.resize((50, 50))
          st.image(image_r) 
          st.caption('Al Ain University')


selected= option_menu(menu_title=None,options=['Home','About','Deaths','Survivals','Login','Contact Us'],icons=['house','info-circle','graph-down','graph-up','person','envelope'],orientation='horizontal',menu_icon='cast')

# def navigator(select='Home',index=0):
#   select= option_menu(menu_title=None,options=['Home','About','Deaths','Survivals','Login','Contact Us'],icons=['house','info-circle','graph-down','graph-up','person','envelope'],orientation='horizontal',menu_icon='cast',default_index=index)
#   return select


def local_css(file):
  with open(file) as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


def calc1(df):
  count=list(df.Entity.unique())
  res=[]
  for i in count:
    res.append(df[df['Entity']==i]['Avg_surv_per_country'].iloc[0])
  return res,count

def csv_to_json(csv_file_path, json_file_path):
    data_dict = {}
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        for rows in csv_reader:
            key = rows['Entity']
            data_dict[key] = rows
    with open(json_file_path, 'w', encoding = 'utf-8') as json_file_handler:
        json_file_handler.write(json.dumps(data_dict, indent = 4))


def map(df):  
    arab= df[(df['Entity']=='Algeria')|(df['Entity']=='Jordan') | (df['Entity']=='Qatar') | (df['Entity']=='Saudi Arabia') | (df['Entity']=='Tunisia')]
    rr,cc=calc1(arab)
    notarab=df[~ ((df['Entity']=='Algeria')|(df['Entity']=='Jordan') | (df['Entity']=='Qatar' )| (df['Entity']=='Saudi Arabia') | (df['Entity']=='Tunisia'))]
    rr1,cc1=calc1(notarab)
    newar=new=pd.DataFrame(list(zip(rr,cc)), columns=['Average_Survival_Percentage','Country'])
    newar['label']='Arab Country'
    newar['Code'] = list(arab.Code.unique())
    newnotar=pd.DataFrame(list(zip(rr1,cc1)), columns=['Average_Survival_Percentage','Country'])
    newnotar['label']='Non Arab Country'
    newnotar['Code'] = list(notarab.Code.unique())
    new=pd.concat([newar,newnotar],axis=0)
    fig = px.scatter_geo(new, locations="Code",color='label', hover_name="Country", size="Average_Survival_Percentage",projection="natural earth",height= 600, width=1300)
    st.plotly_chart(fig)

arab= DSUC1[(DSUC1['Entity']=='Algeria')|(DSUC1['Entity']=='Jordan') | (DSUC1['Entity']=='Qatar') | (DSUC1['Entity']=='Saudi Arabia') | (DSUC1['Entity']=='Tunisia')]
notarab=DSUC1[~ ((DSUC1['Entity']=='Algeria')|(DSUC1['Entity']=='Jordan') | (DSUC1['Entity']=='Qatar' )| (DSUC1['Entity']=='Saudi Arabia') | (DSUC1['Entity']=='Tunisia'))]

arabs= DSUC5[(DSUC5['Entity']=='Algeria')|(DSUC5['Entity']=='Bahrain')|(DSUC5['Entity']=='Egypt')|(DSUC5['Entity']=='Iraq')|(DSUC5['Entity']=='Kuwait')|(DSUC5['Entity']=='Lebanon')|(DSUC5['Entity']=='Libya')|(DSUC5['Entity']=='Mauritania')|(DSUC5['Entity']=='Morocco')|(DSUC5['Entity']=='Oman')|(DSUC5['Entity']=='Palestine')|(DSUC5['Entity']=='Somalia')|(DSUC5['Entity']=='Sudan')|(DSUC5['Entity']=='South Sudan')|(DSUC5['Entity']=='Syria')|(DSUC5['Entity']=='United Arab Emirates')|(DSUC5['Entity']=='Jordan') | (DSUC5['Entity']=='Qatar') | (DSUC5['Entity']=='Saudi Arabia') | (DSUC5['Entity']=='Tunisia')|(DSUC5['Entity']=='Yemen')]
#nonarab = countries[~((countries['Entity']=='Algeria')|(countries['Entity']=='Bahrain')|(countries['Entity']=='Egypt')|(countries['Entity']=='Iraq')|(countries['Entity']=='Kuwait')|(countries['Entity']=='Lebanon')|(countries['Entity']=='Libya')|(countries['Entity']=='Mauritania')|(countries['Entity']=='Morocco')|(countries['Entity']=='Oman')|(countries['Entity']=='Palestine')|(countries['Entity']=='Somalia')|(countries['Entity']=='Sudan')|(countries['Entity']=='South Sudan')|(countries['Entity']=='Syria')|(countries['Entity']=='United Arab Emirates')|(countries['Entity']=='Jordan') | (countries['Entity']=='Qatar') | (countries['Entity']=='Saudi Arabia') | (countries['Entity']=='Tunisia')|(countries['Entity']=='Yemen'))]


if selected == 'Home':
    spaces(2)
    container = st.container()
    col1,col2=st.columns(2)

    with container:
      with col1:
        st.markdown("<h2 style='text-align: left;'> What Is iCanViz? </h2>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: justify;">iCanViz is an intelligent cancer navigator of multiple cancer sites using a data strategy use-case driven approach in relation to cancer incidences, survivals and deaths (including associated risks) in the Arab world within certain reported years of cancer incidences per cancer site. </div>', unsafe_allow_html=True)
        spaces(1)
        st.markdown('<div style="text-align: justify; padding-right: 0px;"> A cancer Incidence Navigator needs a thorough study of the available and missing cancers data in the <b> Arab world </b>, and it requires study of the needs of the region in relation to cancers, their incidences, survival rates, deaths, and associated risks. This project is conducted to research and build a cancer incidence navigator for the Arab world, we call iCanViz. </div>', unsafe_allow_html=True)
        spaces(3)
      with col2:
        c1,c2,c3=st.columns([1,1,1])
        with c2:
          spaces(2)
          image = Image.open('logo_rotated.png')
          image_r = image.resize((300, 450))
          st.image(image_r)
    st.markdown('------')

    st.markdown("<h2 style='text-align: center;'> Data Overview </h2>", unsafe_allow_html=True)
    spaces(2)

    c1,c2,c3 =st.columns(3)

    c1.metric(label='Arab Countries',value=21)
    c2.metric(label='Cancer Sites',value=30)
    c3.metric(label='Duration',value=f"30 Years")
    style_metric_cards(border_left_color='#f04b4c')
    st.write('\n')
    st.write('\n')
    map(DSUC1)

    col1,col2 = st.columns(2)
    with col1:
       st.header('Survivals')
       fig = px.bar(arab,y='Avg_survival_per',x='Year',color='Entity',labels={'Avg_survival_per':'Average Survival Percentage',"Entity":'Country'},width= 600,
               title="Cancer Survival Percentage Across Arab Countries From 1999 Till 2009", 
               text_auto=True)
       fig.update_xaxes(type='category')
       st.plotly_chart(fig)
       col11, col22, col33 = st.columns([1,1,1])
       if col22.button('Survivals'):
          switch_page('Survivals')
       st.markdown(""" <style> .stButton > button{ background:#f04b4c; color: white } div.stButton > button:hover {background-color: #0F107F; color: white;} </style>""", unsafe_allow_html=True) 
   

    with col2:
      st.header('Deaths')
      x=arabs.Avg_death_per
      yr = round(x,2)
      fig = px.line(arabs,y=yr,x='Year',color='Entity',labels={'y':'Average Death Rate ','Avg_survival_per':'Average Survival Percentage',"Entity":'Country'},width= 600,
               title="Cancer Death Percentage Across Arab Countries From 1999 Till 2019"
               #,text_auto=True
               )
      #fig.update_xaxes(type='category')
      st.plotly_chart(fig)
      col4, col5, col6 = st.columns([1,1,1])
      if col5.button('Deaths'):
          switch_page('Deaths')
      st.markdown(""" <style> div.stButton > button:first-child {color= #f04b4c background-color:#f04b4c; } </style>""", unsafe_allow_html=True) 
     

elif selected == 'About':
    image = Image.open('About Us.png')
    image_r = image.resize((1500, 500))
    st.image(image_r)
    spaces(3)
    #st.markdown("<h2 style='text-align: center;'> What Is iCanViz? </h2>", unsafe_allow_html=True)
    #st.markdown('<div style="text-align: center;">iCanViz is an intelligent cancer navigator of multiple cancer sites using a data strategy use-case driven approach in relation </div>', unsafe_allow_html=True)
    #st.markdown('<div style="text-align: center;">to cancer incidences, survivals and deaths (including associated risks) in the Arab world within certain reported years of cancer </div>', unsafe_allow_html=True)
    #st.markdown('<div style="text-align: center;">incidences per cancer site.</div>', unsafe_allow_html=True)
    spaces(2)
    st.markdown("<h2 style='text-align: center;'> Aim and Objectives of the iCanViz Project </h2>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;  padding-right: 80px; padding-left: 80px;"> This research aims to develop an intelligent cancer navigator (iCanViz) of multiple cancer sites using a data strategy use-case driven approach in relation to cancer incidences, survivals and deaths (including associated risks) in the Arab world within certain reported years of cancer incidences per cancer site. </div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;  padding-right: 80px; padding-left: 80px;"> <b>Objective One:</b> Identify and specify sufficient and representative data strategy use-cases related to the intelligent cancer navigator associated with multiple cancers in the Arab world.  </div>', unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;  padding-right: 80px; padding-left: 80px;'> <b>Objective Two:</b>  Conduct a systematic mapping study for literature related to the identified data strategy use cases in the first objective to inform specifying the iCanViz data strategy use cases.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;  padding-right: 80px; padding-left: 80px;'> <b>Objective Three:</b>  Design and implement the iCanViz data strategy use cases identified in objective one using the appropriate data mining and machine learning techniques including the creation of iCanViz data repository. </div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: jusitfy;  padding-right: 80px; padding-left: 80px;'> <b>Objective Four: </b> Critically evaluate the effectiveness of the iCanViz research outcomes through validating the implemented data strategy use-cases with the respective domain specialist(s). </div>", unsafe_allow_html=True)
    spaces(2)
    st.markdown("<h2 style='text-align: center;'> Research Design Philosophy  </h2>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify; padding-right: 80px; padding-left: 80px">The iCanViz research project adopts the <b> Design Science Research Methodology (DSRM).</b> DSRM is a research paradigm that creates novel artifacts and innovative solutions to real-world problems attempting to enhance human knowledge with incremental and iterative attention to research project segments. Given the iCanViz project is an information systems artifact, the DSRM methodological approach appears fit-for-purpose compared to other research methods and frameworks. The rationale behind adopting the DSRM approach in the iCanViz research project is attributed to the following. First, the nature of the DSRM is geared toward research projects that involve information system development, which requires incremental stages in developing and validating the research outcomes. Second, the iCanViz is a data analytics project with several incremental stages associated with key and core data strategy use-cases that need to be contextualized as increments of the iCanViz research project. Third, DSRM incorporates flexibility in the inclusion of research methods and does not limit the research design to one research method, as several research methods will be utilized in the iCanViz research project. </div>', unsafe_allow_html=True)
    
    spaces(2)
    st.markdown("<h2 style='text-align: center;'> Who We Are? </h2>", unsafe_allow_html=True)
    spaces(2)
    with st.expander('+',expanded=True):
      c111,c222=st.columns(2)
      with c111:
        c1,c2,c3=st.columns([1,1,1])
        spaces(2)
        with c2:
          spaces(2)
          image = Image.open('GA4DH.jpg')
          image_r = image.resize((400, 400))
          st.image(image_r) 
          spaces(7)         
          image = Image.open('psut.jpeg')
          image_r = image.resize((400, 400))
          st.image(image_r)
          spaces(9)
          image = Image.open('ain.png')
          image_r = image.resize((400, 400))
          st.image(image_r) 
 

      with c222:
        st.markdown("<h3 style='text-align: center;'> Global Academy For Digital Health (GA4DH)</h3>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: justify; padding-right: 30px'> Global Academy for Digital Health (GA4DH) is an international organisation with the mission to bridge the gap in healthcare divide amongst countries, regions, and nations through digital technology. GA4DH’s mission is orchestrated through the global delivery of digitally empowered specialist healthcare education and training, innovative research and development projects, continuous professional development programs, and fit-for-purpose healthcare support.  GA4DH is associated with domain specialists in various areas of digital healthcare globally.</div>", unsafe_allow_html=True)
        spaces(2)
        st.markdown("<h3 style='text-align: center;'> Princess Sumayya University For Technology (PSUT) </h3>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: justify; padding-right: 30px">From its establishment, the University laid out for itself a path of leadership and excellence and quickly set out on that path. Since that time, it has attained lofty achievements which have taken it to prominence among the body of Jordanian universities. The following are among the most outstanding of those achievements: 1-The receipt of the Order of Independence, First Class, in recognition of the great strides that have been made since the founding of the University in 1991, achievements that have been hailed as exceptional both within Jordan and in the region, in addition to its outstanding contribution to the advancement of the ICT and Business fields in Jordan. The University has also distinguished itself in the academic and research fields, and has worked hard to instill its students with the spirit of creativity and innovation, in addition to supporting the local, regional and global market with graduates equipped with a high level of scientific and technical competencies.</div>', unsafe_allow_html=True)
        spaces(2)
        st.markdown("<h3 style='text-align: center; padding-right: 30px'> Al Ain University Of Science And Technology</h3>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: justify; padding-right: 30px ">Established in 2004, Al Ain University (AAU) opened the doors to its first student cohort in 2005. Constantly innovating, AAU expanded its facilities by opening a second campus in Abu Dhabi in 2008, offering programs in Business and Law. Having begun with three colleges (Engineering, Business, Education, Humanities, and Social Sciences), the University has continued to expand its program offerings which now include 22 undergraduate programs across six colleges (Engineering, Pharmacy, Law, Education, Humanities, and Social Sciences, Business and Communication and Media), 8 Master’s programs, and 1 Professional Diploma in Teaching program.AAU is licensed to operate under the auspices of the UAE Ministry of Education (MoE). </div>', unsafe_allow_html=True)
        spaces(2)
    
        
elif selected == 'Contact Us':
  st.write('\n')
  st.write('\n')
  st.write('\n')
  st.header('Contact Us')
  contact_form = """ 
   <form action="https://formsubmit.co/ree20190150@std.psut.edu.jo" method="POST">
     <input type="text" name="name" placeholder= "Name" required>
     <input type="email" name="email" placeholder= "Email" required>
     <textarea name="Message" placeholder= "Write Here" ></textarea>
     <button type="submit">Send</button>
   </form>
  """
  st.markdown(contact_form, unsafe_allow_html=True)
  local_css("style.css")
  st.write('\n')
  st.write('\n')
  st.write('\n')

  st.caption('Khalil Al Saket Street\n')
  st.caption('Jubeiha\n')
  st.caption('Amman,Jordan \n \n')
  st.caption('Email: Ree20190150@std.psut.edu.jo  or  Mah20190306@std.psut.edu.jo')

# elif selected == 'Analysis':
#   spaces(2)
#   st.markdown("<h2 style='text-align: center;'> Select the page you want to navigate through</h2>", unsafe_allow_html=True)
#   spaces(2)
#   button_style = """
#         <style>
#         .stButton > button {
#             color: white;
#             background: #F04B4C;
#             width: 350px;
#             height: 50px;
           
#         }
#         div.stButton > button:hover {
#               background-color: #0F107F;
#               color: white;
#     }
#         </style>
#         """
#   c7, c8, c9 = st.columns([1,1,1])
#   if c8.button('Deaths'):
#       switch_page('Deaths')
#   st.markdown(button_style, unsafe_allow_html=True)

#   if c8.button('Survivals'):
#       switch_page('Survivals')
#   st.markdown(button_style, unsafe_allow_html=True)
 
#   if c8.button('Years Lost To Disability'):
#       #switch_page('Survivals')
#        st.write('Pending')
#   st.markdown(button_style, unsafe_allow_html=True)
 
#   if c8.button('Risks'):
#       #switch_page('Survivals')
#       st.write('Pending')
#   st.markdown(button_style, unsafe_allow_html=True)

#   if c8.button('Countries'):
#       #switch_page('Survivals')
#       st.write('Pending')
#   st.markdown(button_style, unsafe_allow_html=True)

#   if c8.button('Cancer Sites'):
#       #switch_page('Survivals')
#       st.write('Pending')
#   st.markdown(button_style, unsafe_allow_html=True)

elif selected == 'Deaths':
  switch_page('Deaths')

elif selected =='Survivals':
    switch_page('Survivals')

elif selected == 'Login':
  spaces(3)
  st.write('This page is designated for database curators and authorized personnel only')
  names=['Reema Maen',"Mahmoud Saber"]
  users=['reemam','mahmouds']
  file_path= Path('//Users//reema//Desktop//Grad Project //Streamlit//generate_key.py').parent / "hashed_pw.pkl"
  with file_path.open('rb') as file:
    hashed_pass= pickle.load(file)
  authen=stauth.Authenticate(names,users,hashed_pass,"Repository",'abcdef',cookie_expiry_days=30)
  name,authentication_status,username= authen.login('Login','main')

  if authentication_status==False:
    st.error("Your Username / Password is incorrect")

  elif authentication_status:
    c1,c2= st.columns(2)
    with c1:
      st.header(f'{name}') 
      st.caption('Database curator')
      spaces(3)
    with c2:
      c1,c2,c3,c4,c5,c6,c7=st.columns([1,1,1,1,1,1,1])
      with c7:
        spaces(3)
        authen.logout("Logout", "main")
        st.markdown(""" <style> .stButton > button{ background:#f04b4c; color: white } div.stButton > button:hover {background-color: #0F107F; color: white;} </style>""", unsafe_allow_html=True) 
   
    csv_file_path = '//Users//reema//Desktop//Grad Project //Streamlit//pages//DSUC1.csv'
    json_file_path = '//Users//reema//Desktop//Grad Project //Streamlit//pages//DSUC1.json'
    csv_to_json(csv_file_path, json_file_path)

    with st.expander('Playground'):
      with st.form(key='Code'):
        code_input=st.text_area('Insert Python Code here')
        submit=st.form_submit_button('Execute')
        if submit:
          exec(code_input)
    with st.expander('Data Retrieval'):
      col1111,col2222=st.columns(2)
      with col1111:
        data_as_csv= DSUC1.to_csv(index=False).encode("utf-8")
        st.download_button(
        "Download survival data as CSV", 
        data_as_csv, 
        "benchmark-tools.csv",
        "text/csv",
        key="download-tools-csv",
        )
      with col2222:
        data_as_csv= DSUC5.to_csv(index=False).encode("utf-8")
        st.download_button(
        "Download Deaths data as CSV", 
        data_as_csv, 
        "benchmark-tools.csv",
        "text/csv",
        key="download-tools-csv2",
        )
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 5px; }
    </style>
    """

    style_div = styles(
        #position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=0.3
    )

    style_hr = styles(
        #display="block",
        margin=px(0, 0, "auto", "auto"),
        border_style="inset",
        border_width=px(0.1)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

# def image(directory):
  # image=Image.open(directory)
  # x=image.resize((25,25))

  #return st.image(x)

def footer():
    myargs = [
      
        "   GA4DH  ",
        image('//Users//reema//Desktop//Grad Project //Streamlit//Logos//GA4DH.jpg',
              ),
        "  PSUT  ",
        image('//Users//reema//Desktop//Grad Project //Streamlit//Logos//psut.jpeg',
             ),
        "  Al Ain University  ",
      
        image('//Users//reema//Desktop//Grad Project //Streamlit//Logos//psut.jpeg',
              ),
  
    ]
    layout(*myargs)

footer()


    
# footer="""<style>
# a:link , a:visited{
# footer {visibility: hidden;}
# color: blue;
# .stApp { bottom: 5px; }
# background-color: transparent;
# text-decoration: underline;
# }

# a:hover,  a:active {
# color: red;
# background-color: transparent;
# text-decoration: underline;
# }

# .footer {
# position: fixed;
# left: 0;
# bottom: 0;
# width: 100%;
# background-color: white;
# color: black;
# text-align: center;
# }
# </style>
# <div class="footer">
# <p>
#   Developed by 
# </p>
# <p>
#   <a  text-align: center;' href="https://www.psut.edu.jo/" target="_blank">   GA4DH  </a>,
#   <a  text-align: center;' href="https://www.psut.edu.jo/" target="_blank">   PSUT  </a>,
#   <a  text-align: center;' href="https://www.aau.ac.ae/en/" target="_blank">   Al Ain University </a>
# </p>


# </div>
# """
# st.markdown(footer,unsafe_allow_html=True)

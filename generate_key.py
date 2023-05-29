import pickle 
from pathlib import Path
import streamlit_authenticator as stauth

names=['Reema Maen',"Mahmoud Saber"]
users=['reemam','mahmouds']
password=['XXXX','XXXX']

hashed= stauth.Hasher(password).generate()
file_path= Path('//Users//reema//Desktop//Grad Project //Streamlit//generate_key.py').parent / "hashed_pw.pkl"
with file_path.open('wb') as file:
    pickle.dump(hashed,file)

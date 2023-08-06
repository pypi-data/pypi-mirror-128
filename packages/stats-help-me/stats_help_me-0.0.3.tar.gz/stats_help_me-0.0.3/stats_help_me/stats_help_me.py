import pandas as pd
import os
import sys
from PIL import Image
from IPython.display import display
from urllib.request import urlopen
  

def james():
    print('James Bond 007')
    

def show_img():
    url = "https://i.ibb.co/xF92y4V/img.png"       
    img = Image.open(urlopen(url))
    display(img)
    
    

def show_df():
    url = 'https://docs.google.com/spreadsheets/d/1lxl991aQq9etA5rvG3thCtjbeW-WgXlx/edit?usp=sharing&ouid=112173764928870974633&rtpof=true&sd=true'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_excel(path)
    return df
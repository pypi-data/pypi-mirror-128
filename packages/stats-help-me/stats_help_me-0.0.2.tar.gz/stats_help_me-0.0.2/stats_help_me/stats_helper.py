import pandas as pd
import os
import sys
from PIL import Image
from IPython.display import display
from urllib.request import urlopen
  

def james():
    print('James Bond 007')
    

def show_img():
    url = "https://previews-te.wetransfer.net/file/wetransfer/p1ot/f3ea4e20aa04c1cb0749c09ffe1b182420211121122736/hl-6226582323?height=512&source=storm&url=https%3A%2F%2Fstorm-eu-west-1.wetransfer.net%2Ffiles%2FeyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHNLd2doLytCeUFRQT0iLCJleHAiOm51bGwsInB1ciI6ImludGVybmFsX2ZpbGVfZG93bmxvYWQifX0--ce63eb143435a4b42ca5372c71045bc4b979ab6490d855b41c0d1e71ac8390e6%3Ftoken%3DeyJhbGciOiJIUzI1NiJ9.eyJzdG9ybS5zZmUiOiJleUpmY21GcGJITWlPbnNpYldWemMyRm5aU0k2SWtKQmFITkxkMmRvTHl0Q2VVRlJRVDBpTENKbGVIQWlPbTUxYkd3c0luQjFjaUk2SW1sdWRHVnlibUZzWDJacGJHVmZaRzkzYm14dllXUWlmWDAtLWNlNjNlYjE0MzQzNWE0YjQyY2E1MzcyYzcxMDQ1YmM0Yjk3OWFiNjQ5MGQ4NTViNDFjMGQxZTcxYWM4MzkwZTYiLCJleHAiOjE2Mzc0OTk1OTEsImlhdCI6MTYzNzQ5Nzc5MSwia2lkIjoiV1V0eCJ9.uFlBLHyEOZfhr5fB-vPIZeLK8OXhbejqhLn7u6hFd8s&width=512&s=200e5d98f883d31cec508337c09a14feb0891815&Expires=1637501391&Signature=i4bglSa3dkXGHaA2yJC4DouXjrM4MK--3tycxS8CKqYCQdKNQRaVLUXb4L86ip~24ogGIo1o6wABel~sYKyx1DJqp6R0c5ymTZJ-ErLmXSVW6kQAHzaPyXP6ElNXWqN9tQzJxs5fsSe1asBa312gtXO9JQ-5QoC9cT2Z1e9lojD6uwFSE6bJddG0zmKDFIvtEuTDO7G3mvMnxrD5vSGxh2o1PTaigj04CBHxcO~~7d6n5pjJPjixyEm2GvqptYJKcAh6mqmhchTcps6JDxUPXHPyUuj-O9M0HEmYDY89BJLi-0SC~aDVHENhxjdLjHfbElo6bKU2JdGt-afxqB5xBA__&Key-Pair-Id=APKAIRLQFERKGUWFG7GQ"       
    img = Image.open(urlopen(url))
    display(img)
    
    

def show_df():
    url = 'https://docs.google.com/spreadsheets/d/1lxl991aQq9etA5rvG3thCtjbeW-WgXlx/edit?usp=sharing&ouid=112173764928870974633&rtpof=true&sd=true'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_excel(path)
    return df
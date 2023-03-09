# -*- coding: utf-8 -*-
"""Text Extraction from Image.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11rXXLjdYG74tnQuC0-_PZLQI9Un3Kgzs
"""

#pip install easyocr
#pip install sqlalchemy
#pip install pymysql
#pip install streamlit

import easyocr as ocr
import pandas as pd
import numpy as np
import re
import streamlit as st

# importing sql library
import pymysql
from sqlalchemy import create_engine, text
# Include PIL
from PIL import Image
import cv2


st.title("Text Extractor From Image") 
tab1,tab2,tab3=st.tabs(['Home','Database Upload','Uploaded'])
with tab1:
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
    reader=ocr.Reader(['en'])

    # If user attempts to upload a file.
    if image_file is not None:
        bytes_data = image_file.getvalue()
        # Show the image filename and image.
        #st.write(f'filename: {image_file.name}')
        col1,col2=st.columns(2)
        with col1:
                st.image(bytes_data)
        with col2:
                results=reader.readtext(bytes_data, detail=0,paragraph=True)
                #results=reader.readtext(np.array(input_image), detail=0,paragraph=True)
                df=pd.DataFrame(results,columns=['Text'])
                st.dataframe(df)
    else:
        st.info('Please upload the Image')
    
with tab2:    
    # To connect MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password = "1234",
        database='Text1'
        )
    cur = conn.cursor()
    #creating new database
    #cur.execute('CREATE DATABASE Text1') #For starting up only 
    #importing sql library
    from sqlalchemy import create_engine
    table_name=st.text_input("Enter Image Name for saving in database Table","For Example: ram  (name of the person)")
    # create a reference for sql library
    engine = create_engine('mysql+pymysql://root:1234@localhost:3306/Text1',echo = False)
    # Attach the data frame to the sql with a name of the table
    if st.button("Upload"):
        if len(table_name)!=0:
            try:
                df.to_sql (table_name,con = engine,if_exists='fail')
                st.success(f'{table_name} Text Extraction is uploaded!', icon="✅")
            except:
                st.warning('Image Name already Exists', icon="⚠️")
        
        else:
            st.warning('Give Image Name to upload', icon="⚠️")

with tab3:
    cur.execute("Show tables;")
    myresult = cur.fetchall()
    table_names=[]
    for x in myresult:
        table_names.append(x[0])
    option = st.selectbox('Select Uploaded Photos',np.array(table_names))
    if option:
        st.write('You selected:', option)
        query = f'SELECT * FROM {option}' 
         # As Normal assign gives OPTIONAL ENGINE (Attribute Error)    
        df_upload= pd.read_sql_query(sql=text(query), con=engine.connect())
        st.dataframe(df_upload)
    
    
    
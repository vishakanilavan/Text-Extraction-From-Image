# -*- coding: utf-8 -*-

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
                                                    #Function To Extract Text & Forming DataFrame
#-------------------------------------------------------------------------------------------------------------------------------------#

def text_extract(result_para,result_text):          
    PH=''
    ADD=''
    EMAIL=''
    PIN=''
    WEB=''
    CARD_HOLDER=''
    ID=[]
    web_count=0
    ad_count=0
    for i, string in enumerate(result_para):   
        # TO FIND EMAIL
        match1=re.findall(r'\S+@\S+', string)
        if len(match1)>1:
            EMAIL=EMAIL+' '.join(match1)+' '
            ID.append(i)
        elif len(match1)==1:
            EMAIL=EMAIL+' '.join(match1)

        # TO FIND PINCODE
        match2 = re.findall(r'[\d*]{6,7}', string)
        if match2:
            PIN=PIN+' '.join(match2)
            ID.append(i)

        # TO FIND PHONE NUMBER    
        match3 = re.findall(r'(?:\+*\d+\-?\S*){8,}', string)
        if len(match3)>1:
            PH=PH+' '.join(match3)
            ID.append(i)
        elif len(match3) == 1:
            PH=' '+PH+' '.join(match3)

        # WEBSITE URL          
        match4=re.findall(r"(www*\S*|WWW*\S*|\S*.com\S*)", string)
        match5=re.sub(r' *\S*@\S* *',''," ".join(match4))
        if len(match5)!=0: 
            if web_count==0:# Because match5 is string
                WEB=match5
                ID.append(i)
                web_count=web_count+1
            else:
                WEB=WEB+' '+match5

        # TO FIND ADDRESS 
        keywords = ['road', 'floor', ' st ', 'st ,', 'street', ' dt ', 'district',
                  'near', 'beside', 'opposite', ' at ', ' in ', 'center', 'main road',
                  'state','country', 'post','zip','city','zone','mandal','town','rural',
                  'circle','next to','across from','area','building','towers','village',
                  ' ST ',' VA ',' VA,',' EAST ',' WEST ',' NORTH ',' SOUTH ']
        # Define the regular expression pattern to match six or seven continuous digits
        digit_pattern = r'\d{6,7}'
        # Check if the string contains any of the keywords or a sequence of six or seven digits(i.e pincode)
        if any(keyword in string.lower() for keyword in keywords) or re.search(digit_pattern, string):
            string=re.sub(r' *www\S* *| *WWW\S* *| *\S*.com *| *(?:[+-]?\d+\-?\S*){7,} *','',string)
            if ad_count!= 0:
                ADD=ADD+string+' '
                ID.append(i)
            else:
                ADD=ADD+string
                ad_count=1
    CARD_HOLDER=''
    for string in result_para:
        if string not in(EMAIL+' '+WEB+' '+ADD+' '+PH+' '+PIN):
            string=string.replace(EMAIL,'')
            string=string.replace(PH,'')
            string=string.replace(ADD,'')
            string=string.replace(WEB,'')
            string=string.replace(PIN,'')
            CARD_HOLDER=CARD_HOLDER+string+' '
    NAME=result_text[0]
    WORK=result_text[1]
    PH_lt=[]
    PH_lt.append(PH)
    EMAIL_lt=[]
    EMAIL_lt.append(EMAIL)
    ADD_lt=[]
    ADD_lt.append(ADD)
    WEB_lt=[]
    WEB_lt.append(WEB)
    PIN_lt=[]
    PIN_lt.append(PIN)
    CARD_HOLDER_lt=[]
    CARD_HOLDER_lt.append(CARD_HOLDER)
    NAME_lt=[]
    NAME_lt.append(NAME)
    WORK_lt=[]
    WORK_lt.append(WORK)
    #creating empty dataframe
    df=pd.DataFrame()
    # Assigning columns of dataframe
    df['NAME']=NAME_lt
    df['WORK']=WORK_lt
    df['Address']=ADD_lt
    df['Phone_No']=PH_lt
    df['Pincode']=PIN_lt
    df['E-Mail']=EMAIL_lt
    df['Web']=WEB_lt
    df['BIZ_DETAILS']=CARD_HOLDER_lt
    
    return df
                                                #Text_extract.py
#   -----------------------------------------------------------------------------------------------------------------------------------     
    
st.title(":orange[Text Extractor From Image:ticket:]") 
tab1,tab2,tab3=st.tabs(['Home','Database Upload','Uploaded'])
with tab1:
    image_file = st.file_uploader(":orange[Upload Images👇]", type=["png","jpg","jpeg"])
    reader=ocr.Reader(['en'])

    # If user attempts to upload a file.
    if image_file is not None:
        bytes_data = image_file.getvalue() # To convert stringio file format to bytes format
        # Show the image filename and image.
        #st.write(f'filename: {image_file.name}')
        with st.sidebar:
            st.title(':orange[Image Tab]🎭')
            st.image(bytes_data)      
        results_para=reader.readtext(bytes_data, detail=0,paragraph=True)
        results_text= reader.readtext(bytes_data,detail=0,paragraph=False)
        #results=reader.readtext(np.array(input_image), detail=0,paragraph=True)
        df=text_extract(results_para,results_text)
        # Display the dataframe and allow the user to stretch the dataframe
        if st.button('EXTRACT TEXT'):
            st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    else:
        st.info('📍Please :green[upload the Image]')
    
with tab2:    
    # To connect MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password = "1234",
        database='Text2'
        )
    cur = conn.cursor()
    #creating new database
    #cur.execute('CREATE DATABASE Text2') #For starting up only 
    #importing sql library
    from sqlalchemy import create_engine
    table_name=st.text_input(":orange[Enter Image Name for saving in database Table]👇","For Example: ram  (name of the person)")
    # create a reference for sql library
    engine = create_engine('mysql+pymysql://root:1234@localhost:3306/Text2',echo = False)
    # Attach the data frame to the sql with a name of the table
    if st.button("Upload"):
        if len(table_name)!=0:
            try:
                df.to_sql (table_name,con = engine,if_exists='fail')
                st.success(f':green[{table_name} File is uploaded!]', icon="✅")
            except:
                st.warning('Image Name :red[Already Exists]', icon="⚠️")
        
        else:
            st.warning(':red[Give Image Name] to upload', icon="⚠️")

with tab3:
    cur.execute("Show tables;")
    myresult = cur.fetchall()
    table_names=[]
    for x in myresult:
        table_names.append(x[0])
    option = st.selectbox(':orange[Select Uploaded Photo File]',np.array(table_names))
    if option:
        st.write(f'You selected: :green[{option}]📂')
        query = f'SELECT * FROM {option}' 
         # As Normal assign gives OPTIONAL ENGINE (Attribute Error)    
        df_upload= pd.read_sql_query(sql=text(query), con=engine.connect())
        df_upload.drop(['index'],axis=1,inplace=True)
        st.markdown(df_upload.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    
#---------------------------------------------------------------------------------------------------------------------------------------#   
    

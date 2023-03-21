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
import io
import cv2
from PIL import Image

# importing sql library
import mysql.connector
import pymysql
from sqlalchemy import create_engine, text
import sqlite3 
import base64
# Include PIL
from PIL import Image
import cv2
                                                    #Function To Extract Text & Forming DataFrame
#-------------------------------------------------------------------------------------------------------------------------------------#
@st.cache_data
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
            string=re.sub(r' *www\S* *| *WWW\S* *| *\S*.com *| *(?:[+-]?\d+\-?\S*){6,} *','',string)
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
    df['Name']=NAME_lt
    df['Work']=WORK_lt
    df['Address']=ADD_lt
    df['Phone_No']=PH_lt
    df['Pincode']=PIN_lt
    df['E-Mail']=EMAIL_lt
    df['Website']=WEB_lt
    df['Details']=CARD_HOLDER_lt
    
    return df
                                                #Text_extract.py
#   -----------------------------------------------------------------------------------------------------------------------------------     
    
st.title(":orange[Text Extractor From Image:ticket:]") 
tab1,tab2,tab3,tab4=st.tabs(['Home','Upload','Update','Delete'])
with tab1:
    image_file = st.file_uploader(":orange[Upload Images👇]", type=["png","jpg","jpeg"])
    reader=ocr.Reader(['en'])

    # If user attempts to upload a file.
    if image_file is not None:
        # To read file as bytes:
        bytes_data = image_file.getvalue() # To read file as bytes
        bytes_array=np.array(bytes_data) # Converting bytes to bytes array
        #Encode the byte array as Base64 
        image_base64 = base64.b64encode(bytes_data)
        st.header(':orange[Image]🎭')
        st.image(image_file) # image object accepts only bytes or numpy array datatype 
        # Read the text from the image using OCR
        image = Image.open(io.BytesIO(image_file.read()))
        

        # Convert PIL Image object to numpy array
        img_array = np.array(image)

        # Pass numpy array to EasyOCR's readtext() method
        results_para=reader.readtext(img_array, detail=0,paragraph=True) #Image should be in byte/Numpy array/str format
        results_text= reader.readtext(img_array,detail=0,paragraph=False)
        df=text_extract(results_para,results_text)
        # Display the dataframe and allow the user to stretch the dataframe
        if st.button('EXTRACT TEXT'):
            st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    else:
        st.info('📍Please :green[upload the Image]')  
        
                                                # Upload to DB
# ---------------------------------------------------------------------------------------------------------------------------------------

# To connect MySQL database
con =mysql.connector.connect(
host='localhost',
user='root',
password = "1234",
auth_plugin='mysql_native_password'
)
mycursor = con.cursor()
#creating new database
mycursor.execute('CREATE DATABASE IF NOT EXISTS ocr') #For starting up only
con.commit()
                  #--------------------------------------------------------------------------#
# create a reference for sqlalchemy object
engine = create_engine('mysql+pymysql://root:1234@localhost:3306/ocr',echo = False)                         
conn =pymysql.connect(
host='localhost',
user='root',
password = "1234",
database='ocr',
#auth_plugin='mysql_native_password'
)
mycursor=conn.cursor()
#mycursor.execute("DROP TABLE IF EXISTS business_cards")
mycursor.execute("CREATE TABLE IF NOT EXISTS Business_cards (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), work                                       VARCHAR(255), address VARCHAR(255), phone VARCHAR(255), pincode VARCHAR(255), email VARCHAR(255),website                                   VARCHAR(255), details VARCHAR(255),image LONGBLOB)"
                  )

with tab2:        
    st.subheader("Upload Into Database ")
    query = 'SELECT * FROM business_cards' 
    # As Normal assign gives OPTIONAL ENGINE (Attribute Error)    
    new_df= pd.read_sql_query(sql=text(query), con=engine.connect())
    st.dataframe(new_df)
    
    if st.button("Upload"):
        sql = "INSERT INTO business_cards(name, work, address, phone, pincode, email, website, details, image) VALUES(%s, %s, %s,                                                     %s,%s,%s, %s, %s, %s)"
        val = (df['Name'][0],df['Work'][0],df['Address'][0], df['Phone_No'][0],df['Pincode'][0],df['E-Mail'][0], df['Website'][0],                        df['Details'][0],image_base64)
        mycursor.execute(sql, val)
        conn.commit()
        st.sidebar.success("Data uploaded successfully!")
        query = 'SELECT * FROM business_cards'     
        df_1= pd.read_sql_query(sql=text(query), con=engine.connect())
        st.table(df_1)
        
                                                         # Update DB
 #-----------------------------------------------------------------------------------------------------------------------------------------
with tab3:
    new_df=pd.read_sql(text("SELECT * FROM business_cards"),engine.connect())
    st.table(new_df)
    st.subheader("Update Records:")
    option=st.selectbox('Select Option to Update',new_df.columns[0:-1])
    if option:
        with st.form("Update-form"):
            id1=st.text_input('Enter the id to update')
            new=st.text_input(f'Enter The New {option}')
            if st.form_submit_button('UPDATE'):
                try:
                    sql = f'UPDATE business_cards SET {option}=%s WHERE id = %s'
                    val = (new, id1)
                    mycursor.execute(sql, val)
                    conn.commit()
                    st.success("Record updated successfully")
                except:
                    st.warning("Enter correct Details to Update")
                df = pd.read_sql(text("SELECT * FROM business_cards"),engine.connect())
                st.dataframe(df)
            
                                                     # Delete Records
#------------------------------------------------------------------------------------------------------------------------------------------
with tab4:
    new_df=pd.read_sql(text("SELECT * FROM business_cards"),engine.connect())
    st.table(new_df)
    st.subheader("Delete Data")
    with st.form("delete-form"):
        id = st.text_input("Enter the record id you want to delete")
        submitted = st.form_submit_button("Delete")
        if submitted:
            try:
                sql = "DELETE FROM business_cards WHERE id = %s"
                val = (id,)
                mycursor.execute(sql, val)
                conn.commit()
                st.warning("Record deleted successfully")
            except:
                st.warning("Enter correct Details")
            df = pd.read_sql(text("SELECT * FROM business_cards"),engine.connect())
            st.dataframe(df)


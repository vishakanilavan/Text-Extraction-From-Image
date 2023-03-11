
# TEXT EXTRACTION FROM BIZCARD (USING easyocr)


Image Analysing and visualising is becoming more demand.This project helps in extracting Text from Biz card using easyocr.



## HOW TO RUN CODE:
```bash
1) Clone/download the repository
```
```bash
2) Install the requirements present in the requirements.txt using pip install -r requirements.txt
```
```bash
3) Run the app using streamlit run Text_Extraction_From_Image.py
```
## WORKFLOW OF THE PROJECT:
```bash
 1)EXTRACTING TEXT FROM BIZ CARD:
```
 Extract the text from Biz card using easyocr library. Then Text preprocessing is done to identify Name,Work,Address,Pincode,Phone No,Email ,Website and Card holders details like Company name
```bash
 2)UPLOADING EXTRACTED TEXT TO MYSQL DATABASE:
 ```
 After getting extracted data,upload the data in sql database using pymsql and sqlalchemy.

 ```bash
  3)RETRIEVING EXTRACTED TEXT DATA FROM SQL:
 ```
 Next, Retrieve the data from sql database using pymsql for connecting python with sql and sqlalchemy for easy handling of dataframes in mysql and display in Uploaded tab of app.


## Screenshots:

[![Text-extractor.png](https://i.postimg.cc/d1FVCC3T/Text-extractor.png)](https://postimg.cc/TykxMprR)

[![Text-extractor-2.png](https://i.postimg.cc/bYQ0MZ5C/Text-extractor-2.png)](https://postimg.cc/Th3W53fg)

[![Text-extractor-3.png](https://i.postimg.cc/y85SWK53/Text-extractor-3.png)](https://postimg.cc/dh20SbJJ)
## Demo:
Here's My demo video  of the project
in linkedin's profile

https://www.linkedin.com/posts/vishaka-nilavan-9345aa138_data-datascientist-datasciencejobs-activity-7040315010467721216-0bf5/?utm_source=share&utm_medium=member_desktop


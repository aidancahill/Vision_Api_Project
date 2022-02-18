# VisionApiProject
Vision API Project
Software Project Specification
Aidan Cahill
2/18/2022

Introduction

The Mobile Brow Lounge(MBL) is a mobile micro blading studio owned and operated by Rachelle Fallon. 
The service provided by the MBL is permanent makeup and customers are mainly women but sometimes men. 
The primary record keeping channel for her business was mainly paper documents that were medical history 
release documents, and an agreement of the understanding of the type of procedure being performed. 
A need for a customer database became more prevalent the more customer procedures were being performed.

Purpose

The purpose of the software is to populate a database of customers for the MBL that contains the customer's Name, 
Date of procedure, Email, phone number, Date of birth, Age, the procedure done, and how they heard of the MBL. 
The caveat is that the information that needed to be pulled from the paper documents were hand written by the customer. 
So a means to extract the information from the documents was needed because of the time investment for going through each 
document and manually entering the information into the database. So an OCR program was necessary, that's where google's 
vision api is used to read the text from each document and extract the pertinent data and insert it into the database. 

Intended Audience

The audience of this software is the business owner of the Mobile Brow Lounge so that insights can be pulled from the 
extracted data and leveraged as marketing KPI for an ad campaign. 

Intended Use

The use of the software and the created database is to reveal insights about the MBL and its main customer base. 
This information is then used as leverage to create ad campaigns, email marketing campaigns, and social media posts. 

Scope

The scope of the project entails the customers of the MBL and the permanent makeup artist Rachelle Fallon. 
How she can use these data insights to bring in more clients and grow the small business and streamline that 
process by removing the need for paper record keeping.

Overall Description

The software operates by opening a jpg file within a folder called clients that contains 341 client jpegs. 
It opens one jpg at a time and the google vision api reads the jpg document and pulls all the text from the document. 
This text is assigned to a variable doctext and is separated into a list by indexing each item by the new line character. 
The doctext list is then iterated through and removing any unnecessary information and inserting only the necessary data into 
a list called clientInfo. Within googles api it sometimes reads the information poorly and outputs weird text. So the clientInfo 
list then is filtered for any discrepancies and then starting with the zeroith index and going to the eighth index should contain 
the Name, Date of procedure, Email, phone number, Date of birth, Age, the procedure done, and how they heard of the MBL respectively. 
This data is assigned to their respective variables and then used within the SQL insert statements. The populated database would then be queried to 
extract helpful insights into the business. 

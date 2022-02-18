from dataclasses import replace                         #importing the replace function
from http import client                                 
import os, io                                           
import mysql.connector                                  #importing the mysql connector 
import re
import Clients                                          #importing the client folder with the jpgs
from google.cloud import vision                         #importing the google cloud vision api 
from google.cloud.vision import Image

CLientDb = mysql.connector.connect(user='root', password='***********',         #creating the connection to the Mysql DB
                              host='127.0.0.1',                                 #that is hosted locally on my machine
                              use_pure=False)

cursor = CLientDb.cursor()

createDB = "CREATE DATABASE MBLclients"                                         #database creation sql statement

useDB = "USE MBLclients"                                                        #sql use statement 

createTB_1 = '''CREATE TABLE CLIENTS(
                                    CLIENT_ID INT AUTO_INCREMENT PRIMARY KEY,  
                                    NAME VARCHAR(35) NOT NULL, 
                                    DATE VARCHAR(35) NOT NULL,
                                    EMAIL VARCHAR(35) NOT NULL,
                                    PHONE_NUM VARCHAR(35) NOT NULL,
                                    CLIENT_DOB VARCHAR(50) NOT NULL
                                    )'''
                                                                                    #create table methods create two tables one storing the client pertinent information the other containing the procedure done and how the client was referred 
createTB_2 = '''CREATE TABLE PROCEDURES(
                                        CLIENT_ID INT AUTO_INCREMENT PRIMARY KEY,
                                        PROCEDURE_TYPE VARCHAR(35),
                                        REFFERED_BY VARCHAR(35)
                                        )'''
            
showClients = ''' SELECT * FROM CLIENTS'''

def ClientListRename():                                                 #this function iterates through the clients folder 
                                                                        #and renames the all the jpgs to for easy extraction of data later
    folder = 'Clients'
    
    for count, filename in enumerate(os.listdir(folder)):
        dst = f"Client{str(count)}.jpg"
        src =f"{folder}/{filename}"  
        dst =f"{folder}/{dst}"

        os.rename(src, dst)

def extractClientData(clientImage):                                                     #the extract client data function uses a jpg string name as an argument
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'          #and the jpg that is passed correlates to one mobile brow lounge client

    client = vision.ImageAnnotatorClient()                                             #setting the client to be used will be the image annotator

    FOLDER_PATH = "Clients"                                                             #specifying the folder and image path 
    IMAGE_FILE = clientImage                                                            
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)
        
    with io.open(FILE_PATH, 'rb') as image_file:                                        #opens and reads the image file 
        content = image_file.read()                                                     

    image = vision.Image(content = content)                                            #this google api function tells the api its an image and will be classified as one
    response = client.document_text_detection(image = image)                           #using the image annotator client set the response to document text detection method 
    docText = response.full_text_annotation.text.splitlines()                          #it then pulls all the text from image and places it in full text annotaion meaning 
                                                                                       #that it appears in the order the api extracted it from.Splitlines method then breaks the 
    global clientName                                                                  #string response into a list indexed based on every time a newline break occurs
    global clientDate       
    global clientEmail
    global clientPhone                                                                 #declaring the variables to be extracted from the response and used in the SQL statement
    global clientDOB 
    global clientPROC
    global refferedBy 

    n = 4                                                                              #4 is most often the index where the client information starts
    clientInfo = []                                                                    #creating an empty list to house the most important client info 
                                                                                       #to be extracted and placed into there respective variables
    while n <= 20:
        if (docText[n] != 'Name:') and (docText[n] !='Date:') and (docText[n] !='Email:') and (docText[n] !='Phone #:') and (docText[n] !='Date of Birth') and (docText[n] != 'What procedure(s) are you having done today?:') and (docText[n] !='How did you hear about The Brow Lounge? :') and (docText[n] != 'You have the right to be informed so that you may make the decision whether or not to undergo the procedure(s)') and (docText[n] != ':') and (docText[n] != 'print your contact information clearly.') and (docText[n] != 'You must read and fill out this form completely, making certain that you understand everything and'):
            clientInfo.append(docText[n])
        elif (docText[n] == 'You have the right to be informed so that you may make the decision whether or not to undergo the procedure(s)'):
            break
        n += 1
                                                                                       #the above while loops starts at index 4 of the doctext list and if the contents of index 4
    clientName = ""                                                                    #do not satisy the conditions then the content is appended to the empty client info list
    clientDate = ""                                                                    #I understand this may be a cumbersome way to extract the client data but the way google vision Api
    clientEmail = ""                                                                   #reads image files and assigns the the extracted text to blocks and paragraphs is different for 
    clientPhone = ""                                                                   #every image file that is read so a filtering mechanism needed to be created so that as the indexed
    clientDOB = ""                                                                     #item travels down the filter on the relevant information is getting extracted
    clientPROC = ""                                                                    #The relevant information being extracted from the jpg is handwritten text and the filtering while
    refferedBy = ""                                                                    #loop is weeding out the plain printed information until it reaches the You have the right to be ...

    x = 0
    
    while x <= len(clientInfo) - 1:
        placeHolder = ""
        placeHolder = clientInfo[x]                                                    #this while loop helps further filter out the printed text that couldve been lumped together 
        placeHolder = placeHolder.replace("Name:", "")                                 #with the handwriting when the api pulled the information, so that only the handwriting is extracted
        placeHolder = placeHolder.replace("Name", "")
        placeHolder = placeHolder.replace("name:", "")
        placeHolder = placeHolder.replace("Date:", "")
        placeHolder = placeHolder.replace("Email:", "")                                 #creating an empty string called place holder will then take the contents of clientInfo[x]
        placeHolder = placeHolder.replace("Phone #:", "")                               #and place it into the placeholder if the place holder contains any of the following it will
        placeHolder = placeHolder.replace("Phone #", "")                                #technically remove it and not replace and then strips the white spaces before the string
        placeHolder = placeHolder.replace("Phone :", "")
        placeHolder = placeHolder.replace("Date of Birth", "")
        placeHolder = placeHolder.replace("rth", "")
        placeHolder = placeHolder.lstrip()

        if len(placeHolder) > 4 and len(placeHolder) < 35:                              #in this conditional statement it asses the length of the string if the condition is not satisfied
            if x == 0:                                                                  #it removes the correlating index in the list, once the condition is satisfied it then drops into 
                clientName = placeHolder                                                #a nested condition at this point the extracted handwritten name of the client should be in the 
            elif x == 1:                                                                #clientInfo zeroith index so it then starts assigning the appropriate variables for the SQL statement
                clientDate = placeHolder
            elif x == 2:
                clientEmail = placeHolder
            elif x == 3:
                clientPhone = placeHolder
            elif x == 4:
                clientDOB = placeHolder
            elif x == 5:
                clientPROC = placeHolder
            elif x == 6:
                refferedBy = placeHolder
            else:
                break
            x += 1
        else:
            clientInfo.pop(x)
                                                                                    #the appropriate variables of the corresponding jpg have been assigned and can be
                                                                                    #now be used within the SQL insert statement to be inserted into the DB
                                                                                            
    insertClientData = (''' INSERT INTO CLIENTS(                                        
                                                NAME, 
                                                DATE, 
                                                EMAIL, 
                                                PHONE_NUM, 
                                                CLIENT_DOB
                                                )
                                        VALUES (
                                            %s, 
                                            %s, 
                                            %s, 
                                            %s, 
                                            %s
                                            )''',(
                                            clientName,
                                            clientDate,
                                            clientEmail,
                                            clientPhone,
                                            clientDOB                                            
                                            ))
    
    cursor.execute(*insertClientData)                                                               #exectution of the insert statement 

    CLientDb.commit()                                                                               #committing the insert statement to the DB
                                                                                                    #the table containingg the procedure type and how they referred can be instered now
    insertProcedureData = (''' INSERT INTO PROCEDURES(
                                                        PROCEDURE_TYPE,
                                                        REFFERED_BY
                                                        )
                                                VALUES (
                                                        %s,
                                                        %s
                                                        )''',(
                                                        clientPROC,
                                                        refferedBy
                                                        ))
    
    cursor.execute(*insertProcedureData)                                                            #executing the insert statement

    CLientDb.commit()                                                                               #committing the insert to the procedures table

    return clientName, clientDate, clientEmail, clientPhone, clientDOB, clientPROC, refferedBy

"""ClientListRename()"""                                                                            #this function is commented out because after a singular run doesnt need to be run again

cursor = CLientDb.cursor()                                                                          #creates the database cursor 

cursor.execute(createDB)                                                                            #creates the mbl_clients databse

cursor.execute(useDB)                                                                               #uses the mbl_clients database

cursor.execute(createTB_1)                                                                          #creates the clients table

cursor.execute(createTB_2)                                                                          #creates the procedures table



for i in os.listdir('Clients'):                                                                     #this loop iterates through the jpgs of the clients folder and extracts and inserts 
    extractClientData("{}".format(i))                                                               #each jpg iteration into the client databse 
    print(i, clientName, clientDate, clientEmail, clientPhone, clientDOB, clientPROC, refferedBy)   #printed each extraction to back check the client info was instered 

cursor.close()                                                                                      #closes the cursor and DB
CLientDb.close()
                                                                                                    #this code below was being used as testing information to see what was being instered into the DB
"""cursor.execute(useDB)

cursor.execute("SELECT * FROM clients")                                                             
                                                                                                    
result = cursor.fetchall()
  
for row in result:
    print(row)
    print("\n")"""






  

  






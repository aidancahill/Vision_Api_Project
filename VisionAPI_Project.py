from dataclasses import replace
from http import client
import os, io 
import mysql.connector
import re
import Clients
from google.cloud import vision
from google.cloud.vision import Image

CLientDb = mysql.connector.connect(user='root', password='aidscahill23',
                              host='127.0.0.1',
                              use_pure=False)

cursor = CLientDb.cursor()

createDB = "CREATE DATABASE MBLclients"

useDB = "USE MBLclients"

createTB_1 = '''CREATE TABLE CLIENTS(
                                    CLIENT_ID INT AUTO_INCREMENT PRIMARY KEY, 
                                    NAME VARCHAR(35) NOT NULL, 
                                    DATE VARCHAR(35) NOT NULL,
                                    EMAIL VARCHAR(35) NOT NULL,
                                    PHONE_NUM VARCHAR(35) NOT NULL,
                                    CLIENT_DOB VARCHAR(50) NOT NULL
                                    )'''

createTB_2 = '''CREATE TABLE PROCEDURES(
                                        CLIENT_ID INT AUTO_INCREMENT PRIMARY KEY,
                                        PROCEDURE_TYPE VARCHAR(35),
                                        REFFERED_BY VARCHAR(35)
                                        )'''
            
showClients = ''' SELECT * FROM CLIENTS'''

def ClientListRename():

    folder = 'Clients'
    
    for count, filename in enumerate(os.listdir(folder)):
        dst = f"Client{str(count)}.jpg"
        src =f"{folder}/{filename}"  
        dst =f"{folder}/{dst}"

        os.rename(src, dst)

def extractClientData(clientImage):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

    client = vision.ImageAnnotatorClient()

    FOLDER_PATH = "Clients"
    IMAGE_FILE = clientImage
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)
        
    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content = content)
    response = client.document_text_detection(image = image)
    docText = response.full_text_annotation.text.splitlines()
    
    global clientName 
    global clientDate 
    global clientEmail
    global clientPhone 
    global clientDOB 
    global clientPROC
    global refferedBy 

    n = 4
    clientInfo = []

    while n <= 20:
        if (docText[n] != 'Name:') and (docText[n] !='Date:') and (docText[n] !='Email:') and (docText[n] !='Phone #:') and (docText[n] !='Date of Birth') and (docText[n] != 'What procedure(s) are you having done today?:') and (docText[n] !='How did you hear about The Brow Lounge? :') and (docText[n] != 'You have the right to be informed so that you may make the decision whether or not to undergo the procedure(s)') and (docText[n] != ':') and (docText[n] != 'print your contact information clearly.') and (docText[n] != 'You must read and fill out this form completely, making certain that you understand everything and'):
            clientInfo.append(docText[n])
        elif (docText[n] == 'You have the right to be informed so that you may make the decision whether or not to undergo the procedure(s)'):
            break
        n += 1

    clientName = ""
    clientDate = ""
    clientEmail = ""
    clientPhone = ""
    clientDOB = ""
    clientPROC = ""
    refferedBy = ""

    x = 0
    
    while x <= len(clientInfo) - 1:
        placeHolder = ""
        placeHolder = clientInfo[x]
        placeHolder = placeHolder.replace("Name:", "")
        placeHolder = placeHolder.replace("Name", "")
        placeHolder = placeHolder.replace("name:", "")
        placeHolder = placeHolder.replace("Date:", "")
        placeHolder = placeHolder.replace("Email:", "")
        placeHolder = placeHolder.replace("Phone #:", "")
        placeHolder = placeHolder.replace("Phone #", "")
        placeHolder = placeHolder.replace("Phone :", "")
        placeHolder = placeHolder.replace("Date of Birth", "")
        placeHolder = placeHolder.replace("rth", "")
        placeHolder = placeHolder.lstrip()

        if len(placeHolder) > 4 and len(placeHolder) < 35:
            if x == 0:
                clientName = placeHolder
            elif x == 1:
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
    
    cursor.execute(*insertClientData)

    CLientDb.commit()

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
    
    cursor.execute(*insertProcedureData)

    CLientDb.commit()

    return clientName, clientDate, clientEmail, clientPhone, clientDOB, clientPROC, refferedBy

"""ClientListRename()"""

cursor = CLientDb.cursor()

cursor.execute(createDB)

cursor.execute(useDB)

cursor.execute(createTB_1)

cursor.execute(createTB_2)



for i in os.listdir('Clients'):
    extractClientData("{}".format(i))
    print(i, clientName, clientDate, clientEmail, clientPhone, clientDOB, clientPROC, refferedBy)

cursor.close()
CLientDb.close()

"""cursor.execute(useDB)

cursor.execute("SELECT * FROM clients")
   
result = cursor.fetchall()
  
for row in result:
    print(row)
    print("\n")"""






  

  






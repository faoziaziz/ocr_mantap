#!/usr/bin/python2

import mysql.connector
from mysql.connector import errorcode
import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
from PIL import Image
from io import BytesIO
import os
import sys


class OCR_gege:
    # connection variable
    DeviceId = None 
    RefSN = None 
    FlagImage = None 
    FlagTeks = None 
    ImageInput = None
    # config for database tutorial
    config = {}
    conn = None

    def __init__(self, host, username, password, port, database, refsn, data, flag):
        self.config['user']=username 
        self.config['host']=host 
        self.config['password']=password
        self.config['port']=port 
        self.confif['database']=database 
        self.FlagImage = flag 
        self.ImageInput = data
        self.conn = mysql.connector.connect(**self.config)

        self.getDataImage()
        
    def TranslateData(self):
        # Add your Computer Vision subscription key and endpoint to your environment variables.
        if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
            subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
        else:
            print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
            sys.exit()

        if 'COMPUTER_VISION_ENDPOINT' in os.environ:
            endpoint = os.environ['COMPUTER_VISION_ENDPOINT']



        ocr_url = endpoint + "vision/v2.1/ocr"

        # Set image_url to the URL of an image that you want to analyze.

        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {'language': 'unk', 'detectOrientation': 'true'}

        # Set Content-Type to octet-stream
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
        # put the byte array into your post request
        response = requests.post(ocr_url, headers=headers, params=params, data = self.ImageInput)


        response.raise_for_status()


        analysis = response.json()
        i =0
        # Extract the word bounding boxes and text.
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = [[]]


        limosins = line_infos[0]
        kataku =[]
        kataku2 =[]
        i = 0
        for limosin in limosins:
            
            for word_lines in limosin["words"]:
                kataku2.append(word_lines["text"]) 
            kilimanjaro = ' '.join(kataku2) 
            kataku.append(kilimanjaro)
            #print "silit"
            #print kataku
            del kataku2[:]
    
        self.translated_data = '\n'.join(kataku)
        print self.translated_data
        
    def getDataImage(self):
        get_image_query = "SELECT * FROM Image where Flag = 0"
        cursorget = self.conn.cursor()
        cursorget.execute(get_image_query)
        rows = cursorget.fetchall()

        for row in rows:
            print "Image"
            self.RefSN = 2 # seqnum dari Image
            self.ImageInput = 2 # data image
            self.DeviceId = 3 #device id
            self.TranslateData()
            #self.storeText()
            #self.updateFlag()
        # closing cursor
        cursorget.close()
    def storeText(self):
        insert_query = """ INSERT INTO `Teks` (`DeviceId`, 
                        `RefSN`, 
                        `Data`
                        ) VALUES (%s,%s,%s)"""
        curr.execute(insert_query, (
                                self.DevID, 
                                self.RefSN, 
                                self.translated_data
                            )
                        )

        self.conn.commit()
        cursorinsert = self.conn.cursor()
        cursorinsert.close()

    def updateFlag(self):
        cursorupdate = self.conn.cursor()
        cursorupdate.execute ("""
            UPDATE Image
            SET Flag=%s
            WHERE SeqNum=%s
            """, (self.FlagImage, self.RefSN))

        self.conn.commit()
        # update to query close
        cursorupdate.close()
    def __del__(self):
        # Destructor 

        self.conn.close()

print " Selamat datang para hadirin "

try:
    hostname = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    port = int(sys.argv[4])
    database = sys.argv[5]

    print " ok "+ username
    

except:
    print "yang anda masukan salah "
    print "./OCR_gege [hostname] [username] [password] [port] [database]"
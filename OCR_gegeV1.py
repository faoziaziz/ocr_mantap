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
    
    def __init__(self, host, username, password, port, database):
        print "init"
        self.config['user']=username 
        self.config['host']=host 
        self.config['password']=password
        self.config['port']=port 
        self.config['database']=database
	
	print (self.config) 
	try:
        	self.conn = mysql.connector.connect(**self.config)
	except mysql.connector.Error as err:
    		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        		print "mengalami error pada username dan password"
    		elif err.errno == errorcode.ER_BAD_DB_ERROR:
        		print "database tidak ada"
    		else:
        		print "Error lainnya : " + `err`

        self.getDataImage()
        
    def TranslateData(self):
        # Add your Computer Vision subscription key and endpoint to your environment variables.
        try:
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

            self.FlagImage=1
            self.translated_data = '\n'.join(kataku)
            print self.translated_data
        except:
            print "file image alay"
            self.translated_data = 'Image Allay'
            self.fileImage = 99

    def getDataImage(self):
        get_image_query = "SELECT * FROM Image where Flag = 0"
        cursorget = self.conn.cursor()
        cursorget.execute(get_image_query)
        rows = cursorget.fetchall()

        for row in rows:
            print "Image"
            self.RefSN = row[0] # seqnum dari Image
            print "da" + `self.RefSN` 
            ImageGet =  row[3] # data image
            fileImage = open("filegambar.png", "wb")
            fileImage.write(ImageGet)
            fileImage.close()
            self.ImageInput = open("filegambar.png", "rb").read()
            print type(self.ImageInput)
            self.DeviceId = row[1] #device id
            print "refsn "
            print self.RefSN
            self.TranslateData()
            self.storeText()
            self.updateFlag()
        # closing cursor
        cursorget.close()


    def storeText(self):
        cursorinsert = self.conn.cursor()
        insert_query = """ INSERT INTO `Teks` (`DeviceId`, 
                        `RefSN`, 
                        `Data`
                        ) VALUES (%s,%s,%s)"""
        cursorinsert.execute(insert_query, (
                                self.DeviceId, 
                                self.RefSN, 
                                self.translated_data
                            )
                        )

        self.conn.commit()
        
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
        self.conn.close()
    def __del__(self):
        # Destructor 
	print "self destruct"
        #self.conn.close()

print " Selamat datang para hadirin "

#try:
hostname = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
port = int(sys.argv[4])
database = sys.argv[5]

print " ok ["+ username+"] "
ocr_mulai = OCR_gege(hostname, username, password,port, database)

#except:
print "yang anda masukan salah "
print "./OCR_gege [hostname] [username] [password] [port] [database]"
import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
#import matplotlib.pyplot as plt
#from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO
import os
import sys
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


image_path = "filegambar.png"
# Read the image into a byte array
image_data = open(image_path, "rb").read()
# Set Content-Type to octet-stream
print "type image data"
print type(image_data)
headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
# put the byte array into your post request
response = requests.post(ocr_url, headers=headers, params=params, data = image_data)


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
  
translated_data='\n'.join(kataku)


print translated_data

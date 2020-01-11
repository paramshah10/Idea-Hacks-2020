import os
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
client = vision.ImageAnnotatorClient()

import io
path = 'images\IMG-1626.JPG'

with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.document_text_detection(image=image)
document = response.full_text_annotation
output_file = open("vision_output.txt","w")

document_text = str(document.text.encode(encoding='UTF-8'))

print("Reading image done")


output_file.write(document_text)
output_file.close()

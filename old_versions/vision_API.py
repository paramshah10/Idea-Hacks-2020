
import os, requests, time, io
from xml.etree import ElementTree
from google.cloud import vision

# This code is required for Python 2.7
try: input = raw_input
except NameError: pass

# Authenticating the code of google vision API with credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
client = vision.ImageAnnotatorClient()

path = 'IMG-1626.JPG'


def PictureToText():

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


######## Microsoft API code

'''
If you prefer, you can hardcode your subscription key as a string and remove
the provided conditional statement. However, we do recommend using environment
variables to secure your subscription keys. The environment variable is
set to SPEECH_SERVICE_KEY in our sample.
For example:
'''
subscription_key = "cb0355acc1b445b1987ad40abe95ba07"

#DON'T DELETE THIS CODE - USEFUL WHEN SET ENVIRONMENT VARIABLE RATHER THAN HARDCODING
##if 'SPEECH_SERVICE_KEY' in os.environ:
##    subscription_key = os.environ['SPEECH_SERVICE_KEY']
##else:
##    print('Environment variable for your subscription key is not set.')
##    exit()

class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        #self.tts = input("What would you like to convert to speech: ")
        myText = open("./vision_output.txt", "r")
        string1 = myText.read()
        myText.close()

        string1 = string1.replace(".\\n", ". ZZZZ")
        string1 = string1.replace("\\n", " ")
        string1 = string1.replace(". ZZZZ", ".\\n")
#        string1 = string1.decode('utf-8')

        self.tts = string1
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', 'en-US-Guy24kRUS') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)


        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        if response.status_code == 200:
            with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                global audio_file_name
                audio_file_name = 'sample-' + self.timestr + '.wav'
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            print("Reason: " + str(response.reason) + "\n")

    def get_voices_list(self):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/voices/list'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")


def playAudioFile():

    print("Going to start playing file " + audio_file_name)
    os.system('aplay ' + audio_file_name)
    print("Done playing")

if __name__ == "__main__":
    PictureToText()
    app = TextToSpeech(subscription_key)
    app.get_token()
    app.save_audio()
    playAudioFile()
    # Get a list of voices https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices
    # app.get_voices_list()

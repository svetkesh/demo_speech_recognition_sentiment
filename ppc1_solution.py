import os
import io
from google.cloud import speech
from google.cloud import language_v1


# Creates google client
client = speech.SpeechClient()

# Instantiates a client for google lagnguage service
lang_serv_client = language_v1.LanguageServiceClient()

# Full path of the audio file
file_name = os.path.join(os.path.dirname(__file__), "2021-01-03-23-52.flac")

#Loads the audio file into memory
with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)


config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    audio_channel_count=2,
    language_code="en-US",
)


# Sends the request to google to transcribe the audio
response = client.recognize(request={"config": config, "audio": audio})

full_transcript_list = []

# Reads the response
for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
    full_transcript_list.append(result.alternatives[0].transcript)

full_transcript = ' '.join(full_transcript_list)

document = language_v1.Document(content=full_transcript, type_=language_v1.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = lang_serv_client.analyze_sentiment(request={'document': document}).document_sentiment

print("Text: {}".format(full_transcript))
print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

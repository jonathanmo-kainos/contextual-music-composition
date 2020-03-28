import requests
from pprint import pprint
import json
import enums

with open(enums.EnvVars.AZURE_CONFIG_DIRECTORY_FILEPATH) as config_file:
    azure_config = json.load(config_file)
subscription_key = azure_config['subscription_key']
endpoint = azure_config['endpoint']
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
language_api_url = endpoint + '/text/analytics/v2.1/languages'
sentiment_api_url = endpoint + '/text/analytics/v2.1/sentiment'


def is_sentiment_negative(user_input_text):
    detected_language = detect_language_of_user_input_text(user_input_text)
    documents = {"documents": [
        {"id": "1", "language": detected_language,
         "text": user_input_text}
    ]}

    response = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()
    pprint(sentiments)

    if sentiments['documents'][0]['score'] < 0.5:
        print('User input has a negative sentiment')
        return True
    else:
        print('User input has a positive sentiment')
        return False


def detect_language_of_user_input_text(user_input_text):
    documents = {"documents": [
        {"id": "1", "text": user_input_text},
    ]}

    response = requests.post(language_api_url, headers=headers, json=documents)
    languages = response.json()
    pprint(languages)

    return languages['documents'][0]['detectedLanguages'][0]['iso6391Name']


def get_sample_type_based_on_user_input(user_input_text):
    if is_sentiment_negative(user_input_text):
        return 'minor'
    else:
        return 'major'

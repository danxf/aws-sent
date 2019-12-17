import json
from PhraseCollector import PhraseCollector
import boto3
from utilities_noreq import get_batches
import statistics
comprehend_client = boto3.client('comprehend')

def analyse(event, context):
    # Validating the phrase parameter and rejecting if too short
    if event["queryStringParameters"] and "phrase" in event["queryStringParameters"]:
        if len(event["queryStringParameters"]["phrase"]) <=2:
            response = {"statusCode": 200,
                    "body": "Phrase should be at least 3 characters long"
                    }
            return response
        else:
            phrase = event["queryStringParameters"]["phrase"]
    else:
        response = {"statusCode": 200,
                    "body": "Please specify phrase"
                    }
        return response
    
    
    #Gathering the stories which match the phrase
    try:
        phraseCollector = PhraseCollector(phrase, story_limit = 3, comment_limit = 15)
    except ValueError as e:
        response = {
        "statusCode": 416,
        "body": "API Error before any comments recieved"
        }
        return response
        
    #Getting the comment data which match the phrase
    matched_comment_data = phraseCollector.collect_data()
    if len(matched_comment_data) == 0:
        response = {
        "statusCode": 200,
        "body": "No matches found for given phrase"
        }
        return response
    
    comprehend_res = []
    #Using batch_detect_sentiment has a 25 document limit
    for batch in get_batches(matched_comment_data, 25):
        comprehend_res.extend(comprehend_client.batch_detect_sentiment(TextList = batch, LanguageCode = 'en')["ResultList"])
    comprehend_res = list(map(lambda x:x["SentimentScore"],comprehend_res))
    
    res_dict ={"comments" : len(comprehend_res),
             "positive" : {"average" : statistics.mean(map(lambda x:x["Positive"],comprehend_res)),
                           "median":statistics.median(map(lambda x:x["Positive"],comprehend_res))},
             "neutral" : {"average":statistics.mean(map(lambda x:x["Neutral"],comprehend_res)),
                           "median":statistics.median(map(lambda x:x["Neutral"],comprehend_res))},
             "negative" : {"average":statistics.mean(map(lambda x:x["Negative"],comprehend_res)),
                           "median":statistics.median(map(lambda x:x["Negative"],comprehend_res))},
             "mixed" : {"average":statistics.mean(map(lambda x:x["Mixed"],comprehend_res)),
                           "median":statistics.median(map(lambda x:x["Mixed"],comprehend_res))}
             }
    
    
    
    response = {
        "statusCode": 200,
        "body": json.dumps(res_dict)
    }
    
    
    
    
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

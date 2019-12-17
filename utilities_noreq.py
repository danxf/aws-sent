from urllib import request
import json
from html.parser import HTMLParser
API_URL = "https://hacker-news.firebaseio.com/"

def get_batches(l, batch_size):
    return (l[i:i + batch_size] for i in range(0, len(l), batch_size))
def get_top_stories():
    try:
        req = request.Request(API_URL + "v0/topstories.json")
        res = request.urlopen(req)
        #Read request, decode and pass to json parser
        return json.loads(res.read().decode('utf-8'))
    except Exception as e:
        return None
    

"""
Queries the API for JSON representation of the node
"""
def get_json(node_id):

    try:
        req = request.Request(API_URL + "v0/item/" + str(node_id) + ".json")
        res = request.urlopen(req)
        #Read request, decode and pass to json parser
        return json.loads(res.read().decode('utf-8'))
    except Exception as e:
        return None
    

class mod_parser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        
    def handle_data(self, data):
        self.container+=data
    def feed(self, data):
        self.container = ""
        HTMLParser.feed(self,data)
        


def parse_html_string(s):
    parser = mod_parser()
    parser.feed(s)
    return parser.container
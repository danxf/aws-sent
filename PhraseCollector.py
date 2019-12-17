from ItemTraverser import ItemTraverser
import utilities_noreq as utilities
import re
class PhraseCollector():
    def __init__(self, phrase, story_limit = 10, comment_limit = 15):
        if len(phrase) <= 2:
            raise ValueError("Phrase should be at least 3 characters")
        self.phrase = phrase
        
        #Creating a list of stories mathcing to phrase argument
        self.relevant_top_stories_id = []
        self.titles = []
        self.relevant_data = []
        self.per_story_comment_limit = comment_limit
        #Get the current front page
        self.top_stories = utilities.get_top_stories()
        if not self.top_stories:
            raise RuntimeError("API error")
        #Check for every item in front page if the story matches the phrase
        if story_limit>0:
            self.top_stories = self.top_stories[:story_limit]
        
                
        
    def get_stories(self):
        for top_story in self.top_stories:
            print("getting story {}".format(top_story))
            top_story_json = utilities.get_json(top_story)
            if not top_story_json:
                raise RuntimeError("API error")
            #Looking for a match in the title
            if re.search(self.phrase, utilities.parse_html_string(top_story_json["title"]),re.IGNORECASE):
                self.relevant_top_stories_id.append(top_story_json["id"])
                self.titles.append(top_story_json["title"])
                
            
    def print_titles(self):
        for x in self.titles:
            print(x)

    
    def collect_data(self):
        self.get_stories()
        for i,relevant_story_id in enumerate(self.relevant_top_stories_id):
            #print("Doing item no. {} / {}".format(i+1,len(self.relevant_top_stories_id)))
            itemTrav = ItemTraverser(relevant_story_id, 
                                     limit = self.per_story_comment_limit)
            data_from_story_id = itemTrav.get_comments()
            self.relevant_data.extend(data_from_story_id)
        
        #Clean comments from HTML tags and remove links from comments
        self.relevant_data = list(map(lambda x: re.sub(r'https?:\/\/.*[\r\n]*','',x),map(utilities.parse_html_string, self.relevant_data)))
        #self.relevant_data = list(map(utilities.parse_html_string, self.relevant_data))
        return self.relevant_data


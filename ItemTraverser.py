import utilities_noreq as utilities


    
class ItemTraverser:
    def __init__(self, root_id, limit=10):
        #print("Processing item {}".format(root_id))
        self.root = root_id
        self.kids = set()
        self.kids_text = []
        self.processed_kids = set()
        self.non_processed_kids = set()
        root_json = utilities.get_json(self.root)
        if root_json:
            if "kids" in root_json:
                for kid_id in root_json["kids"]:
                    self.kids.add(kid_id)
                    self.non_processed_kids.add(kid_id)
        else:
            #raise Exception("API query failed")
            pass
        self.Ndescendants = root_json["descendants"]
        self.limit = limit
        self.cache = dict()
    """
    Since the top level comments are retreived during instance creation and are unreachable by 
    other nodes we might want to check for new top-level comments after a certain period of time
    to have up-to-date data on the root_id node.
    """
    def update_roots_children(self):
        root_json = utilities.get_json(self.root)
        if root_json:
            if "kids" in root_json:
                for kid_id in root_json["kids"]:
                    self.kids.add(kid_id)
                    if kid_id not in self.processed_kids:
                        self.non_processed_kids.add(kid_id)
        else:
            #raise Exception("API query failed")
            pass

    """
    Traverse all nodes and their children which are currently in non_processed_kids
    """
    def traverse(self):
        while len(self.non_processed_kids) > 0:
            #testing for the optional limit parameter, we might not want to collect very large threads
            if self.limit > 0 and len(self.kids_text) >= self.limit:
                break
            kid_id = self.non_processed_kids.pop()
            
            #If we already processed kid continue
            if kid_id in self.processed_kids:
                continue
            
            #Get kid JSON, extract the text and add it's children, finally mark the kid as seen
            if kid_id in self.cache:
                kid_json = self.cache[kid_id]
            else:   
                kid_json = utilities.get_json(kid_id)
                self.cache[kid_id] = kid_json
            if not kid_json:
                continue
            if "text" in kid_json: #some comments might be deleted   
                print("Added comment {}".format(kid_id))
                self.kids_text.append(kid_json["text"])
            #checking if any more kids available and adding them
            if "kids" in kid_json:
                for kids_kid in kid_json["kids"]:
                    self.kids.add(kids_kid)
                    self.non_processed_kids.add(kids_kid)
            self.processed_kids.add(kid_id)
    
    def get_comments(self):
        self.traverse()
        return self.kids_text
    
    def done(self):
        #some nodes might be added during the collection
        return self.Ndescendants <= len(self.processed_kids)
    

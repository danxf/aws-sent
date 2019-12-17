# Modules used
* `urllib` - Used to handle HTTP requests for HN API
* `json` - Decoding requests from HN API
* `HTMLParser` - Used to remove tags and other unnecessary information from the retrieved HN text.
* `re` - Used for case insensitive pattern matching and removing URL's from text
* `statistics` - Mean and median calculation
All of the modules are part of the Python standard library and were specifically chosen to be this way in order to prevent over-complicating the deployment process to AWS. It would have been easier to use `requests` module instead of `urllib` since it offers a cleaner interface for HTTP requests and can easily detect the correct encoding for JSON parsing. Also `HTMLParser` is a bit difficult to work with and using something like `BeautifulSoup` would have been much nicer.

# Project Modules
* `ItemTraverser` - Holds ID number of a news item. `get_comments()` method is used to traverse the comments of the item and will return all the comments under the item.
* `PhraseCollector` - Scans the front page for news item that match the given phrase. Instantiates `ItemTraverser` objects for each of the items that match and then parses, cleans and aggregates all of the data that was returned by each object.

# Handler
The function verifies that a key phrase was given and that it is not too short. A `PhraseCollector` object is created to gather the relevant data. Then we check if any matches were found. AWS's Sentiment Analysis service is then used on the collected data. We apply basic statistics on the results and post them to the user. 

Due to the AWS timeout and the time it takes to recieve the API requests this version can only handle scanning through a limited number of top posts and their comments. The parameter which control the number of top posts to scan is `story_limit` and `comment_limit` controls maximum number of comments gathered per matched post.

# Future work
* Add cache. We can either cache comments or complete threads. Caching comments is the simplest, caching entire threads will require some timeout mechanism since new comments might be added and we might work on irrelevant data. 
* Add concurrency for API calls. Right now we make subsequent HTTP requests to the firebase API which is very slow. We can intorduce some concurrency by either using threads or by using a library like `tornado` which offers asynchronous calls.
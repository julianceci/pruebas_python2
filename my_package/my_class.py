#Imports
from token_utils import tokenize
from collections import Counter

# Define Document class
class Document:
    """A class for text analysis
    
    :param text: string of text to be analyzed
    :ivar text: string of text to be analyzed; set by `text` parameter
    """
    # Method to create a new instance of MyClass
    def __init__(self, text):
        # Store text parameter to the text attribute
        self.text = text
        # Tokenize the document with non-public tokenize method
        self.tokens = self._tokenize()
        # Perform word count with non-public count_words method
        self.word_counts = self._count_words()

    def _tokenize(self):
        return tokenize(self.text)
        
    # non-public method to tally document's word counts with Counter
    def _count_words(self):
        #pass
        #return Counter(self.tokens) # no se porque no anda esto!
        return Counter(self.text)


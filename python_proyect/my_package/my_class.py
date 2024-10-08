#Imports
#from token_utils import tokenize
from collections import Counter
import re

# Define Document class
class Document:
    """
    A class for text analysis.

    Attributes:
        text (str): string of text to be analyzed
        tokens (list[Any]): ...
        word_counts (Counter): ...

    Methods:
        _tokenize() ->  list[Any]:
            Returns ...
        _count_words() -> Counter:
            Returns ...
    """
    
    # Method to create a new instance of MyClass
    def __init__(self, text):
        """
        Initializes a new Car instance.

        Args:
            text (str): string of text to be analyzed
            tokens (list[str]): ...
            word_counts (Counter): ...
        """
        # Store text parameter to the text attribute
        self.text = text
        # Tokenize the document with non-public tokenize method
        self.tokens = self._tokenize()
        # Perform word count with non-public count_words method
        self.word_counts = self._count_words()

    def _tokenize(self):
        """
        Tokenizing the text.

        This method returns a tokenized text
        """
        #return tokenize(self.text)
        return re.findall(r'\b\w+\b', self.text.lower())
        
    # non-public method to tally document's word counts with Counter
    def _count_words(self):
        """
        Counting characters.

        This method returns a Counter
        """
        #pass
        #return Counter(self.tokens) # no se porque no anda esto!
        return Counter(self.text)



#-------------------------------------------------
# Clases + packages

import my_package

#help(my_package)

datacamp_tweets = "a e i o u"

# create a new document instance from datacamp_tweets
datacamp_doc = my_package.Document(datacamp_tweets)

print(datacamp_doc.text)

# print the first 5 tokens from datacamp_doc
print(datacamp_doc.tokens)

# print the top 5 most used words in datacamp_doc
print(datacamp_doc.word_counts)

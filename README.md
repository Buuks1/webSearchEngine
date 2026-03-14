# Buks' Webpage Search Engine

Project Description
A small scale project that uses python code to develop an information retrieval system (search engine) for html videogame files using tf-idf term weighting and other advanced forms of representation. The system has a simple command line interface to run search queries allowing for single and multiple term queries to be entered from the keyboard and returns a ranked list of URLs & content to the console and a file.

Features
  -HTML Parsing using BeautifulSoup from BS4
  -Uses punctation removal, tokenisation and lemmatization to process words
  -Filters out stopwords with NLTK
  -Uses tf-df formula to calculate the weighing of words
  -Uses cosine similarity to rank search results
  -UI is user-friendly and easy to use
  -Displays ranked search results, with file content and saves results to a pickle file.

Dependencies
  -Libraries that are required for this program is:
  -Pickle
  -Os
  -Math
  -RegEx
  -NLTK
  -Bs4
  -Regex
  -String
  -SpaCy
All must be downloaded for program to run


Setup Instructions
Assuming the program is already on the machine:
  1.	Download all dependencies if not already
  2.	Change the ‘setdir’ variable to which ever directory you would like to search
  3.	Run the program (For now it can only be ran in a python IDE)

How It Works

The search engine extracts text content from HTML files by reading and parsing them. It filters out common stopwords and tokenises, lemmatises, and removes punctuation. Tokens are then mapped to the texts in which they occur using an inverted index. For every token, the term frequency (tf) and inverse document frequency (idf) are computed. The users’ search input is then tokenised and its tf-idf is then computed too. The documents are then ordered according to their similarity scores once the cosine similarity between the query and document vectors has been calculated. The results are then saved to a pickle file and the top 10 is displayed.

Troubleshooting
Please understand that due to the many low-level syscalls and large iterations used to operate this program, the code is very expensive and might take a few seconds to load before any prompt appears to allow a search.

Module Not Found Error: This means you do not have all of the dependencies downloaded, ensuring they are downloaded should solve this issue.

No Relevant Documents Found: This could mean two things. Either the files in the selected directory wasn’t properly opened and loaded or the search query has no relevance because it is not in the html files in the directory or its too vague. Ensure the correct directory is selected and change the search query, if this issue persists then it means there is an issue with the ‘setdir’ variable. If this doesn’t solve the problem, then the issue is your search.

import os
import math
import string
import regex as re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy

lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

#This class helps me store important arrays and lists
class SearchEngine:
    def __init__(self):
        self.inverted_index = {}
        self.document_tokens = {}
        self.tf_scores = []
        self.idf_scores = {}
        self.tf_idf_scores = []

#This computes the tf-idf for the words in the provided html files
    def compute_tf_idf(self):
        num_of_docs = len(self.document_tokens)
        
        # Compute TF Scores
        for doc_id, tokens in self.document_tokens.items():
            tf_dict = {}
            for token in tokens:
                tf_dict[token] = tf_dict.get(token, 0) + 1
            self.tf_scores.append({term: 1 + math.log10(count) if count > 0 else 0 for term, count in tf_dict.items()})

        # Compute IDF Scores
        for term, doc_list in self.inverted_index.items():
            df = len(doc_list)
            self.idf_scores[term] = math.log10(num_of_docs / df) if df > 0 else 0

        # Compute TF-IDF Scores
        self.tf_idf_scores = []
        for tf_dict in self.tf_scores:
            self.tf_idf_scores.append({term: tf * self.idf_scores.get(term, 0) for term, tf in tf_dict.items()})

#This is my tokenisation function used for both information storing and retreival
    def tokenising(self, text):
        inline_cleanse = re.sub(r'\s+', ' ', text)
        punc_cleanse = re.sub(f"[{string.punctuation}]", ' ', inline_cleanse)
        tokenising = nlp(punc_cleanse)
        cleaning = [token.text.strip() for token in tokenising if token.text.strip()]
        stopwords_cleanse = [word for word in cleaning if word not in stop_words]
        lemmatizing = [lemmatizer.lemmatize(word) for word in stopwords_cleanse]
        return lemmatizing

#This computes tf-idf for the query search
    def compute_query_tf_idf(self, query_tokens):
        tf_query = {}
        for token in query_tokens:
            tf_query[token] = tf_query.get(token, 0) + 1

        total_tokens = len(query_tokens)
        tf_idf_query = {term: (1 + math.log10(count)) * self.idf_scores.get(term, 0) 
                        for term, count in tf_query.items()}
        
        return tf_idf_query

#This is my calculations for cosine_similarity
    def cosine_similarity(self, doc_vector, query_vector):
        dot_product = sum(doc_vector.get(term, 0) * query_vector.get(term, 0) for term in query_vector)
        doc_magnitude = math.sqrt(sum(val ** 2 for val in doc_vector.values()))
        query_magnitude = math.sqrt(sum(val ** 2 for val in query_vector.values()))
        
        if doc_magnitude == 0 or query_magnitude == 0:
            return 0
        
        return dot_product / (doc_magnitude * query_magnitude)

#This function process the search
    def search_documents(self, query):
        query_tokens = self.tokenising(query)
        query_tf_idf = self.compute_query_tf_idf(query_tokens)

        # This computes the search similarity using my cosine function
        ranked_results = []
        for doc_id, doc_vector in enumerate(self.tf_idf_scores):
            score = self.cosine_similarity(doc_vector, query_tf_idf)
            if score > 0:
                ranked_results.append((doc_id, score))
        
        # This sorts score in descending order
        ranked_results.sort(key=lambda x: x[1], reverse=True)
        

        return ranked_results[:10]  #This ensures only the first 10 is returned and stored as results

#This function prints the scores to 4 decimal places
    def display_results(self, results, file_paths):
        if not results:
            print("No relevant documents found.")
            return
        
        for rank, (doc_id, score) in enumerate(results, 1):
            with open (file_paths[doc_id], 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser').get_text()
                cleansed_content = re.sub(r'\s+', ' ', soup)
            print(
                f"""Rank {rank}: {file_paths[doc_id]} (Score: {score:.4f})
                {cleansed_content}
                
                """)


# Directory can be changed here
setdir = 'C:/Users/Bukun/OneDrive/Documents/Uni work/IR/Project/videogames/videogames/'

# Initialize the search engine
search_engine = SearchEngine()

# (Sidenote) If this was java, int main would start here
file_paths = []
for doc_id, filename in enumerate(os.listdir(setdir)):
    if filename.endswith('.html'):
        file_path = os.path.join(setdir, filename)
        file_paths.append(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            soup = BeautifulSoup(content, 'html.parser').get_text()
            tokens = search_engine.tokenising(soup)
            search_engine.document_tokens[doc_id] = tokens

            for token in tokens:
                if token not in search_engine.inverted_index:
                    search_engine.inverted_index[token] = []
                if doc_id not in search_engine.inverted_index[token]:
                    search_engine.inverted_index[token].append(doc_id)

# Compute TF-IDF for all documents
search_engine.compute_tf_idf()

print ("Welcome to Buk's search engine")
while True:
    query = input("Enter search here >").lower()
    results = search_engine.search_documents(query)

    # Display the top 10 results
    search_engine.display_results(results, file_paths)
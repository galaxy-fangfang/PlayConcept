#here goes the code.
import csv
from llama_index.embeddings.ollama import OllamaEmbedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

import json

ollama_embedding = OllamaEmbedding(
    model_name="llama2",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)

def cosine_similarity(vec1, vec2):
   #vec1 = np.array(vec1).reshape(1, -1)  # Reshape to 2D array
   #vec2 = np.array(vec2).reshape(1, -1)
   #similarity = sklearn_cosine_similarity(vec1,vec2)
   dot_product = np.dot(vec1, vec2)
   norm_vec1 = np.linalg.norm(vec1)
   norm_vec2 = np.linalg.norm(vec2)
   similarity = dot_product / (norm_vec1 * norm_vec2)
   #print(similarity)
   return similarity

def find_similar_words(d1, d2, threshold=0.0):
   result = {}

   for word1, vec1 in d1.items():
       best_match = None
       best_similarity = threshold  # Initialize with the threshold
       best_match = []
       for word2, vec2 in d2.items():
           similarity = cosine_similarity(vec1, vec2)
           if similarity > best_similarity:
               best_similarity = similarity
               best_match.append(word2)

       if best_match is not None:
           result[word1.replace(" ",",")] = best_match

   return result


dict_concepts = {}
dict_codes = {}

##CONCEPTS##
lines = []

with open('list.txt', 'r') as file:
    #lines = [line.strip() for line in file]
    for line in file:
    	embedding = ollama_embedding.get_query_embedding(line.replace("\n",""))
    	dict_concepts[line.replace("\n","")] = embedding



##CODES##
processed_rows = []

with open("codes.csv", "r") as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader(csv_file)
    
    for row in csv_reader:
        # remove the first column
        row = row[1:]
        sentence = ' '.join(row)

        embedding = ollama_embedding.get_query_embedding(sentence)
        dict_codes[sentence] = embedding



selected_concepts = find_similar_words(dict_codes, dict_concepts)

print(len(selected_concepts))

# write the dict to a json file
with open('candidates.json', 'w') as json_file:
    json.dump(selected_concepts, json_file, indent=4)


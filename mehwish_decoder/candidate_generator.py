#here goes the code.
import csv
from llama_index.embeddings.ollama import OllamaEmbedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from wikipedia2vec import Wikipedia2Vec

import json

ollama_embedding = OllamaEmbedding(
    model_name="llama2",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)

def get_cosine_similarity(vec1, vec2):
   #vec1 = np.array(vec1).reshape(1, -1)  # Reshape to 2D array
   #vec2 = np.array(vec2).reshape(1, -1)
   #similarity = sklearn_cosine_similarity(vec1,vec2)
   dot_product = np.dot(vec1, vec2)
   norm_vec1 = np.linalg.norm(vec1)
   norm_vec2 = np.linalg.norm(vec2)
   sim = dot_product / (norm_vec1 * norm_vec2)
   norm_sim = (sim + 1) / 2
   return norm_sim

def find_similar_words(d1, d2, threshold=0.75):
   result = {}

   for word1, vec1 in d1.items():
        best_match = None
        best_similarity = threshold  # Initialize with the threshold
        best_match = []
        for word2, vec2 in d2.items():
        	#print(len(vec1))
        	#print(len(vec2))
        	similarity = get_cosine_similarity(vec1, vec2)
        	print(similarity)
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

#wiki2vec = Wikipedia2Vec.load('enwiki_20180420_win10_100d.pkl') ##filename

with open('list.txt', 'r') as file:
	embedding = []
	#lines = [line.strip() for line in file]
	for line in file:
		#try:
		#	embedding = wiki2vec.get_word_vector(line.replace("\n",""))
		#except Exception as e:
		#	print(e)

		#if embedding:
		#	dict_concepts[line.replace("\n","")] = embedding
		#else:
		#np.random.rand(100)
		embedding = ollama_embedding.get_query_embedding(line.replace("\n",""))
		dict_concepts[line.replace("\n","")] = embedding

		#print(line)
		#print(embedding)





    	#embedding = ollama_embedding.get_query_embedding(line.replace("\n",""))
    	


##CODES##
processed_rows = []

with open("codes.csv", "r") as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader(csv_file)
    
    for row in csv_reader:
    	embedding = []
    	# remove the first column
    	row = row[1:]
    	vectors = [ollama_embedding.get_query_embedding(token) for token in row]
    	embedding = np.mean(vectors, axis=0)
    	##average_vector = np.mean(vectors, axis=0)
    	sentence = ' '.join(row) #activate for ollama embeddings
    	#try:
    	#	embedding = wiki2vec.get_word_vector(sentence)
    	#except Exception as e:
    	#	print(e)

    	#if embedding:
    	dict_codes[sentence] = embedding
    	#else:
    	#	np.random.rand(100)
    	#	embedding = ollama_embedding.get_query_embedding(sentence)
    	#	dict_codes[sentence] = embedding
    		#embedding = ollama_embedding.get_query_embedding(sentence)
    		#dict_codes[sentence] = embedding

#print(dict_codes)
#print(dict_concepts)
selected_concepts = find_similar_words(dict_codes, dict_concepts)

print(len(selected_concepts))

# write the dict to a json file
with open('candidates_075.json', 'w') as json_file:
    json.dump(selected_concepts, json_file, indent=4)


 #pip install wikipedia2vec
 #download pretrained model from: https://wikipedia2vec.github.io/wikipedia2vec/pretrained/ 


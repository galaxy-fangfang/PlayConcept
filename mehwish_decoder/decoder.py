from decoderutils.utils import get_words, partition_candidates, encode
import json
from langchain.llms import Ollama
ollama = Ollama(base_url='http://localhost:11434', model="llama2")


def ask_llama(prompt):

    answer = ollama(prompt)

    return answer

def code2words(codes):

    with open("codes.csv") as file:
        lines = file.read().split("\n")
        codes = [line.split(",") for line in lines]
        #print(codes)
    
    # Translate the codes into the corresponding words
    nl_codes = get_words(code, codes)
    return nl_codes

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data


def get_candidates(json_data,words):
    candidates = []
    for i in words:
        if i[0] in json_data:
            candidates.append(json_data[i[0]])
        else:
            print(f"Key '{i[0]}' not found in the JSON data.")
    #print(candidates)
    all_candidates = set()
    for lst in candidates:
        all_candidates = all_candidates.union(set(lst))

    return list(all_candidates)

def extract_concepts(code):

    # Extract main concept and associated concepts from the first sublist
    main_concept = code[0][0].split(',')
    associated_concepts = [sub.split(',') for sub in code[0][1:]]

    # Print main concept and associated concepts
    prompt = f"Main Concept: {main_concept} \n "
    if associated_concepts:
        for associated_concept in associated_concepts:
            prompt = prompt + f"Associated Concept: {associated_concept} \n "

    # Extract and print sub concepts from the remaining sublists
    for i, sublist in enumerate(code[1:], start=2):
        sub_concept = sublist[0].split(',')
        associated_concepts = [sub.split(',') for sub in sublist[1:]]
        prompt = prompt + (f"\nSub Concept: {sub_concept}\n ")
        for j, associated_concept in enumerate(associated_concepts):
            prompt = prompt + (f"Associated Concept {j+1}: {associated_concept} \n")
    return prompt


def decode(code, candidates):
    """Decoder for Concept.

    Parameter
    ---------
    code: list of lists of integers
        Each list corresponds to a marker, starting with the green.
        The first element of each list is the marker (= question / exclamation mark), the others are the attributes (= cubes).
        There are at most 5 lists, each of length at most 10.

    candidates: list of str
        Candidate concepts.
        
    Returns
    -------
    concept: str
        Concept.
        
    Example
    -------
    Candidates = ['Apple', 'Honey', 'House']
    Code = [[26], [6]]
    Decoding = Food (main concept) related to an animal (secondary concept).
    Expected concept = 'Honey'
    """
    
    
    #return candidates
    
    # concept = ''
    # return 

    print(code)
    print(candidates)

    with open('prompt_cot.txt', 'r') as file:
        # Read the contents of the file into a variable
        file_contents = file.read()

        # Now, the variable file_contents contains the contents of the text file
    prompt_template = file_contents

    candidates_final = ', '.join(candidates)
    final_prompt = prompt_template + extract_concepts(code)+"\n Candidates: "+ candidates_final + "\n Answer Concept: ?"

    answer = ask_llama(final_prompt)

    print(answer)


if __name__ == "__main__":

    # Path to the JSON file
    file_path = 'candidates.json'
    json_data = read_json_file(file_path)

    #candidates = ['Apple', 'Honey', 'House']
    code = [[26], [6]]

    words = code2words(code)
    candidates = get_candidates(json_data,words)

    #print(candidates)
    decode(words,candidates)

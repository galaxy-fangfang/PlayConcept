from decoderutils.utils import get_words
import json
from langchain.llms import Ollama
import warnings




def ask_llama(prompt):

    answer = ollama(prompt)

    return answer

def code2words(codes):

    with open("codes.csv") as file:
        lines = file.read().split("\n")
        codes = [line.split(",") for line in lines]
        #print(codes)
    
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

    all_candidates = set()
    for lst in candidates:
        all_candidates = all_candidates.union(set(lst))

    return list(all_candidates)

def extract_concepts(code):

    main_concept = code[0][0].split(',')
    associated_concepts = [sub.split(',') for sub in code[0][1:]]

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

    with open('prompt_cot.txt', 'r') as file:
        file_contents = file.read()

    prompt_template = file_contents

    candidates_final = ', '.join(candidates)
    final_prompt = prompt_template + extract_concepts(code)+"\n Choose top5 answer concepts from the following candidates: "+ candidates_final + "\n Answer Concept: ?"

    answer = ask_llama(final_prompt)

    print("********************PROMPT START********************")
    print(final_prompt)
    print("********************PROMPT END********************")
    print("*****")
    print("*****")
    print("Answer: ")
    print(answer)


if __name__ == "__main__":

    #warnings.filterwarnings("ignore")
    ollama = Ollama(base_url='http://localhost:11434', model="llama2")


    file_path = 'candidates_075.json'
    json_data = read_json_file(file_path)

    #candidates = ['Apple', 'Honey', 'House']
    code = [[26], [6]]

    words = code2words(code)
    candidates = get_candidates(json_data,words)

    decode(words,candidates)

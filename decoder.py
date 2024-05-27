from decoderutils.utils import get_words, partition_candidates, encode
from langchain.llms import Ollama
ollama = Ollama(base_url='http://localhost:11434', model="llama2")


def ask_llama(prompt):

    answer = ollama(prompt)

    return answer




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
    
    
    # Samuel: Here is a suggestion that uses template prompts from the decoderutils/utils.py. Th eidea it to use each color to filter the list and to return the final list after all filters. To help the model, I divide the list into chunks (the size can be set in the function`partition_candidates`). Finally, to account for complex strategy such a discribing a country through its flag, I also add a prompt to ask the model to suggest an expression based on the code.
    
    # Retrieve the content from codes.csv file
    codes=[]

    with open("codes.csv") as file:
        lines = file.read().split("\n")
        codes = [line.split(",") for line in lines]
        #print(codes)
    
    # Translate the codes into the corresponding words
    nl_codes = get_words(code, codes)
    #print(nl_codes)
    
    # For each concept (each color), ask OLLAMA to filter the current list of candidates based either on the codes or on the expression
    for sub_code in nl_codes:

        #print(sub_code)
    
        # Ask OLLAMA for an expression based on the prompt, e.g. a "flag,country,location" that is "cross" and "red" and "white" and "blue" is the "union jack" or england
        prompt = expression_prompt.format(f'"{sub_code[0].replace(",",", ")}"', " and ".join([f'"{elt}"' for elt in sub_code[1:]]))
        print(prompt)
        expression = ask_llama(prompt)
        print(expression)
    
        ## Get answers based on the code and on the expression
        '''filter_candidates = set()
    
        # Divide the list of candidates to hep the model
        for subset_candidates in partition_candidates(candidates, chunk_size=50):
            # Ask OLLAMA for the answer based on the code
            prompt = base_prompt.format(f'"{sub_code[0]}"', " and ".join([f'"{elt}"' for elt in sub_code[1:]]),"\n".join(subset_candidates))
            filter_candidates |= set(ask_OLLAMA(prompt))
        
            # Ask OLLAMA for the answer based on the expression
            prompt = base_prompt_with_expression.format(f'"{expression}"', "\n".join(subset_candidates))
            filter_candidates |= set(ask_OLLAMA(prompt))
            
            # Consider the selected elements as the candidate for next concept
            candidates = list(filter_candidates)'''
    
    # Return the set of filtered candidates after each concept because it seems that the instructions have changed about the output type (a list instead of a single gess)
    return candidates
    
    # concept = ''
    # return 


candidates = ['Apple', 'Honey', 'House']
code = [[26], [6]]
decode(code,candidates)

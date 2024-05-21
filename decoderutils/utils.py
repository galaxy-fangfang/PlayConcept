import numpy as np

base_prompt = '''Select the elements of this list that best fit a {} which is {}:

{}'''

base_prompt_with_expression = '''Select the elements of this list that best fit {}:

{}'''

expression_prompt = 'What would be the expression / name that would best fit a {} that is {}?'
        
def get_words(code, codes):
    nl_code = []
    for concept in code:
        concept_nl_code = []
        for subconcept in concept:
            concept_nl_code.append(",".join(codes[subconcept][1:]))
        nl_code.append(concept_nl_code)
    return nl_code
    
def partition_candidates(candidates, chunk_size=50):
    ids = np.arange(len(candidates))
    np.random.shuffle(ids)
    ret = []
    for i in range(0,len(candidates), chunk_size):
        chunk_ids = ids[i:i+chunk_size]
        ret.append([candidates[j] for j in chunk_ids])
    return ret
    
def decode(code, candidates):
  # Retrieve the content from codes.csv file
with open("codes.csv") as file:
    lines = file.read().split("\n")
codes = [line.split(",") for line in lines]
return codes

  # Retrieve the templated prompts
  base_prompt = base_prompt
  expression_prompt = expression_prompt
  base_prompt_with_expression = base_prompt_with_expression

  # Translate the codes into the corresponding words
  nl_codes = get_words(code, codes)
  
  # For each concept (each color), ask OLLAMA to filter the current list of candidates based either on the codes or on the expression
  for sub_code in nl_codes:

    # Ask OLLAMA for an expression based on the prompt, e.g. a "flag,country,location" that is "cross" and "red" and "white" and "blue" is the "union jack" or england
    prompt = expression_prompt.format(f'"{sub_code[0]}"', " and ".join([f'"{elt}"' for elt in sub_code[1:]]))
    expression = ask_OLLAMA(prompt)

    ## Get answers based on the code and on the expression
    filter_candidates = set()

    # Divide the list of candidates to hep the model
    for subset_candidates in partition_candidates(candidates):
      # Ask OLLAMA for the answer based on the code
      prompt = base_prompt.format(f'"{sub_code[0]}"', " and ".join([f'"{elt}"' for elt in sub_code[1:]]),"\n".join(subset_candidates))
      filter_candidates |= set(ask_OLLAMA(prompt))

      # Ask OLLAMA for the answer based on the expression
      prompt = base_prompt_with_expression.format(f'"{expression}"', "\n".join(subset_candidates))
      filter_candidates |= set(ask_OLLAMA(prompt))
    
    # Consider the selected elements as the candidate for next concept
    candidates = list(filter_candidates)

  # Return the set of filtered candidates after each concept
  return candidates
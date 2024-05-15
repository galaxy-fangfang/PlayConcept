import csv

def get_words(code):
    with open("codes.csv") as file:
        lines = file.read().split("\n")
    codes = [line.split(",") for line in lines]
    nl_code = []
    for concept in code:
        concept_nl_code = []
        for subconcept in concept:
            concept_nl_code.append(",".join(codes[subconcept][1:]))
        nl_code.append(concept_nl_code)
    return nl_code
    
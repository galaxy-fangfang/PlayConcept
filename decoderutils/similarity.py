import ollama
from scipy.spatial import distance
import numpy as np

def search_simple(guess, candidates, k=2):
  emb_candidates = [
    ollama.embeddings(
      model='mxbai-embed-large',
      prompt=candidate,
    )['embedding'] for candidate in candidates
  ]
  emb_guess = ollama.embeddings(
    model='mxbai-embed-large',
    prompt=guess,
  )['embedding']

  # Calculate cosine similarities
  cosine_emb = [
    (candidate, distance.cosine(emb_guess, emb_candidate)) for candidate, emb_candidate in
    zip(candidates, emb_candidates)
  ]

  # Sort based on similarity scores in descending order
  cosine_emb.sort(key=lambda x: x[1], reverse=True)

  # Return the top k candidates and their scores
  return cosine_emb[:k]
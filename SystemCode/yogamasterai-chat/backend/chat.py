import sys
from transformers import pipeline

# Init nlp model
nlp = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# User input
user_input = sys.argv[1]
response = nlp(user_input, max_length=100)

# Print feedback
print(response[0]['generated_text'])

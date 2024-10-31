from transformers import pipeline

#  text-generation 
nlp = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Test model
user_input = "Hello, how can I improve my flexibility?"
response = nlp(user_input, max_length=100)

print(response[0]['generated_text'])

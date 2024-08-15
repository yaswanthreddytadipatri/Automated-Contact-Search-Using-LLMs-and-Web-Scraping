import ollama

# Load a model (example: llama2)
model_name = "llama3:8b"

# Define a prompt
prompt = "Hi"

# Generate a response from the model
response = ollama.generate(model=model_name, prompt=prompt)

# Print the generated response
print(response)

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-rw-1b")
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-rw-1b")

# Move to device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Prompt
prompt = (
    "Citizen AI: List and explain the fundamental rights of Indian citizens as per the Constitution of India.\n"
    "Answer:\n"
)

# Tokenize
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Generate (only valid arguments)
outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
    do_sample=False  # Greedy decoding
)

# Decode and print
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
response = decoded_output.split("Answer:")[-1].strip()

print("🤖 Citizen AI replies:\n")
print(response)

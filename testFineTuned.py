from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel

adapter_path = "./t5_fineTuned" 
base_model_name = "t5-small"

tokenizer = AutoTokenizer.from_pretrained(adapter_path)
base_model = AutoModelForSeq2SeqLM.from_pretrained(base_model_name)
base_model.resize_token_embeddings(len(tokenizer))
model = PeftModel.from_pretrained(base_model, adapter_path)

input_text = "Every cat is an animal"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=128)

result = tokenizer.decode(outputs[0], skip_special_tokens=False)
print("Result:", result)

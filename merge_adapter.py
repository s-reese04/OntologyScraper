from peft import PeftModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

BASE_MODEL_NAME = "t5-small"
ADAPTER_PATH = "./t5_fineTuned"
MERGED_OUTPUT_PATH = "./t5_fineTuned_merged"

tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH)

base_model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL_NAME)
base_model.resize_token_embeddings(len(tokenizer))

peft_model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)

merged_model = peft_model.merge_and_unload()

merged_model.save_pretrained(MERGED_OUTPUT_PATH)
tokenizer.save_pretrained(MERGED_OUTPUT_PATH)

print(f"Merged to {MERGED_OUTPUT_PATH}")

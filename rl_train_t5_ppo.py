import torch
from transformers import AutoTokenizer
from trl import (
    AutoModelForSeq2SeqLMWithValueHead,
    PPOConfig,
    PPOTrainer,
    create_reference_model,
)

#set GPU
device = "cuda" if torch.cuda.is_available() else "cpu"

#load model
MODEL_PATH = "./t5_fineTuned_merged"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSeq2SeqLMWithValueHead.from_pretrained(MODEL_PATH)
ref_model = create_reference_model(model)

#load dataset
with open("patterns/sentences.txt") as f:
    sentences = f.readlines()

query_tensors = [
    tokenizer(s, return_tensors="pt").input_ids[0] for s in sentences
]

#reward
def reward(text: str) -> float:
    return float(1)

#PPO setup
config = PPOConfig(
    batch_size=16,
    mini_batch_size=4,
    learning_rate=1e-5,
)

ppo_trainer = PPOTrainer(config, model, ref_model, tokenizer)

generation_kwargs = {
    "min_length": -1,
    "top_k": 0.0,
    "top_p": 1.0,
    "do_sample": True,
    "max_new_tokens": 32,
    "pad_token_id": tokenizer.pad_token_id,
}

#train loop
for epoch in range(3):
    response_tensors = ppo_trainer.generate(
        query_tensors, return_prompt=False, **generation_kwargs
    )

    responses = [tokenizer.decode(r, skip_special_tokens=True) for r in response_tensors]

    rewards = [torch.tensor(reward(text)) for text in responses]

    stats = ppo_trainer.step(query_tensors, response_tensors, rewards)
    mean_reward = sum(r.item() for r in rewards) / len(rewards)
    print(f"Epoch {epoch}: mean reward = {mean_reward:.3f}")

ppo_trainer.save_pretrained("./ppo-t5")

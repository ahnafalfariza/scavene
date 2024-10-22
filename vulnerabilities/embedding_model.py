import json
from sentence_transformers import SentenceTransformer, losses
from torch.utils.data import DataLoader
from datasets import Dataset

# Load the pre-trained model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load and prepare the dataset
with open("vulnerabilities/list_vulnerabilities.json", "r") as f:
    vulnerabilities = json.load(f)

# Prepare the training data
train_data = [
    {"text": f"{vuln['title']} {vuln['description']}"} for vuln in vulnerabilities
]

# Create a Hugging Face Dataset
dataset = Dataset.from_list(train_data)

# Define a data collator
def collate_fn(batch):
    return {
        'texts': [item['text'] for item in batch],
    }

# Create a DataLoader
train_dataloader = DataLoader(dataset, shuffle=True, batch_size=16, collate_fn=collate_fn)

print("Model and dataset loaded.")

# Use the MultipleNegativesRankingLoss
train_loss = losses.MultipleNegativesRankingLoss(model)

# Fine-tune the model
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=10,
    warmup_steps=100,
    show_progress_bar=True
)

# Save the fine-tuned model
model.save("fine_tuned_vulnerability_model")

print("Model fine-tuning completed and saved.")

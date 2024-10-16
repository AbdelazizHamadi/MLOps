from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BartTokenizer, BartForConditionalGeneration
import torch

class Config:
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu' # get GPU if possible 
    NUM_WORD_SPLIT = 10     # number of words before splitting the rest --> input_text, completion_text = comment_text
    MAX_TOKEN_LEN = 128
    BATCH_SIZE = 32
    EPOCHS = 5
    LEARNING_RATE = 5e-5    # allows gental update, good for finetuning 
    
config = Config()


# Load the fine-tuned model and tokenizer
model = BartForConditionalGeneration.from_pretrained('./finetuned-facebook-bart-base/checkpoint-635')
model = model.to(config.DEVICE)

# Load the pre-trained BART tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')

# Create Fast app 
app = FastAPI()

class TextInput(BaseModel):
    prompt: str
    max_length: int = 100  # Default max_length

@app.post("/generate/")
async def generate_text(text_input: TextInput):
    # Encode the input prompt
    inputs = tokenizer(text_input.prompt, return_tensors='pt', padding=True, truncation=True, max_length=config.MAX_TOKEN_LEN)

    # Generate text
    with torch.no_grad():
        generated_ids = model.generate(inputs['input_ids'].to(config.DEVICE), 
                                       attention_mask=inputs['attention_mask'].to(config.DEVICE), 
                                       max_length=text_input.max_length)


    # Decode the generated text
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    return {f"generated_text with ({config.DEVICE})": generated_text}

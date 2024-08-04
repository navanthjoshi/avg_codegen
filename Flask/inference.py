

from transformers import AutoModelForCausalLM, AutoTokenizer

from peft import PeftModel, PeftConfig
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

peft_model_id = "navanth360/codegen-test4000-2b-multi-lora-tagger"
config = PeftConfig.from_pretrained(peft_model_id)
model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path, return_dict=True, load_in_8bit=True, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)

model = PeftModel.from_pretrained(model, peft_model_id)


# model_name = "navanth360/codegen-test3-2b-multi-lora-tagger"  # Replace with your fine-tuned model name
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name).to(device)


def predict(input):
        # Tokenize the input text
        input_ids = tokenizer.encode(input, return_tensors="pt").to(device)
        
        # Generate the response
        sample_outputs = model.generate(input_ids, 
                                        max_length=128, 
                                        do_sample=True, 
                                        top_k=50, 
                                        top_p=0.95, 
                                        temperature=0.7,
                                        num_return_sequences=1)

        # Decode the generated text
        generated_text = tokenizer.decode(sample_outputs[0], skip_special_tokens=True)
        return generated_text

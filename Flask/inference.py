from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
import torch
from transformers import BitsAndBytesConfig

# Configuration for loading the model in 4-bit precision
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

# Specify the ID of your PEFT model
peft_model_id = "navanth360/codegen-test4000-2b-multi-lora-tagger"

# Load the PEFT configuration and base model with the quantization config
config = PeftConfig.from_pretrained(peft_model_id)
model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path, 
    return_dict=True, 
    quantization_config=bnb_config, 
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)

# Load the PEFT model
model = PeftModel.from_pretrained(model, peft_model_id)

# Define the device to use (GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def predict(input_text):
    # Tokenize the input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
    
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
    generated_text = generated_text.replace("\\n", "\n")
    print(generated_text)
# Print the formatted text
    return generated_text


# Example usage
# output = predict("//module adder:")
# print(output)



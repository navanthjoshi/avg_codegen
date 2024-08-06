from peft import PeftModel, PeftConfig
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

peft_model_id = "navanth360/codegen-test3-2b-multi-lora-tagger"
config = PeftConfig.from_pretrained(peft_model_id)
model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path, return_dict=True, load_in_8bit=True, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)

model = PeftModel.from_pretrained(model, peft_model_id)

batch = tokenizer("'### System Prompt: I want you to act as an IC designer, and implement the following in Verilog.### Instruction: Generate a Verilog module with the following description: FIFO module with simple read and write functionality### Output:module axi_protocol_converter_v2_1_b2s_simple_fifo", return_tensors='pt').to("cuda")

with torch.cuda.amp.autocast():
    output_tokens = model.generate(**batch, max_new_tokens=200)

print('\n\n', tokenizer.decode(output_tokens[0], skip_special_tokens=True))
import pandas as pd
import re

def extract_keywords(prompt):
    stop_words = {'give', 'me', 'a', 'with', 'the', 'to', 'is', 'as', 'an', 'in'}
    prompt = re.sub(r'[^\w\s]', '', prompt)
    words = prompt.lower().split()
    keywords = [word for word in words if word not in stop_words]
    return keywords

def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

def find_best_match(keywords, descriptions):
    best_match = None
    best_output = None
    highest_ratio = 0
    for description, output in descriptions:
        if not isinstance(description, str):
            description = str(description)
        description_keywords = description.lower().split()
        match_ratio = jaccard_similarity(keywords, description_keywords)
        if match_ratio > highest_ratio:
            highest_ratio = match_ratio
            best_match = description
            best_output = output
    return best_match, best_output, highest_ratio

def create_system_prompt(best_match, match_ratio):
    if match_ratio < 0.2:
        system_prompt = (
            "### System Prompt: I want you to act as an IC designer, and implement the following in Verilog.### "
            "Instruction: Generate a Verilog module with the following description: "
            f"Matching Module: {best_match}\n"
        )
    else:
        system_prompt = (
            "### System Prompt: I want you to act as an IC designer, and implement the following in Verilog.### "
            f"Instruction: Generate a Verilog module with the following description: {best_match}\n"
        )
    return system_prompt

def load_modules_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        module_names = df['module'].tolist()
        descriptions = df[['description', 'output']].values.tolist()
        return df, module_names, descriptions
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None, None, None

def generate_system_prompt(user_prompt, file_path='D:/MERN_FINAL/PS_verilog/Flask/train (1) xslx.xlsx'):
    df, module_names, descriptions = load_modules_from_excel(file_path)
    if df is None:
        return "Error loading modules from the Excel file."

    keywords = extract_keywords(user_prompt)
    best_match, best_output, highest_ratio = find_best_match(keywords, descriptions)

    if best_match:
        system_prompt = create_system_prompt(best_match, highest_ratio)
        return system_prompt, best_output
    else:
        system_prompt = (
            "### System Prompt: I want you to act as an IC designer, and implement the following in Verilog.### "
            "Instruction: Generate a Verilog module with the following description: "
        )
        return system_prompt + " " + user_prompt

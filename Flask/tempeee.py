# Original string with \n
input_text = """### System Prompt: I want you to act as an IC designer, and implement the following in Verilog.### Instruction: Generate a Verilog module with the following description: Instantiate Full Adder\n### Output:module  fulladder (\n\tinput  A_n,\n\tinput  B_n,\n\toutput Z_n,\n\n\tinput  C_n,\n\tinput  D_n,\n\tinput  E_n,\n\tinput  F_n,\n\toutput G_n\n);\n\tfulladder_b a0 (\n\t\t.A"""

# Replace \n with actual new lines
formatted_text = input_text.replace("\\n", "\n")

# Print the formatted text
print(formatted_text)
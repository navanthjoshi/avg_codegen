from flask import Flask, request, jsonify
from inference import predict
from upscaling import generate_system_prompt
from comparison import calculate_scores
import subprocess
import os

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    user_input = data.get('input', '')

    if user_input:
        try:
            # Generate system prompt and obtain prediction
            system_prompt, best_output = generate_system_prompt(user_input)
            prediction = predict(system_prompt)
            
            # Write the prediction to a temporary Verilog file
            temp_file = 'temp.v'
            print("Writing prediction to temporary Verilog file...")
            with open(temp_file, 'w') as f:
                f.write(prediction)
            
            # Compile the Verilog code using Icarus Verilog
            print("Compiling Verilog code with Icarus Verilog...")
            process = subprocess.run(['iverilog', temp_file], capture_output=True, text=True)
            
            print("Icarus Verilog stdout:", process.stdout)
            print("Icarus Verilog stderr:", process.stderr)
            
            # Collect the Verilog compilation result
            verilog_result = None
            if process.returncode != 0:
                verilog_result = {"error": process.stderr}
            else:
                verilog_result = {"stdout": process.stdout, "stderr": process.stderr}
            
            # Clean up temporary file
            os.remove(temp_file)
            
            # Calculate score (optional step based on your needs)
            score = calculate_scores(prediction, best_output)
            
            return jsonify({
                "generated_text": prediction,
                "verilog_result": verilog_result
            })
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "No input provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)

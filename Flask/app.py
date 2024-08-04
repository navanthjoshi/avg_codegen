# app.py
from flask import Flask, request, jsonify
from inference import predict 
from upscaling import generate_system_prompt
from comparison import calculate_scores
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    user_input = data.get('input', '')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    try:
        system_prompt, best_output = generate_system_prompt(user_input)
        output = best_output
        prediction = predict(system_prompt)
        score = calculate_scores(output, output)
        ### Send the inference code here!!!
        return jsonify({"generated_text": score})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)


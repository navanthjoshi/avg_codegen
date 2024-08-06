import React, { useState } from "react";
import axios from "axios";
import "./App.css";  // Ensure you import the CSS file

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/predict", { input });
      setResponse(res.data);
    } catch (error) {
      console.error("Error sending input to server:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Automatic Verilog Code Generation</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter the Prompt"
          />
          <button type="submit">Submit</button>
        </form>
        {response && (
          <div className="response-box">
            {response.generated_text && (
              <div className="prediction-box">
                <h2>Prediction:</h2>
                <pre>{response.generated_text}</pre>
              </div>
            )}
            {response.verilog_result && (
              <div className="verilog-result-box">
                <h2>Verilog Compilation Result:</h2>
                {response.verilog_result.error ? (
                  <pre className="error">Error: {response.verilog_result.error}</pre>
                ) : (
                  <>
                    <pre className="stdout">Output: {response.verilog_result.stdout}</pre>
                    <pre className="stderr">Messages: {response.verilog_result.stderr}</pre>
                  </>
                )}
              </div>
            )}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;

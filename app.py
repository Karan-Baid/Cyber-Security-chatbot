from flask import Flask, request, jsonify, send_from_directory
from flask import Flask, request, jsonify, render_template
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize the Ollama chain with updated import
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a cybersecurity expert assistant. Provide direct, concise answers to cybersecurity queries without greetings.The amswers should be based on Indian regualtions and technologies as you will have queries from Indians."),
    ("user", "Answer concisely: {question}")
])

# Updated Ollama import (make sure you have langchain-community installed)
llm = Ollama(model="llama2")
chain = prompt | llm | StrOutputParser()

@app.route('/')
def serve_index():
    return render_template('index.html') 

@app.route('/ask', methods=['POST'])
def handle_query():
    data = request.json
    try:
        response = chain.invoke({"question": data['question'], "max_tokens": 200})
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
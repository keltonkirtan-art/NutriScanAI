import os
from flask import Flask, render_template, request, jsonify
from google import genai # Nova biblioteca
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Configuração do novo Cliente Google GenAI
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-receita', methods=['POST'])
def gerar():
    try:
        dados = request.json
        ingredientes = dados.get('ingredientes')
        objetivo = dados.get('objetivo')
        restricoes = dados.get('restricoes')

        # Prompt com rigor científico (Biomedicina + Ed. Física)
        prompt = f"""
        Aja como um Nutricionista Clínico e Especialista em Fisiologia do Exercício.
        Crie uma solução nutricional para: {ingredientes}.
        Objetivo: {objetivo}. Restrições: {restricoes}.
        
        Requisitos técnicos da resposta:
        1. Analise a combinação de aminoácidos (Valor Biológico) para o objetivo de {objetivo}.
        2. Considere a Carga Glicêmica da refeição.
        3. Forneça a Tabela Nutricional Estimada detalhada (Kcal, P, C, G).
        4. Modo de preparo focado em preservar nutrientes.
        
        Retorne a resposta EXCLUSIVAMENTE em HTML formatado (use <h2> para títulos, 
        <div style='background-color: #ecfdf5; padding: 15px; border-radius: 10px; margin: 10px 0;'> para a tabela e <ul> para passos).
        """
        
        # Chamada usando o modelo que você já conhece e prefere
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents=prompt
        )
        
        return jsonify({"receita": response.text})
    except Exception as e:
        # Log do erro no terminal para facilitar seu diagnóstico
        print(f"Erro detalhado: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000) # Mudamos de 5000
import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
api_key = os.getenv("GEMINI_API_KEY")

# Ajuste para o Flask encontrar os templates fora da pasta api
app = Flask(__name__, 
            template_folder="../templates", 
            static_folder="../static")

# Configuração da API
# Dica: Use variáveis de ambiente para segurança
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

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

        prompt = f"""
        Aja como um nutricionista e chef. 
        Crie uma receita saudável usando: {ingredientes}.
        Objetivo do usuário: {objetivo}. 
        Restrições: {restricoes}.
        
        Retorne em HTML formatado:
        1. Nome da Receita (em <h2>)
        2. Tabela Nutricional Estimada (Kcal, P, C, G) em uma <div> destacada.
        3. Modo de preparo passo a passo.
        """
        
        response = model.generate_content(prompt)
        return jsonify({"receita": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Necessário para a Vercel reconhecer a aplicação
app.debug = True
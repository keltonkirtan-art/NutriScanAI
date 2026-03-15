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
        objetivo = dados.get('objetivo').upper()
        restricoes = dados.get('restricoes')

        prompt = f"""
        Aja como um Nutricionista com pós graduação em Nutrição esportiva e em tratamento e obesidade e Designer de UI.
        Crie uma receita saudável para: {ingredientes}. Objetivo: {objetivo}.
        
        RETORNE EXCLUSIVAMENTE O CONTEÚDO HTML USANDO ESTAS REGRAS:
        1. Título: Use <h2 class='text-2xl font-bold text-emerald-800 mb-4'>.
        2. Dashboard de Macros: Crie uma <div class='grid grid-cols-2 gap-3 mb-6'> com 4 cards internos.
           Cada card deve ter: <div class='bg-emerald-50 p-3 rounded-xl border border-emerald-100 text-center'>.
           Use ícones da FontAwesome: 🔥 (Kcal), 💪 (Prot), 🍞 (Carb), 🥑 (Gord).
        3. Análise Bio: Use uma <div class='bg-blue-50 p-4 rounded-xl border-l-4 border-blue-400 mb-6'> para a análise de biodisponibilidade e carga glicêmica.
        4. Preparo: Use <ul class='space-y-3'> com <li> contendo ícones de check.
        """
        
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents=prompt
        )
        
        return jsonify({"receita": response.text})
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"error": str(e)}), 500 # Retorna status 500 em caso de erro

if __name__ == "__main__":
    app.run(debug=True, port=5000) # Mudamos de 5000
    
    # nova rota que peça explicitamente à IA um planejamento de 7 dias e uma lista consolidada.
    
@app.route('/gerar-plano-semanal', methods=['POST'])
def gerar_semanal():
    try:
        dados = request.json
        ingredientes = dados.get('ingredientes')
        objetivo = dados.get('objetivo').upper()
        restricoes = dados.get('restricoes')

        prompt = f"""
        Aja como um Nutricionista Chefe altamente especializado em nutrição esportiva e tratamento da obesidade com especialização em gastronomia. Crie um PLANEJAMENTO SEMANAL (7 dias).
        Baseado em: {ingredientes}. Objetivo: {objetivo}. Restrições: {restricoes}.
        
        FORMATO DE SAÍDA (HTML):
        1. <h2 class='text-2xl font-bold text-emerald-800 mb-4'>📅 Plano Semanal Pro</h2>
        2. Crie uma tabela <table> ou grid de 7 cards para os dias da semana.
        3. <div class='bg-yellow-50 p-6 rounded-2xl border-2 border-yellow-200 my-6'>
           <h3 class='font-bold text-yellow-800 mb-2'>🛒 Lista de Compras Consolidada</h3>
           <p class='text-sm mb-3'>Considerando o que você já tem, compre apenas:</p>
           <ul class='grid grid-cols-2 gap-2'> (Liste os itens faltantes com checkboxes)
        4. Uma breve análise Bio e Nutri da estratégia da semana.
        """
        
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents=prompt
        )
        
        return jsonify({"plano": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
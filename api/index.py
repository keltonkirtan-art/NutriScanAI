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
        Aja como um Nutricionista e Especialista nutrição esportiva, tratamento da obesidade e em Logística Doméstica. 
        Crie um PLANEJAMENTO SEMANAL de 7 dias para: {ingredientes}. 
        Objetivo: {objetivo}.

        FORMATO DE SAÍDA (HTML):
        1. <h2 class='text-2xl font-bold text-emerald-800 mb-4'>📅 Cronograma Semanal NutriScan</h2>
        (Crie um resumo rápido de segunda a domingo)

        2. <div class='bg-gray-100 p-6 rounded-2xl border-2 border-gray-300 my-6 no-print'>
        <h3 class='font-bold text-gray-800 mb-4'><i class='fas fa-shopping-basket mr-2'></i>Lista de Compras Inteligente</h3>
        <p class='text-xs mb-4 text-gray-600'>Organizada para você ganhar tempo no mercado:</p>
        
        <div class='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <div>
                <h4 class='font-bold text-emerald-700 text-sm underline'>🥬 Hortifruti (Frutas e Verdes)</h4>
                <ul class='text-sm mb-3'> [Itens aqui com checkbox] </ul>
            </div>
            <div>
                <h4 class='font-bold text-red-700 text-sm underline'>🥩 Proteínas (Açougue/Peixaria)</h4>
                <ul class='text-sm mb-3'> [Itens aqui] </ul>
            </div>
            <div>
                <h4 class='font-bold text-blue-700 text-sm underline'>🧊 Laticínios e Congelados</h4>
                <ul class='text-sm mb-3'> [Itens aqui] </ul>
            </div>
            <div>
                <h4 class='font-bold text-amber-700 text-sm underline'>🌾 Despensa (Grãos e Temperos)</h4>
                <ul class='text-sm mb-3'> [Itens aqui] </ul>
            </div>
        </div>
        </div>
        """
        
       # response = client.models.generate_content(
           # model="gemini-3.1-flash-lite-preview", 
            # contents=prompt
      #  )
        
      #  return jsonify({"plano": response.text})
   # except Exception as e:
    #    return jsonify({"error": str(e)}), 500    
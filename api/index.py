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
        Aja como um Nutricionista Clínico Esportivo e especialista em tratamento da obesidade e manutenção da saúde além de ser um chef de cozinha renomado na área da gastronomia. Crie um PLANEJAMENTO SEMANAL (7 dias).
        O usuário listou as seguintes PREFERÊNCIAS ou base de ingredientes: {ingredientes}.
        Objetivo: {objetivo}. Restrições: {restricoes}.

        REGRAS CRÍTICAS: 
        - NÃO limite a dieta apenas aos itens listados! Adicione grande VARIEDADE de alimentos complementares (diferentes proteínas, carboidratos e vegetais) para evitar monotonia.
        - Inclua o Modo de Preparo prático para as refeições.

        FORMATO DE SAÍDA (HTML ESTRITO):
        1. <h2 class='text-2xl font-bold text-emerald-800 mb-4'>📅 Cronograma Semanal</h2>
        2. Para CADA DIA (Segunda a Domingo), crie um bloco contendo:
        - Nome da Refeição
        - Ingredientes
        - <b>Modo de Preparo:</b> (Instruções claras de como fazer)
        3. <div class='bg-gray-50 p-6 rounded-2xl border-2 border-gray-200 my-6 no-print'>
        <h3 class='font-bold text-emerald-900 mb-4'><i class='fas fa-shopping-cart mr-2'></i>Lista de Compras Interativa</h3>
        Organize por categorias (🥬 Hortifruti, 🥩 Açougue, 🌾 Despensa).
        Para cada item, dê uma opção (ex: "Batata Doce ou Mandioca").
        
        OBRIGATÓRIO: Use EXATAMENTE esta estrutura HTML para cada item da lista (para o JS funcionar):
        <li class='flex items-center mb-3'>
            <input type='checkbox' class='mr-3 w-5 h-5 cursor-pointer accent-emerald-600'>
            <span class='text-gray-700 font-medium'>Nome do Item (ou substituto)</span>
        </li>
        </div>
        """
        
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
             contents=prompt
        )
     
        return jsonify({"plano": response.text})
    
    except Exception as e:
       return jsonify({"error": str(e)}), 500    
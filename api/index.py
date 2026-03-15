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
        instrucao_tempo = "FOCO TOTAL EM PRATICIDADE: Refeições de no máximo 15 min, poucos utensílios." if tempo == 'rapido' else "Pode sugerir técnicas mais elaboradas, marinadas e preparos lentos para máximo sabor."

        prompt = f"""
        Aja como um Nutricionista Clínico (pós-graduado em Nutrição Esportiva, tratammento da obesidade, manutenção da saúde e Gastronomia) e Designer de UI.
        Crie uma solução nutricional inteligente e acessível para: {ingredientes}. Objetivo: {objetivo}. RESTRIÇÃO DE TEMPO: {instrucao_tempo}
        Restrições: {restricoes}.
        
        RETORNE EXCLUSIVAMENTE O CONTEÚDO HTML USANDO ESTAS REGRAS:
        1. Título: <h2 class='text-2xl font-bold text-emerald-800 mb-4'>.
        2. Dashboard de Macros: <div class='grid grid-cols-2 gap-3 mb-6'> com cards em <div class='bg-emerald-50 p-3 rounded-xl border border-emerald-100 text-center'>.
        3. Análise Bio: <div class='bg-blue-50 p-4 rounded-xl border-l-4 border-blue-400 mb-6'> (fale sobre biodisponibilidade).
        
        4. MODO DE PREPARO (Checklist Interativo):
           Para cada preparação, use EXATAMENTE esta estrutura:
           <div class='flex items-start mb-4 bg-white p-4 rounded-xl shadow-sm border border-gray-100'>
                <div class='mr-4 mt-1'>
                    <input type='checkbox' class='w-6 h-6 accent-emerald-600 cursor-pointer'>
                </div>
                <div>
                    <strong class='block text-emerald-800 text-xs uppercase tracking-widest mb-1'>Preparação: Nome do Alimento</strong>
                    <p class='text-gray-600 text-sm leading-relaxed'>Instrução clara. Sugira um substituto se aplicável (ex: 'ou Frango').</p>
                </div>
           </div>
        """
        # O motor da IA (Garanta que estas linhas existam após o prompt)
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
        tempo = dados.get('tempo')
        ingredientes = dados.get('ingredientes')
        objetivo = dados.get('objetivo').upper()
        restricoes = dados.get('restricoes')

        prompt = f"""
        Aja como um Nutricionista Clínico Esportivo (Especialista em Fisiologia e Gastronomia). 
        Crie um PLANEJAMENTO SEMANAL (7 dias) para: {ingredientes}.
        Objetivo: {objetivo}. ESTRATÉGIA DE TEMPO ({tempo.upper()}):
        { "Sugira receitas que usem a mesma base (ex: cozinhar frango para 2 dias) para otimizar o tempo." if tempo == 'rapido' else "Foque em variedade gourmet e técnicas gastronômicas diversas." }
        Restrições: {restricoes}.

        REGRAS DE CONTEÚDO:
        1. VARIEDADE: Não use apenas os itens listados. Adicione vegetais, diferentes fontes de fibras e gorduras boas.
        2. SUBSTITUTOS: Em cada proteína ou carbo, sugira uma opção (Ex: Frango ou Tofu).
        
        FORMATO DE SAÍDA (HTML ESTRITO):
        1. Título: <h2 class='text-2xl font-bold text-emerald-800 mb-6'>📅 Cronograma Semanal NutrIdeias IA</h2>

        2. PARA CADA DIA (Segunda a Domingo):
           - <div class='mb-8 p-4 bg-emerald-50 rounded-2xl border border-emerald-100'>
           - <h3 class='text-lg font-bold text-emerald-700 mb-3 border-b border-emerald-200 pb-1'>DIA: Nome do Dia</h3>
           - <strong>Refeição Sugerida:</strong> Nome do Prato.
           - <strong>Modo de Preparo (Checklist):</strong>
             Use esta estrutura para cada preparação:
             <div class='flex items-start mt-3 mb-3 bg-white p-3 rounded-xl shadow-sm border-l-4 border-emerald-500'>
                <div class='mr-3 mt-1'><input type='checkbox' class='w-6 h-6 accent-emerald-600'></div>
                <div>
                    <strong class='block text-xs uppercase text-emerald-800'>Preparação: Nome</strong>
                    <p class='text-gray-600 text-sm'>Instrução detalhada aqui.</p>
                </div>
             </div>
           - </div>

        3. LISTA DE COMPRAS (No final):
           <div class='bg-gray-100 p-6 rounded-2xl border-2 border-gray-300 my-6 no-print'>
           <h3 class='font-bold text-gray-800 mb-4'><i class='fas fa-shopping-basket mr-2'></i>Lista de Compras Pro</h3>
           Organize em Categorias (Hortifruti, Proteínas, etc). 
           Para cada item use: <li class='flex items-center mb-2'><input type='checkbox' class='mr-3 w-5 h-5'><span>Item</span></li>
           </div>
        """
            
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents=prompt
        )
     
        return jsonify({"plano": response.text})
    
    except Exception as e:
        print(f"Erro no Plano Semanal: {e}")
        return jsonify({"error": str(e)}), 500
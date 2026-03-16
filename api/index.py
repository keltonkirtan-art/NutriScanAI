import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Configuração do novo Cliente Google GenAI
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# ROTA 1: RECEITA ÚNICA (FREEMIUM)
# ==========================================
@app.route('/gerar-receita', methods=['POST'])
def gerar():
    try:
        dados = request.json
        ingredientes = dados.get('ingredientes')
        objetivo = dados.get('objetivo').lower()
        restricoes = dados.get('restricoes')
        tempo = dados.get('tempo')
        
        # Dados Biométricos
        sexo = dados.get('sexo', 'masculino')
        idade = int(dados.get('idade', 30))
        peso = float(dados.get('peso', 70))
        altura_cm = float(dados.get('altura', 170))
        altura_m = altura_cm / 100

        # Cálculo do IMC e TMB
        imc = round(peso / (altura_m ** 2), 1)
        if sexo == 'masculino':
            tmb = (10 * peso) + (6.25 * altura_cm) - (5 * idade) + 5
        else:
            tmb = (10 * peso) + (6.25 * altura_cm) - (5 * idade) - 161
        tmb = round(tmb)

        # 3. Lógica de Proteína Ajustada
        fator_prot = 2.0 # Padrão para hipertrofia
        if 'emagrecimento' in objetivo:
            fator_prot = 2.2
        elif 'manutencao' in objetivo:
            fator_prot = 1.6
        elif 'performance' in objetivo:
            fator_prot = 1.8 # Ajuste clínico para atletas de performance
            
        meta_proteina = round(peso * fator_prot)
        
        instrucao_tempo = "Refeição vapt-vupt de 15 até 30 min." if tempo == 'rapido' else "Pode sugerir preparos mais elaborados."

        prompt = f"""
        Aja como um Nutricionista Clínico (pós-graduado em Nutrição Esportiva e Gastronomia) e Designer de UI.
        Crie uma solução nutricional para: {ingredientes}. Restrições: {restricoes}.
        Tempo disponível: {instrucao_tempo}
        
        PERFIL DO PACIENTE:
        - Sexo: {sexo} | Idade: {idade} anos | Peso: {peso}kg | Altura: {altura_m}m
        - IMC: {imc} | Taxa Metabólica Basal (TMB): {tmb} kcal/dia
        - Objetivo: {objetivo} (Meta proteica diária estimada: {meta_proteina}g)
        
        RETORNE EXCLUSIVAMENTE O HTML USANDO ESTAS REGRAS:
        1. Título: <h2 class='text-2xl font-bold text-teal-800 mb-4'>
        
        2. ANÁLISE METABÓLICA DO PACIENTE:
           Crie uma <div class='mb-6 bg-slate-900 text-white p-4 rounded-xl border-l-4 border-teal-400 text-sm'>
           Faça uma brevíssima leitura do IMC ({imc}) e TMB ({tmb} kcal) deste usuário, explicando como esta receita se encaixa no objetivo dele de forma realista.
           </div>
           
        3. BARRA DE PROGRESSO DE PROTEÍNA:
           <div class='mb-6 bg-white p-4 rounded-xl border border-gray-100 shadow-sm'>
               <div class='flex justify-between text-sm font-bold text-gray-700 mb-2'>
                   <span>Meta Diária de Proteína ({meta_proteina}g)</span>
                   <span class='text-teal-600'>Xg atingidos nesta refeição</span>
               </div>
               <div class='w-full bg-gray-200 rounded-full h-3'>
                   <div class='bg-teal-500 h-3 rounded-full' style='width: [INSERIR_PORCENTAGEM]%'></div>
               </div>
               <p class='text-xs text-gray-500 mt-2'>Isso representa [INSERIR_PORCENTAGEM]% do seu alvo diário de proteína.</p>
           </div>

        4. Dashboard de Macros: <div class='grid grid-cols-2 gap-3 mb-6'> com cards em <div class='bg-teal-50 p-3 rounded-xl border border-teal-100 text-center'>.
        
        5. MODO DE PREPARO (Checklist Interativo):
           <div class='flex items-start mb-4 bg-white p-4 rounded-xl shadow-sm border border-gray-100'>
                <div class='mr-4 mt-1'><input type='checkbox' class='w-6 h-6 accent-teal-600 cursor-pointer'></div>
                <div>
                    <strong class='block text-teal-800 text-xs uppercase tracking-widest mb-1'>Passo: Nome do Alimento</strong>
                    <p class='text-gray-600 text-sm leading-relaxed'>Instrução clara sobre o preparo.</p>
                </div>
           </div>
        """
        
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents=prompt
        )
        return jsonify({"receita": response.text})
    except Exception as e:
        print(f"Erro na Receita: {e}")
        return jsonify({"error": str(e)}), 500


# ==========================================
# ROTA 2: PLANO SEMANAL (PRO)
# ==========================================
@app.route('/gerar-plano-semanal', methods=['POST'])
def gerar_semanal():
    try:
        dados = request.json
        tempo = dados.get('tempo')
        ingredientes = dados.get('ingredientes')
        objetivo = dados.get('objetivo').upper()
        restricoes = dados.get('restricoes')
        
        # Dados Biométricos (Adicionados para a IA do Plano Semanal ficar mais inteligente)
        sexo = dados.get('sexo', 'masculino')
        idade = int(dados.get('idade', 30))
        peso = float(dados.get('peso', 70))
        altura_cm = float(dados.get('altura', 170))
        altura_m = altura_cm / 100
        imc = round(peso / (altura_m ** 2), 1)

        prompt = f"""
        Aja como um Nutricionista Clínico Esportivo (Especialista em Fisiologia e Gastronomia). 
        Crie um PLANEJAMENTO SEMANAL (7 dias) para: {ingredientes}.
        
        PERFIL DO PACIENTE: Sexo: {sexo} | Idade: {idade} anos | Peso: {peso}kg | IMC: {imc}
        Objetivo Fisiológico: {objetivo}. 
        Restrições: {restricoes}.
        
        ESTRATÉGIA DE TEMPO ({tempo.upper()}):
        { "Sugira receitas que usem a mesma base (ex: cozinhar frango para 2 dias ou 'batch cooking') para otimizar o tempo na cozinha." if tempo == 'rapido' else "Foque em variedade gourmet e técnicas gastronômicas diversas." }

        REGRAS DE CONTEÚDO:
        1. VARIEDADE: Não use apenas os itens listados. Adicione vegetais, diferentes fontes de fibras e gorduras boas.
        2. SUBSTITUTOS: Em cada proteína ou carbo, sugira uma opção (Ex: Frango ou Tofu).
        
        FORMATO DE SAÍDA (HTML ESTRITO):
        1. Título: <h2 class='text-2xl font-bold text-teal-800 mb-6'>📅 Cronograma Semanal NutrIdeias IA</h2>

        2. PARA CADA DIA (Segunda a Domingo):
           - <div class='mb-8 p-4 bg-teal-50 rounded-2xl border border-teal-100'>
           - <h3 class='text-lg font-bold text-teal-700 mb-3 border-b border-teal-200 pb-1'>DIA: Nome do Dia</h3>
           - <strong>Refeição Sugerida:</strong> Nome do Prato.
           - <strong>Modo de Preparo (Checklist):</strong>
             Use esta estrutura para cada preparação:
             <div class='flex items-start mt-3 mb-3 bg-white p-3 rounded-xl shadow-sm border-l-4 border-teal-500'>
                <div class='mr-3 mt-1'><input type='checkbox' class='w-6 h-6 accent-teal-600'></div>
                <div>
                    <strong class='block text-xs uppercase text-teal-800'>Preparação: Nome</strong>
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

# ==========================================
# INICIALIZAÇÃO DO SERVIDOR (Sempre no final!)
# ==========================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
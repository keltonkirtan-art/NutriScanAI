# 🥗 NutrIdeias IA - Seu Nutricionista Inteligente

O **NutrIdeias IA** é uma aplicação web progressiva (PWA) alimentada por Inteligência Artificial (Google Gemini) que transforma os ingredientes que você tem em casa em receitas balanceadas e planos alimentares personalizados. Com foco em praticidade e saúde, o sistema analisa seu perfil biométrico para oferecer orientações nutricionais precisas.

## 🚀 Principais Funcionalidades

- **Gerador de Receitas Inteligente**: Informe o que tem na geladeira e receba receitas completas com modo de preparo e análise de macros.
- **Perfil Clínico (PRO)**: Cálculo automático de IMC (Índice de Massa Corporal) e TMB (Taxa Metabólica Basal) com base em sexo, idade, peso e altura.
- **Objetivos Personalizados**: Escolha entre emagrecimento, hipertrofia, manutenção ou performance esportiva para ajustar as metas de proteína e calorias.
- **Chef Pro (PRO)**: Modo de preparo detalhado com técnicas gastronômicas profissionais para quem quer cozinhar com excelência.
- **Plano Semanal (PRO)**: Planejamento completo de 7 dias com cardápio variado e lista de compras automatizada.
- **Exportação para PDF**: Salve suas receitas e planos nutricionais em PDF com um clique para levar para a cozinha ou imprimir.
- **Instalação PWA**: Funciona como um aplicativo nativo no celular, podendo ser adicionado à tela inicial.

## 🛠️ Tecnologias Utilizadas

- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python)
- **IA**: [Google Gemini 3.1 Flash](https://aistudio.google.com/) para geração de conteúdo dinâmico nutricional.
- **Frontend**: HTML5, [Tailwind CSS](https://tailwindcss.com/) e FontAwesome.
- **Autenticação e Banco de Dados**: [Supabase](https://supabase.com/).
- **Pagamentos**: Integração com [Mercado Pago](https://www.mercadopago.com.br/).
- **Hospedagem**: Otimizado para [Vercel](https://vercel.com/).
- **Testes**: Vitest e TestSprite.

## 📦 Como Instalar e Rodar Localmente

### Pré-requisitos
- Python 3.10+
- Chave de API do Google Gemini Studio.
- Conta no Supabase (para autenticação de usuários).

### Passo a Passo
1. Clone este repositório.
2. Acesse a pasta do projeto: `cd NutriScanAI`.
3. Crie um ambiente virtual: `python -m venv venv`.
4. Ative o ambiente virtual:
   - No Windows: `venv\Scripts\activate`
   - No Linux/macOS: `source venv/bin/activate`
5. Instale as dependências necessárias: `pip install -r requirements.txt`.
6. Configure as variáveis de ambiente no arquivo `.env`:
   ```env
   GEMINI_API_KEY=sua_chave_aqui
   ```
7. Inicie a aplicação: `python api/index.py` ou use o Vercel CLI com `vercel dev`.
8. No navegador, acesse: `http://127.0.0.1:5000`.

## 📂 Estrutura do Projeto

- `api/index.py`: Servidor Flask e integração principal com a API da Gemini.
- `templates/index.html`: Interface de usuário, lógica do frontend e comunicação com Supabase.
- `static/style.css`: Estilização PWA personalizada.
- `templates/sw.js` & `manifest.json`: Configurações de aplicação instalável (Service Worker e PWA).
- `tests/`: Suíte completa de testes para garantir a qualidade do sistema.

## 🛡️ Aviso Legal
O **NutrIdeias IA** é uma ferramenta de apoio tecnológico informativo. Ele **não substitui** o acompanhamento individual por médicos ou nutricionistas registrados. Consulte sempre um profissional de saúde qualificado antes de iniciar dietas ou protocolos de treinamento.

---
Desenvolvido com carinho por **MK2MIND**.

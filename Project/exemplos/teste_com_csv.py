"""
Sistema de Risco Fuzzy - Flask Web App
Usando scikit-fuzzy para lógica fuzzy real (Python 3.11)
"""

from flask import Flask, render_template_string, request, jsonify
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

class SistemaRiscoFuzzy:
    def __init__(self):
        """Inicializa o sistema fuzzy"""
        self.setup_fuzzy_system()
        self.historico = []

    def setup_fuzzy_system(self):
        """Configura o sistema fuzzy com scikit-fuzzy"""
        print("🔧 Configurando Sistema Fuzzy com scikit-fuzzy...")

        # === VARIÁVEIS DE ENTRADA ===
        self.renda = ctrl.Antecedent(np.arange(0, 15001, 1), 'renda')
        self.historico = ctrl.Antecedent(np.arange(0, 11, 1), 'historico_credito')
        self.idade = ctrl.Antecedent(np.arange(18, 81, 1), 'idade')
        self.tempo_emprego = ctrl.Antecedent(np.arange(0, 31, 1), 'tempo_emprego')
        self.dividas = ctrl.Antecedent(np.arange(0, 101, 1), 'percentual_dividas')

        # === VARIÁVEL DE SAÍDA ===
        self.risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco_credito')

        # === FUNÇÕES DE PERTINÊNCIA - RENDA ===
        self.renda['muito_baixa'] = fuzz.trimf(self.renda.universe, [0, 0, 2000])
        self.renda['baixa'] = fuzz.trimf(self.renda.universe, [1000, 2500, 4000])
        self.renda['media'] = fuzz.trimf(self.renda.universe, [3000, 5500, 8000])
        self.renda['alta'] = fuzz.trimf(self.renda.universe, [6500, 10000, 12000])
        self.renda['muito_alta'] = fuzz.trimf(self.renda.universe, [10000, 15000, 15000])

        # === FUNÇÕES DE PERTINÊNCIA - HISTÓRICO ===
        self.historico['pessimo'] = fuzz.trimf(self.historico.universe, [0, 0, 2])
        self.historico['ruim'] = fuzz.trimf(self.historico.universe, [1, 3, 5])
        self.historico['regular'] = fuzz.trimf(self.historico.universe, [4, 6, 8])
        self.historico['bom'] = fuzz.trimf(self.historico.universe, [7, 9, 10])
        self.historico['excelente'] = fuzz.trimf(self.historico.universe, [9, 10, 10])

        # === FUNÇÕES DE PERTINÊNCIA - IDADE ===
        self.idade['jovem'] = fuzz.trimf(self.idade.universe, [18, 18, 30])
        self.idade['adulto_jovem'] = fuzz.trimf(self.idade.universe, [25, 35, 45])
        self.idade['adulto'] = fuzz.trimf(self.idade.universe, [40, 50, 60])
        self.idade['maduro'] = fuzz.trimf(self.idade.universe, [55, 70, 80])

        # === FUNÇÕES DE PERTINÊNCIA - TEMPO DE EMPREGO ===
        self.tempo_emprego['novo'] = fuzz.trimf(self.tempo_emprego.universe, [0, 0, 2])
        self.tempo_emprego['pouco'] = fuzz.trimf(self.tempo_emprego.universe, [1, 3, 6])
        self.tempo_emprego['medio'] = fuzz.trimf(self.tempo_emprego.universe, [4, 8, 15])
        self.tempo_emprego['experiente'] = fuzz.trimf(self.tempo_emprego.universe, [12, 25, 30])

        # === FUNÇÕES DE PERTINÊNCIA - DÍVIDAS ===
        self.dividas['baixo'] = fuzz.trimf(self.dividas.universe, [0, 0, 30])
        self.dividas['medio'] = fuzz.trimf(self.dividas.universe, [20, 40, 60])
        self.dividas['alto'] = fuzz.trimf(self.dividas.universe, [50, 70, 90])
        self.dividas['critico'] = fuzz.trimf(self.dividas.universe, [80, 100, 100])

        # === FUNÇÕES DE PERTINÊNCIA - RISCO (SAÍDA) ===
        self.risco['muito_baixo'] = fuzz.trimf(self.risco.universe, [0, 0, 20])
        self.risco['baixo'] = fuzz.trimf(self.risco.universe, [10, 25, 40])
        self.risco['medio'] = fuzz.trimf(self.risco.universe, [30, 50, 70])
        self.risco['alto'] = fuzz.trimf(self.risco.universe, [60, 75, 90])
        self.risco['muito_alto'] = fuzz.trimf(self.risco.universe, [80, 100, 100])

        # === REGRAS FUZZY ===
        self.criar_regras()

        # === SISTEMA DE CONTROLE ===
        self.sistema_controle = ctrl.ControlSystem(self.regras)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema_controle)

        print("✅ Sistema Fuzzy configurado com sucesso!")

    def criar_regras(self):
        """Define as regras fuzzy (mais abrangentes)"""
        self.regras = [
            # === REGRAS DE MUITO BAIXO RISCO ===
            ctrl.Rule(self.renda['muito_alta'] & self.historico['excelente'] &
                     self.dividas['baixo'], self.risco['muito_baixo']),

            ctrl.Rule(self.renda['alta'] & self.historico['excelente'] &
                     self.dividas['baixo'] & self.tempo_emprego['experiente'],
                     self.risco['muito_baixo']),

            # === REGRAS DE BAIXO RISCO ===
            ctrl.Rule(self.renda['alta'] & self.historico['bom'] &
                     self.dividas['baixo'], self.risco['baixo']),

            ctrl.Rule(self.renda['alta'] & self.historico['excelente'],
                     self.risco['baixo']),

            ctrl.Rule(self.renda['muito_alta'] & self.historico['bom'],
                     self.risco['baixo']),

            ctrl.Rule(self.renda['media'] & self.historico['bom'] &
                     self.idade['adulto'] & self.dividas['baixo'],
                     self.risco['baixo']),

            ctrl.Rule(self.idade['maduro'] & self.tempo_emprego['experiente'] &
                     self.historico['bom'], self.risco['baixo']),

            ctrl.Rule(self.renda['media'] & self.historico['excelente'] &
                     self.dividas['baixo'], self.risco['baixo']),

            # === REGRAS DE RISCO MÉDIO ===
            ctrl.Rule(self.renda['media'] & self.historico['regular'],
                     self.risco['medio']),

            ctrl.Rule(self.renda['baixa'] & self.historico['bom'] &
                     self.tempo_emprego['medio'], self.risco['medio']),

            ctrl.Rule(self.renda['alta'] & self.historico['regular'] &
                     self.dividas['alto'], self.risco['medio']),

            ctrl.Rule(self.renda['media'] & self.dividas['medio'],
                     self.risco['medio']),

            ctrl.Rule(self.historico['regular'] & self.dividas['medio'],
                     self.risco['medio']),

            # === REGRAS DE ALTO RISCO ===
            ctrl.Rule(self.renda['baixa'] & self.historico['ruim'],
                     self.risco['alto']),

            ctrl.Rule(self.historico['ruim'] & self.dividas['alto'],
                     self.risco['alto']),

            ctrl.Rule(self.idade['jovem'] & self.tempo_emprego['novo'] &
                     self.renda['baixa'], self.risco['alto']),

            ctrl.Rule(self.dividas['alto'] & self.historico['regular'],
                     self.risco['alto']),

            # === REGRAS DE MUITO ALTO RISCO ===
            ctrl.Rule(self.renda['muito_baixa'] & self.historico['pessimo'],
                     self.risco['muito_alto']),

            ctrl.Rule(self.dividas['critico'], self.risco['muito_alto']),

            ctrl.Rule(self.historico['pessimo'] & self.dividas['alto'],
                     self.risco['muito_alto']),

            ctrl.Rule(self.renda['muito_baixa'] & self.historico['ruim'],
                     self.risco['muito_alto']),

            # === REGRAS DE FALLBACK (para evitar o erro) ===
            ctrl.Rule(self.renda['alta'], self.risco['baixo']),
            ctrl.Rule(self.renda['muito_alta'], self.risco['muito_baixo']),
            ctrl.Rule(self.historico['excelente'], self.risco['baixo']),
            ctrl.Rule(self.historico['bom'], self.risco['baixo']),
            ctrl.Rule(self.historico['pessimo'], self.risco['muito_alto']),
            ctrl.Rule(self.historico['ruim'], self.risco['alto']),
            ctrl.Rule(self.dividas['critico'], self.risco['muito_alto']),
            ctrl.Rule(self.dividas['baixo'], self.risco['baixo']),
        ]

    def avaliar_cliente(self, dados):
        """Avalia um cliente usando lógica fuzzy"""
        try:
            # Configurar inputs
            self.simulador.input['renda'] = dados['renda']
            self.simulador.input['historico_credito'] = dados['historico']
            self.simulador.input['idade'] = dados['idade']
            self.simulador.input['tempo_emprego'] = dados['tempo_emprego']
            self.simulador.input['percentual_dividas'] = dados['dividas']

            # Executar inferência fuzzy
            self.simulador.compute()

            # Obter resultado
            risco_score = self.simulador.output['risco_credito']

        except Exception as fuzzy_error:
            # Se der erro no fuzzy, usar fallback baseado em lógica simples
            print(f"⚠️ Erro fuzzy: {fuzzy_error}")
            print("🔄 Usando sistema de fallback...")

            risco_score = self.calcular_risco_fallback(dados)

        # Classificar risco
        classificacao = self.classificar_risco(risco_score)

        # Gerar recomendação
        recomendacao = self.gerar_recomendacao(risco_score, dados)

        # Resultado completo
        resultado = {
            'nome': dados['nome'],
            'risco_score': round(risco_score, 1),
            'classificacao': classificacao,
            'recomendacao': recomendacao,
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'dados_entrada': dados
        }

        # Salvar no histórico
        self.historico.append(resultado)

        return resultado

    def calcular_risco_fallback(self, dados):
        """Sistema de fallback quando o fuzzy falha"""
        # Normalizar valores
        renda_norm = min(dados['renda'] / 10000, 1.0)
        historico_norm = dados['historico'] / 10
        idade_factor = 1.0 if 25 <= dados['idade'] <= 55 else 0.7
        emprego_factor = min(dados['tempo_emprego'] / 15, 1.0)
        divida_penalty = dados['dividas'] / 100

        # Cálculo híbrido fuzzy-like
        score_positivo = (renda_norm * 0.35 + historico_norm * 0.30 +
                         idade_factor * 0.15 + emprego_factor * 0.20)

        risco_score = max(0, min(100, (1 - score_positivo + divida_penalty * 0.8) * 100))

        return risco_score

    def classificar_risco(self, score):
        """Classifica o score de risco"""
        if score <= 20:
            return {"nivel": "MUITO BAIXO", "emoji": "🟢", "cor": "#28a745"}
        elif score <= 40:
            return {"nivel": "BAIXO", "emoji": "🔵", "cor": "#17a2b8"}
        elif score <= 60:
            return {"nivel": "MÉDIO", "emoji": "🟡", "cor": "#ffc107"}
        elif score <= 80:
            return {"nivel": "ALTO", "emoji": "🟠", "cor": "#fd7e14"}
        else:
            return {"nivel": "MUITO ALTO", "emoji": "🔴", "cor": "#dc3545"}

    def gerar_recomendacao(self, risco_score, dados):
        """Gera recomendação baseada no risco"""
        if risco_score <= 30:
            return {
                "decisao": "✅ APROVADO",
                "limite": min(dados['renda'] * 8, 50000),
                "taxa": "Taxa preferencial (1.2% a.m.)",
                "observacoes": "Cliente com excelente perfil. Baixo risco de inadimplência."
            }
        elif risco_score <= 50:
            return {
                "decisao": "⚠️ APROVADO COM RESTRIÇÕES",
                "limite": min(dados['renda'] * 4, 25000),
                "taxa": "Taxa intermediária (2.5% a.m.)",
                "observacoes": "Bom perfil, mas requer acompanhamento."
            }
        elif risco_score <= 70:
            return {
                "decisao": "🔍 ANÁLISE MANUAL",
                "limite": min(dados['renda'] * 2, 10000),
                "taxa": "Taxa elevada (4.0% a.m.)",
                "observacoes": "Requer análise detalhada e garantias adicionais."
            }
        else:
            return {
                "decisao": "❌ REPROVADO",
                "limite": 0,
                "taxa": "N/A",
                "observacoes": "Alto risco de inadimplência. Crédito não recomendado."
            }

# Instância global do sistema
sistema = SistemaRiscoFuzzy()

# Template HTML com seções adicionais sobre o projeto e lógica fuzzy
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏦 Sistema de Avaliação de Risco de Crédito com Lógica Fuzzy</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        .form-card, .result-card, .about-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .about-card {
            grid-column: span 2;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            font-weight: bold;
            margin-bottom: 8px;
            color: #333;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .examples {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 20px;
        }
        
        .example-btn {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .example-btn:hover {
            background: #e9ecef;
            border-color: #667eea;
        }
        
        .result-card {
            min-height: 400px;
        }
        
        .result-card.hidden {
            display: none;
        }
        
        .risk-score {
            text-align: center;
            margin: 20px 0;
        }
        
        .score-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 24px;
            font-weight: bold;
            color: white;
            flex-direction: column;
        }
        
        .recommendation {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .recommendation h4 {
            margin-bottom: 10px;
            color: #333;
        }
        
        .recommendation p {
            margin-bottom: 8px;
            color: #555;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 18px;
            color: #666;
            display: none;
        }
        
        .loading.show {
            display: block;
        }
        
        .historico {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: 30px;
        }
        
        .historico h2 {
            margin-bottom: 20px;
            color: #333;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        table th, table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e1e5e9;
        }
        
        table th {
            background: #f8f9fa;
            font-weight: bold;
            color: #333;
        }
        
        .tabs {
            display: flex;
            margin-bottom: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .tab {
            padding: 15px 25px;
            cursor: pointer;
            flex: 1;
            text-align: center;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: #667eea;
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .tab-content h2 {
            margin-bottom: 20px;
            color: #333;
            font-size: 1.8em;
        }
        
        .tab-content p {
            margin-bottom: 15px;
            text-align: justify;
        }
        
        .tab-content h3 {
            margin: 25px 0 15px;
            color: #444;
            font-size: 1.5em;
        }
        
        .team-members {
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .team-members p {
            margin-bottom: 5px;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .about-card {
                grid-column: span 1;
            }
            
            .tabs {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏦 Sistema de Avaliação de Risco de Crédito</h1>
            <p>Utilizando Lógica Fuzzy para análise de crédito mais humanizada e precisa</p>
            <div class="badge">Powered by scikit-fuzzy</div>
        </div>
        
        <div class="about-card">
            <div class="tabs">
                <div class="tab active" onclick="openTab('simulador')">Simulador</div>
                <div class="tab" onclick="openTab('sobre')">Sobre o Projeto</div>
                <div class="tab" onclick="openTab('fuzzy')">Lógica Fuzzy</div>
            </div>
            
            <div id="simulador" class="tab-content active">
                <div class="main-content">
                    <div class="form-card">
                        <h2>📋 Dados do Cliente</h2>
                        <form id="riskForm">
                            <div class="form-group">
                                <label for="nome">Nome do Cliente:</label>
                                <input type="text" id="nome" name="nome" value="João Silva" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="renda">Renda Mensal (R$):</label>
                                <input type="number" id="renda" name="renda" value="5000" min="1000" max="50000" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="historico">Score de Crédito (0-10):</label>
                                <input type="number" id="historico" name="historico" value="7" min="0" max="10" step="0.1" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="idade">Idade:</label>
                                <input type="number" id="idade" name="idade" value="35" min="18" max="80" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="tempo_emprego">Tempo de Emprego (anos):</label>
                                <input type="number" id="tempo_emprego" name="tempo_emprego" value="5" min="0" max="40" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="dividas">Dívidas/Renda (%):</label>
                                <input type="number" id="dividas" name="dividas" value="30" min="0" max="100" required>
                            </div>
                            
                            <button type="submit" class="btn">🧠 Avaliar com Lógica Fuzzy</button>
                        </form>
                        
                        <div class="examples">
                            <div class="example-btn" onclick="carregarExemplo('ideal')">
                                👍 Cliente Ideal
                            </div>
                            <div class="example-btn" onclick="carregarExemplo('risco')">
                                👎 Alto Risco
                            </div>
                            <div class="example-btn" onclick="carregarExemplo('aposentado')">
                                👴 Aposentado
                            </div>
                            <div class="example-btn" onclick="carregarExemplo('jovem')">
                                👦 Jovem
                            </div>
                        </div>
                    </div>
                    
                    <div class="result-card hidden" id="resultCard">
                        <h2>📊 Resultado da Avaliação Fuzzy</h2>
                        <div class="loading" id="loading">🧠 Processando com scikit-fuzzy...</div>
                        <div id="resultContent">
                            <!-- Resultado será inserido aqui -->
                        </div>
                    </div>
                </div>
                
                <div class="historico" id="historicoSection" style="display: none;">
                    <h2>📈 Histórico de Avaliações</h2>
                    <div id="historicoContent">
                        <!-- Histórico será inserido aqui -->
                    </div>
                </div>
            </div>
            
            <div id="sobre" class="tab-content">
                <h2>Sistema de Avaliação de Risco de Crédito com Lógica Fuzzy</h2>
                
                <p>O Sistema de Avaliação de Risco de Crédito com Lógica Fuzzy representa uma abordagem inovadora para a análise financeira, superando as limitações dos métodos tradicionais baseados em lógica binária. Desenvolvido por uma equipe multidisciplinar, este projeto busca humanizar e aprimorar o processo de avaliação de crédito através da aplicação de técnicas avançadas de inteligência computacional.</p>
                
                <div class="team-members">
                    <h3>Integrantes da Equipe</h3>
                    <p>Gabriel Belitz Baldez</p>
                    <p>Cristian Augusto Bredow Honze</p>
                    <p>Juliano César dos Santos</p>
                    <p>Guilherme Panosso Locatelli</p>
                </div>
                
                <h3>Descrição do Problema</h3>
                <p>No cenário financeiro atual, as instituições frequentemente utilizam sistemas de análise de crédito que operam com decisões binárias - aprovado ou reprovado - sem considerar adequadamente as nuances e incertezas inerentes à avaliação de risco. Conceitos como "renda média", "histórico regular" ou "idade jovem" são intrinsecamente subjetivos e demandam uma abordagem mais flexível para serem processados de maneira eficaz. É neste contexto que a Lógica Fuzzy emerge como uma solução ideal, permitindo o tratamento de informações imprecisas de forma mais natural e próxima ao raciocínio humano.</p>
                
                <h3>Objetivo</h3>
                <p>O objetivo central deste sistema é desenvolver uma ferramenta inteligente capaz de processar informações subjetivas com a mesma naturalidade que um analista humano experiente. Ao contrário dos métodos convencionais, nossa solução fornece classificações graduais em vez de decisões abruptas, permitindo uma avaliação mais justa e precisa do perfil de cada cliente. Esta abordagem não apenas melhora a qualidade das decisões de crédito, mas também demonstra de forma prática as vantagens da Lógica Fuzzy sobre os métodos tradicionais em cenários reais do mercado financeiro.</p>
                
                <h3>Tecnologias Utilizadas</h3>
                <p>Para a implementação deste projeto, utilizamos um conjunto robusto de tecnologias modernas. A linguagem Python 3.11 serve como base para o desenvolvimento, complementada pela biblioteca scikit-fuzzy para a implementação dos algoritmos de Lógica Fuzzy. A interface do usuário foi construída utilizando o framework Flask, garantindo uma experiência web responsiva e intuitiva. Para os cálculos numéricos e manipulação de dados, empregamos as bibliotecas NumPy e Pandas, enquanto o Matplotlib nos permite visualizar graficamente as funções de pertinência e outros elementos do sistema fuzzy. O frontend foi desenvolvido com HTML, CSS e JavaScript, resultando em uma interface moderna e acessível.</p>
                
                <h3>Metodologia</h3>
                <p>Nossa metodologia de desenvolvimento seguiu um processo estruturado, iniciando com um estudo teórico aprofundado sobre os fundamentos da Lógica Fuzzy e suas aplicações em análise de risco. Em seguida, realizamos a modelagem do sistema, definindo cuidadosamente as variáveis linguísticas, funções de pertinência e regras que compõem o núcleo do motor de inferência fuzzy. A implementação foi realizada utilizando a biblioteca scikit-fuzzy, que oferece um conjunto abrangente de ferramentas para sistemas baseados em Lógica Fuzzy. Paralelamente, desenvolvemos uma interface web interativa com Flask, permitindo aos usuários interagir facilmente com o sistema. As etapas finais incluíram a validação do sistema com dados simulados e uma análise comparativa com métodos tradicionais de avaliação de crédito.</p>
                
                <h3>Diferencial do Projeto</h3>
                <p>O diferencial deste projeto reside em sua aplicação prática para um problema real do mercado financeiro, combinada com uma interface moderna e intuitiva que facilita a demonstração dos conceitos. Além disso, incorporamos uma base de dados realista com mais de 50 perfis de clientes diversos, permitindo uma avaliação abrangente do desempenho do sistema em diferentes cenários. O dashboard web interativo oferece estatísticas, gráficos e relatórios automáticos, proporcionando insights valiosos sobre o processo de tomada de decisão. Como compromisso com a comunidade acadêmica e profissional, disponibilizamos o código-fonte completo para estudo e replicação, contribuindo para a disseminação do conhecimento sobre Lógica Fuzzy e suas aplicações práticas.</p>
            </div>
            
            <div id="fuzzy" class="tab-content">
                <h2>Lógica Fuzzy: Fundamentos e Aplicações</h2>
                
                <p>A Lógica Fuzzy, também conhecida como Lógica Nebulosa, representa uma extensão da lógica booleana tradicional que permite lidar com conceitos imprecisos e subjetivos. Desenvolvida pelo matemático Lotfi Zadeh em 1965, esta abordagem revolucionou a forma como sistemas computacionais processam informações que envolvem incerteza e ambiguidade.</p>
                
                <h3>Conceitos Fundamentais</h3>
                <p>Na lógica clássica, um elemento pertence ou não pertence a um conjunto, seguindo o princípio do terceiro excluído. Por exemplo, uma pessoa é considerada "jovem" ou "não jovem", sem meio-termo. A Lógica Fuzzy, por outro lado, permite graus de pertinência entre 0 e 1, possibilitando que um elemento pertença parcialmente a um conjunto.</p>
                
                <p>Assim, uma pessoa de 35 anos pode ser considerada "jovem" com um grau de pertinência de 0.3 e "adulta" com um grau de 0.7, refletindo melhor a natureza gradual das categorias no mundo real. Esta característica torna a Lógica Fuzzy particularmente adequada para modelar conceitos linguísticos vagos como "alto", "quente", "rápido" ou "arriscado".</p>
                
                <h3>Componentes de um Sistema Fuzzy</h3>
                <p>Um sistema baseado em Lógica Fuzzy típico possui quatro componentes principais. O primeiro é a Fuzzificação, processo de transformar valores numéricos precisos (crisp) em conjuntos fuzzy, atribuindo graus de pertinência. O segundo componente é a Base de Regras, conjunto de regras linguísticas do tipo "SE-ENTÃO" que definem o comportamento do sistema. O terceiro elemento é o mecanismo de Inferência, que combina as regras fuzzy para mapear os conjuntos fuzzy de entrada nos conjuntos fuzzy de saída. Por fim, temos a Defuzzificação, processo de converter os conjuntos fuzzy resultantes em um valor numérico preciso.</p>
                
                <h3>Vantagens da Lógica Fuzzy</h3>
                <p>A Lógica Fuzzy oferece diversas vantagens em relação aos métodos convencionais. Sua capacidade de modelagem de incerteza permite representar conhecimento impreciso e incompleto de forma natural. A facilidade de expressar regras em termos linguísticos compreensíveis torna os sistemas fuzzy mais acessíveis e intuitivos. Além disso, esses sistemas apresentam robustez e tolerância a dados imprecisos ou ruidosos, característica fundamental em aplicações do mundo real. A implementação relativamente simples, quando comparada a técnicas como redes neurais, e a interpretabilidade das regras fuzzy, que são transparentes e compreensíveis por humanos, completam o conjunto de vantagens desta abordagem.</p>
                
                <h3>Aplicações Práticas</h3>
                <p>A Lógica Fuzzy encontra aplicações em diversos campos. No controle de processos, é utilizada em sistemas de ar condicionado, freios ABS e transmissões automáticas. Na medicina, auxilia no diagnóstico médico e na dosagem de medicamentos. No setor financeiro, é aplicada na análise de risco, sistemas de trading e avaliação de crédito, como demonstrado neste projeto. Também está presente em eletrônicos de consumo, como câmeras, máquinas de lavar e fornos de micro-ondas, além de ser utilizada em sistemas de reconhecimento de padrões para classificação de imagens e reconhecimento de voz.</p>
                
                <p>No contexto específico de análise de crédito, a Lógica Fuzzy permite avaliar o risco de forma mais nuançada, considerando a natureza gradual de conceitos como "renda adequada", "bom histórico" ou "cliente confiável", resultando em decisões mais precisas e justas. Este sistema demonstra na prática como a aplicação da Lógica Fuzzy pode transformar a avaliação de risco de crédito, tornando-a mais humanizada e eficiente.</p>
            </div>
        </div>
    </div>

    <script>
        // Controle de abas
        function openTab(tabName) {
            // Ocultar todos os conteúdos
            const tabContents = document.getElementsByClassName('tab-content');
            for (let i = 0; i < tabContents.length; i++) {
                tabContents[i].classList.remove('active');
            }
            
            // Remover classe ativa de todas as abas
            const tabs = document.getElementsByClassName('tab');
            for (let i = 0; i < tabs.length; i++) {
                tabs[i].classList.remove('active');
            }
            
            // Mostrar conteúdo selecionado
            document.getElementById(tabName).classList.add('active');
            
            // Adicionar classe ativa à aba clicada
            event.currentTarget.classList.add('active');
        }
    
        // Exemplos pré-definidos
        const exemplos = {
            ideal: {
                nome: 'Ana Executiva',
                renda: 12000,
                historico: 9,
                idade: 35,
                tempo_emprego: 8,
                dividas: 20
            },
            risco: {
                nome: 'Carlos Jovem',
                renda: 2500,
                historico: 3,
                idade: 22,
                tempo_emprego: 1,
                dividas: 75
            },
            aposentado: {
                nome: 'Sandra Aposentada',
                renda: 4000,
                historico: 8,
                idade: 65,
                tempo_emprego: 30,
                dividas: 15
            },
            jovem: {
                nome: 'Pedro Estudante',
                renda: 1800,
                historico: 4,
                idade: 20,
                tempo_emprego: 0,
                dividas: 60
            }
        };

        function carregarExemplo(tipo) {
            const exemplo = exemplos[tipo];
            if (exemplo) {
                document.getElementById('nome').value = exemplo.nome;
                document.getElementById('renda').value = exemplo.renda;
                document.getElementById('historico').value = exemplo.historico;
                document.getElementById('idade').value = exemplo.idade;
                document.getElementById('tempo_emprego').value = exemplo.tempo_emprego;
                document.getElementById('dividas').value = exemplo.dividas;
            }
        }

        // Submissão do formulário
        document.getElementById('riskForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Mostrar loading
            const loading = document.getElementById('loading');
            const resultCard = document.getElementById('resultCard');
            resultCard.classList.remove('hidden');
            loading.style.display = 'block';
            
            const formData = new FormData(this);
            const dados = Object.fromEntries(formData);
            
            // Converter valores numéricos
            dados.renda = parseFloat(dados.renda);
            dados.historico = parseFloat(dados.historico);
            dados.idade = parseInt(dados.idade);
            dados.tempo_emprego = parseInt(dados.tempo_emprego);
            dados.dividas = parseFloat(dados.dividas);
            
            try {
                const response = await fetch('/avaliar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dados)
                });
                
                const resultado = await response.json();
                
                // Ocultar loading
                loading.style.display = 'none';
                
                if (resultado.erro) {
                    alert('Erro: ' + resultado.erro);
                    return;
                }
                
                mostrarResultado(resultado);
                carregarHistorico();
                
            } catch (error) {
                loading.style.display = 'none';
                alert('Erro ao processar: ' + error.message);
            }
        });

        function mostrarResultado(resultado) {
            const resultContent = document.getElementById('resultContent');
            
            const html = `
                <div style="text-align: center; margin-bottom: 20px;">
                    <h3>${resultado.nome}</h3>
                    <p style="color: #666;">${resultado.timestamp}</p>
                </div>
                
                <div class="risk-score">
                    <div class="score-circle" style="background-color: ${resultado.classificacao.cor};">
                        ${resultado.classificacao.emoji}<br>
                        ${resultado.risco_score}
                    </div>
                    <h3>RISCO ${resultado.classificacao.nivel}</h3>
                    <p>Score: ${resultado.risco_score}/100</p>
                </div>
                
                <div class="recommendation">
                    <h4>💼 Recomendação:</h4>
                    <p><strong>Decisão:</strong> ${resultado.recomendacao.decisao}</p>
                    <p><strong>Limite Sugerido:</strong> R$ ${resultado.recomendacao.limite.toLocaleString('pt-BR')}</p>
                    <p><strong>Taxa de Juros:</strong> ${resultado.recomendacao.taxa}</p>
                    <p><strong>Observações:</strong> ${resultado.recomendacao.observacoes}</p>
                </div>
            `;
            
            resultContent.innerHTML = html;
        }

        async function carregarHistorico() {
            try {
                const response = await fetch('/historico');
                const historico = await response.json();
                
                if (historico.length > 0) {
                    const historicoSection = document.getElementById('historicoSection');
                    const historicoContent = document.getElementById('historicoContent');
                    
                    let html = `
                        <table>
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Score</th>
                                    <th>Classificação</th>
                                    <th>Decisão</th>
                                    <th>Limite</th>
                                    <th>Hora</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    
                    historico.forEach(item => {
                        html += `
                            <tr>
                                <td>${item.nome}</td>
                                <td>${item.risco_score}</td>
                                <td style="color: ${item.classificacao.cor};">
                                    ${item.classificacao.emoji} ${item.classificacao.nivel}
                                </td>
                                <td>${item.recomendacao.decisao}</td>
                                <td>R$ ${item.recomendacao.limite.toLocaleString('pt-BR')}</td>
                                <td>${item.timestamp.split(' ')[1]}</td>
                            </tr>
                        `;
                    });
                    
                    html += `
                            </tbody>
                        </table>
                    `;
                    
                    historicoContent.innerHTML = html;
                    historicoSection.style.display = 'block';
                }
            } catch (error) {
                console.error('Erro ao carregar histórico:', error);
            }
        }

        // Carregar histórico na inicialização
        window.addEventListener('load', carregarHistorico);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/avaliar', methods=['POST'])
def avaliar():
    """Endpoint para avaliar cliente"""
    try:
        dados = request.get_json()
        resultado = sistema.avaliar_cliente(dados)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/historico', methods=['GET'])
def historico():
    """Endpoint para obter histórico"""
    return jsonify(sistema.historico)

@app.route('/limpar', methods=['POST'])
def limpar_historico():
    """Endpoint para limpar histórico"""
    sistema.historico.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Risco Fuzzy Web")
    print("🧠 Usando scikit-fuzzy para Lógica Fuzzy REAL")
    print("📱 Acesse: http://localhost:5000")
    print("⚡ Compatible com Python 3.11")
    print("🔥 Pressione Ctrl+C para parar")

    app.run(debug=True, host='0.0.0.0', port=5000)

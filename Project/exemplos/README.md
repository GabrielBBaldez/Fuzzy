📁 Pasta Exemplos - Sistema de Risco Fuzzy
Esta pasta contém scripts de teste e dados de exemplo para validar e demonstrar o funcionamento do Sistema de Avaliação de Risco de Crédito usando Lógica Fuzzy.

📋 Arquivos Incluídos
🐍 teste_clientes.py
Script principal de testes com exemplos pré-definidos

Funcionalidades:

✅ 10 perfis de clientes pré-configurados (do excelente ao péssimo)
✅ Teste de sensibilidade (varia um parâmetro por vez)
✅ Casos extremos para validação
✅ Relatórios detalhados com estatísticas
✅ Exportação para CSV
✅ Interface de menu interativa
Como usar:

bash
cd exemplos/
python teste_clientes.py
📊 dados_exemplo.csv
Base de dados com 50 clientes fictícios

Colunas disponíveis:

nome: Nome do cliente
renda: Renda mensal (R$ 800 - R$ 25.000)
historico_credito: Score de 0-10
idade: 20-68 anos
tempo_emprego: 0-35 anos
percentual_dividas: 12-90% da renda
perfil_esperado: Classificação manual esperada
setor: Área de atuação profissional
estado_civil: Estado civil
dependentes: Número de dependentes
🔬 teste_com_csv.py
Script avançado para processar dados do CSV

Funcionalidades:

✅ Carregamento e validação de dados CSV
✅ Processamento em lote de todos os clientes
✅ Análises estatísticas completas
✅ Visualizações gráficas (histogramas, scatter plots, correlações)
✅ Análise por setor profissional
✅ Comparação com expectativas manuais
✅ Exportação de resultados
Como usar:

bash
cd exemplos/
python teste_com_csv.py
🚀 Exemplos de Execução
1. Teste Rápido com Perfis Pré-definidos
bash
python teste_clientes.py
# Escolha opção 1: Executar teste completo
2. Análise Completa com CSV
bash
python teste_com_csv.py
# Seguir o menu: 1 → 2 → 3 → 4 → 5
3. Teste de Sensibilidade
bash
python teste_clientes.py
# Escolha opção 2: Teste de sensibilidade
📊 Resultados Esperados
Perfis de Exemplo:
Ana Executiva (Renda: R$ 12k, Histórico: 9/10) → Risco Baixo
Carlos Jovem (Renda: R$ 2.8k, Histórico: 4/10) → Risco Alto
Sandra Aposentada (Renda: R$ 4k, Histórico: 8/10) → Risco Baixo
Análises Geradas:
📈 Distribuição de scores por faixa de risco
🏢 Análise por setor profissional
💰 Correlação renda vs risco
👥 Perfil demográfico dos clientes
🎯 Precisão do sistema vs expectativas
🛠️ Personalização
Adicionar Novos Clientes no CSV:
csv
nome,renda,historico_credito,idade,tempo_emprego,percentual_dividas,perfil_esperado,setor,estado_civil,dependentes
Novo Cliente,8000,7,32,6,25,Bom,Tecnologia,Casado,1
Modificar Perfis de Teste:
Edite a função carregar_clientes_exemplo() em teste_clientes.py:

python
{
    'nome': 'Seu Cliente',
    'renda': 5000,
    'historico_credito': 6,
    'idade': 30,
    'tempo_emprego': 5,
    'percentual_dividas': 35,
    'perfil': 'Regular'
}
📈 Interpretação dos Resultados
Scores de Risco:
0-20: Muito Baixo (Cliente ideal)
21-40: Baixo (Bom pagador)
41-60: Médio (Acompanhar)
61-80: Alto (Cautela)
81-100: Muito Alto (Evitar)
Fatores Mais Influentes:
Histórico de Crédito (40% do peso)
Renda Mensal (30% do peso)
Percentual de Dívidas (20% do peso)
Tempo de Emprego (10% do peso)
🔧 Dependências Necessárias
bash
pip install pandas numpy matplotlib seaborn
🎯 Para a Apresentação
Demonstrações Recomendadas:
Mostrar a diferença entre cliente ideal vs alto risco
Executar teste de sensibilidade ao vivo
Carregar dados do CSV e processar em lote
Mostrar gráficos gerados automaticamente
Comparar resultados com expectativas manuais
Pontos de Destaque:
✨ Sistema processa 50 clientes em segundos
✨ Visualizações automáticas para análise
✨ Comparação estatística com classificação manual
✨ Interface amigável para testes
✨ Dados realistas de diferentes setores
🐛 Solução de Problemas
Erro: "Arquivo não encontrado"
bash
# Certifique-se de estar na pasta exemplos/
cd exemplos/
ls -la  # Verificar se os arquivos estão presentes
Erro: "ModuleNotFoundError"
bash
pip install pandas matplotlib seaborn numpy
Gráficos não aparecem:
bash
# Linux: instalar tkinter
sudo apt-get install python3-tk

# macOS: usar backend diferente
import matplotlib
matplotlib.use('Agg')
📞 Próximos Passos
Execute os testes para entender o comportamento
Analise os gráficos gerados
Compare com suas expectativas
Ajuste os parâmetros se necessário
Prepare demonstrações para a apresentação
💡 Dica: Use esses scripts para validar seu sistema e gerar conteúdo impressionante para a apresentação!


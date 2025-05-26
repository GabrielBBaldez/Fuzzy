# Sistema de Avaliação de Risco de Crédito com Lógica Fuzzy

## Integrantes da Equipe
- Gabriel Belitz Baldez
- Cristian Augusto Bredow Honze
- Juliano César dos Santos
- Guilherme Panosso Locatelli

## Descrição do Problema

Instituições financeiras tradicionalmente utilizam sistemas de análise de crédito baseados em lógica binária (aprovado/reprovado), que não conseguem capturar adequadamente as nuances e incertezas inerentes à avaliação de risco financeiro. Variáveis como "renda média", "histórico regular" ou "idade jovem" são conceitos subjetivos que requerem uma abordagem mais flexível e humanizada para análise precisa.

## Objetivo

Desenvolver um sistema inteligente de avaliação de risco de crédito utilizando técnicas de Lógica Fuzzy, capaz de:
- Processar informações imprecisas e subjetivas de forma mais natural
- Simular o raciocínio humano na tomada de decisões financeiras
- Fornecer classificações graduais ao invés de decisões binárias abruptas
- Demonstrar as vantagens da Lógica Fuzzy sobre métodos tradicionais em cenários reais
- Visualizar graficamente o processo de fuzzificação e as funções de pertinência

## Tecnologias Utilizadas

- **Python 3.11**: Linguagem principal de desenvolvimento
- **scikit-fuzzy**: Biblioteca para implementação de Lógica Fuzzy
- **Flask**: Framework web para interface do usuário
- **NumPy**: Computação numérica e arrays
- **Matplotlib**: Visualização das funções de pertinência
- **Base64**: Codificação de imagens para exibição na web
- **HTML/CSS/JavaScript**: Interface web responsiva e moderna

## Funcionalidades Implementadas

### 1. Motor de Inferência Fuzzy
- Cinco variáveis de entrada: renda, histórico de crédito, idade, tempo de emprego e percentual de dívidas
- Uma variável de saída: risco de crédito
- Funções de pertinência triangulares para todas as variáveis
- Conjunto abrangente de regras fuzzy para avaliação de risco
- Sistema de fallback para garantir robustez em casos extremos

### 2. Interface Web Interativa
- Dashboard moderno e responsivo
- Sistema de abas para navegação intuitiva
- Formulário para entrada de dados do cliente
- Exemplos pré-definidos para demonstração rápida
- Visualização clara dos resultados da avaliação
- Histórico de avaliações realizadas

### 3. Visualização Gráfica das Funções de Pertinência
- Gráficos estáticos de todas as funções de pertinência
- Visualização separada para variáveis de entrada e saída
- Gráficos dinâmicos que destacam os valores atuais do cliente
- Integração visual do processo de fuzzificação
- Representação clara dos conjuntos fuzzy e seus limites

### 4. Avaliação de Risco Detalhada
- Score numérico de risco (0-100)
- Classificação em cinco níveis: Muito Baixo, Baixo, Médio, Alto, Muito Alto
- Recomendações personalizadas baseadas no perfil do cliente
- Cálculo automático de limite de crédito sugerido
- Indicação de taxa de juros apropriada

## Estrutura do Projeto

```
├── SistemaRiscoFuzzy_com_graficos.py   # Arquivo principal da aplicação Flask
├── generate_fuzzy_plots.py             # Módulo para geração de gráficos das funções de pertinência
└── README.md                           # Documentação do projeto
```

## Instalação e Execução

### Pré-requisitos
- Python 3.11 ou superior
- Pip (gerenciador de pacotes Python)

### Instalação das Dependências
```bash
pip install scikit-fuzzy scipy networkx matplotlib flask numpy
```

### Execução do Sistema
```bash
python SistemaRiscoFuzzy_com_graficos.py
```

Após a execução, acesse o sistema através do navegador em: http://localhost:5000

## Guia de Uso

### 1. Simulador de Avaliação de Risco
- Preencha os dados do cliente no formulário
- Utilize os exemplos pré-definidos para testar diferentes perfis
- Clique em "Avaliar com Lógica Fuzzy" para processar a avaliação
- Visualize o resultado com score, classificação e recomendações

### 2. Visualização das Funções de Pertinência
- Acesse a aba "Funções de Pertinência" para visualizar os gráficos estáticos
- Navegue entre as abas "Variáveis de Entrada" e "Variável de Saída"
- Após realizar uma avaliação, visualize os gráficos dinâmicos que mostram os valores do cliente

### 3. Informações sobre o Projeto e Lógica Fuzzy
- Acesse as abas "Sobre o Projeto" e "Lógica Fuzzy" para informações didáticas
- Entenda os conceitos fundamentais da Lógica Fuzzy e sua aplicação na avaliação de risco

## Diferenciais do Sistema

- **Visualização Didática**: Gráficos interativos que tornam o processo de fuzzificação transparente
- **Aplicação Prática**: Solução real para problema do mercado financeiro
- **Interface Moderna**: Dashboard web interativo e responsivo
- **Robustez**: Sistema de fallback para garantir funcionamento mesmo em casos extremos
- **Modularidade**: Código organizado e reutilizável
- **Experiência Completa**: Desde a entrada de dados até a visualização dos resultados

## Contribuições Futuras

- Implementação de explicações detalhadas sobre quais regras foram ativadas
- Comparação visual entre método tradicional e fuzzy
- Ajuste interativo de parâmetros das funções de pertinência
- Visualização de tendências no histórico de avaliações
- Exportação de relatórios em PDF

## Licença

Este projeto é disponibilizado como código aberto para fins educacionais e de estudo.

---

Desenvolvido como projeto acadêmico para demonstração prática dos conceitos de Lógica Fuzzy aplicados a problemas reais do mercado financeiro.

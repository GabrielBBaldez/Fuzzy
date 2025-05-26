"""
Gerador de gráficos para funções de pertinência fuzzy
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import base64
from io import BytesIO

# Configurar matplotlib para usar português
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams.update({'font.size': 12})

def generate_membership_plots(sistema_fuzzy):
    """Gera gráficos para todas as funções de pertinência do sistema fuzzy"""
    
    plots = {}
    
    # Gerar gráficos para cada variável de entrada
    plots['renda'] = plot_variable(
        sistema_fuzzy.renda, 
        'Funções de Pertinência - Renda Mensal (R$)',
        'Renda (R$)',
        'Grau de Pertinência'
    )
    
    plots['historico'] = plot_variable(
        sistema_fuzzy.historico, 
        'Funções de Pertinência - Score de Crédito',
        'Score (0-10)',
        'Grau de Pertinência'
    )
    
    plots['idade'] = plot_variable(
        sistema_fuzzy.idade, 
        'Funções de Pertinência - Idade',
        'Idade (anos)',
        'Grau de Pertinência'
    )
    
    plots['tempo_emprego'] = plot_variable(
        sistema_fuzzy.tempo_emprego, 
        'Funções de Pertinência - Tempo de Emprego',
        'Tempo (anos)',
        'Grau de Pertinência'
    )
    
    plots['dividas'] = plot_variable(
        sistema_fuzzy.dividas, 
        'Funções de Pertinência - Percentual de Dívidas',
        'Dívidas/Renda (%)',
        'Grau de Pertinência'
    )
    
    plots['risco'] = plot_variable(
        sistema_fuzzy.risco, 
        'Funções de Pertinência - Risco de Crédito',
        'Risco (0-100)',
        'Grau de Pertinência'
    )
    
    return plots

def plot_variable(variable, title, xlabel, ylabel):
    """Gera um gráfico para uma variável fuzzy específica"""
    
    # Criar figura
    plt.figure(figsize=(10, 6))
    
    # Verificar se a variável é do tipo correto (com atributo terms)
    if hasattr(variable, 'terms'):
        # Plotar cada função de pertinência
        for term_name, term_mf in variable.terms.items():
            plt.plot(variable.universe, term_mf.mf, label=term_name)
    else:
        print(f"Erro: Variável {title} não possui atributo 'terms'")
        # Criar um gráfico vazio para não quebrar o fluxo
        plt.text(0.5, 0.5, "Gráfico não disponível", 
                 horizontalalignment='center', verticalalignment='center',
                 transform=plt.gca().transAxes, fontsize=14)
    
    # Configurar o gráfico
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(0, 1.1)
    plt.grid(True)
    plt.legend(loc='center right')
    
    # Salvar o gráfico em um buffer de memória
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    
    # Converter para base64 para uso em HTML
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    return f"data:image/png;base64,{img_base64}"

def plot_with_current_value(variable, value, title, xlabel, ylabel):
    """Gera um gráfico para uma variável fuzzy com o valor atual destacado"""
    
    # Criar figura
    plt.figure(figsize=(10, 6))
    
    # Verificar se a variável é do tipo correto (com atributo terms)
    if hasattr(variable, 'terms'):
        # Plotar cada função de pertinência
        for term_name, term_mf in variable.terms.items():
            plt.plot(variable.universe, term_mf.mf, label=term_name)
        
        # Destacar o valor atual
        plt.axvline(x=value, color='red', linestyle='--', label=f'Valor atual: {value}')
    else:
        print(f"Erro: Variável {title} não possui atributo 'terms'")
        # Criar um gráfico vazio para não quebrar o fluxo
        plt.text(0.5, 0.5, "Gráfico não disponível", 
                 horizontalalignment='center', verticalalignment='center',
                 transform=plt.gca().transAxes, fontsize=14)
    
    # Configurar o gráfico
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(0, 1.1)
    plt.grid(True)
    plt.legend(loc='center right')
    
    # Salvar o gráfico em um buffer de memória
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    
    # Converter para base64 para uso em HTML
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    return f"data:image/png;base64,{img_base64}"

def generate_dynamic_plots(sistema_fuzzy, dados_cliente):
    """Gera gráficos com os valores atuais do cliente destacados"""
    
    plots = {}
    
    # Gerar gráficos para cada variável de entrada com o valor atual
    plots['renda'] = plot_with_current_value(
        sistema_fuzzy.renda,
        dados_cliente['renda'],
        'Funções de Pertinência - Renda Mensal (R$)',
        'Renda (R$)',
        'Grau de Pertinência'
    )
    
    plots['historico'] = plot_with_current_value(
        sistema_fuzzy.historico,
        dados_cliente['historico'],
        'Funções de Pertinência - Score de Crédito',
        'Score (0-10)',
        'Grau de Pertinência'
    )
    
    plots['idade'] = plot_with_current_value(
        sistema_fuzzy.idade,
        dados_cliente['idade'],
        'Funções de Pertinência - Idade',
        'Idade (anos)',
        'Grau de Pertinência'
    )
    
    plots['tempo_emprego'] = plot_with_current_value(
        sistema_fuzzy.tempo_emprego,
        dados_cliente['tempo_emprego'],
        'Funções de Pertinência - Tempo de Emprego',
        'Tempo (anos)',
        'Grau de Pertinência'
    )
    
    plots['dividas'] = plot_with_current_value(
        sistema_fuzzy.dividas,
        dados_cliente['dividas'],
        'Funções de Pertinência - Percentual de Dívidas',
        'Dívidas/Renda (%)',
        'Grau de Pertinência'
    )
    
    return plots

if __name__ == "__main__":
    # Teste
    print("Este módulo deve ser importado pelo sistema principal.")

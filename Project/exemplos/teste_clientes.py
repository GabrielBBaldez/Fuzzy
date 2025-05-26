"""
Scripts de Teste - Sistema de Avaliação de Risco Fuzzy
Exemplos práticos para testar o sistema com diferentes perfis de clientes
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Adicionar o diretório pai ao path para importar o sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Importar o sistema (descomente quando tiver o arquivo principal)
# from sistema_risco_fuzzy import SistemaRiscoFuzzy

class TestadorSistemaFuzzy:
    """Classe para realizar testes sistemáticos do sistema fuzzy"""

    def __init__(self):
        # Para demonstração, vamos simular o sistema
        self.sistema = self.criar_sistema_demo()
        self.resultados_teste = []

    def criar_sistema_demo(self):
        """Cria uma versão demo do sistema para testes"""

        class SistemaDemo:
            def avaliar_cliente(self, dados):
                # Simulação simplificada da lógica fuzzy
                renda_score = min(dados['renda'] / 10000, 1.0) * 30
                historico_score = (dados['historico_credito'] / 10) * 40
                idade_score = 15 if 25 <= dados['idade'] <= 55 else 5
                emprego_score = min(dados['tempo_emprego'] / 10, 1.0) * 10
                divida_penalty = (dados['percentual_dividas'] / 100) * 50

                risco_score = max(0, min(100, 100 - (
                            renda_score + historico_score + idade_score + emprego_score) + divida_penalty))

                return {
                    'nome': dados.get('nome', 'Cliente'),
                    'risco_score': round(risco_score, 1),
                    'dados_entrada': dados,
                    'timestamp': datetime.now()
                }

        return SistemaDemo()

    def carregar_clientes_exemplo(self):
        """Carrega clientes de exemplo para teste"""
        return [
            {
                'nome': 'Ana Executiva',
                'renda': 12000,
                'historico_credito': 9,
                'idade': 35,
                'tempo_emprego': 8,
                'percentual_dividas': 20,
                'perfil': 'Excelente'
            },
            {
                'nome': 'João Empresário',
                'renda': 15000,
                'historico_credito': 8,
                'idade': 45,
                'tempo_emprego': 15,
                'percentual_dividas': 30,
                'perfil': 'Muito Bom'
            },
            {
                'nome': 'Maria Professora',
                'renda': 5500,
                'historico_credito': 7,
                'idade': 40,
                'tempo_emprego': 12,
                'percentual_dividas': 25,
                'perfil': 'Bom'
            },
            {
                'nome': 'Pedro Vendedor',
                'renda': 3500,
                'historico_credito': 6,
                'idade': 30,
                'tempo_emprego': 5,
                'percentual_dividas': 40,
                'perfil': 'Regular'
            },
            {
                'nome': 'Carlos Jovem',
                'renda': 2800,
                'historico_credito': 4,
                'idade': 24,
                'tempo_emprego': 2,
                'percentual_dividas': 60,
                'perfil': 'Risco Médio'
            },
            {
                'nome': 'Julia Estudante',
                'renda': 1500,
                'historico_credito': 3,
                'idade': 22,
                'tempo_emprego': 1,
                'percentual_dividas': 70,
                'perfil': 'Alto Risco'
            },
            {
                'nome': 'Roberto Desempregado',
                'renda': 1200,
                'historico_credito': 2,
                'idade': 35,
                'tempo_emprego': 0,
                'percentual_dividas': 90,
                'perfil': 'Muito Alto Risco'
            },
            {
                'nome': 'Sandra Aposentada',
                'renda': 4000,
                'historico_credito': 8,
                'idade': 65,
                'tempo_emprego': 30,
                'percentual_dividas': 15,
                'perfil': 'Perfil Especial'
            },
            {
                'nome': 'Lucas Freelancer',
                'renda': 6000,
                'historico_credito': 5,
                'idade': 28,
                'tempo_emprego': 3,
                'percentual_dividas': 50,
                'perfil': 'Renda Variável'
            },
            {
                'nome': 'Fernanda Médica',
                'renda': 18000,
                'historico_credito': 9,
                'idade': 32,
                'tempo_emprego': 6,
                'percentual_dividas': 35,
                'perfil': 'Alta Renda'
            }
        ]

    def executar_teste_completo(self):
        """Executa bateria completa de testes"""
        print("🚀 INICIANDO TESTES DO SISTEMA FUZZY")
        print("=" * 60)

        clientes = self.carregar_clientes_exemplo()

        print(f"📋 Testando {len(clientes)} perfis de clientes...\n")

        for i, cliente in enumerate(clientes, 1):
            print(f"[{i:2d}] Avaliando: {cliente['nome']}")

            # Avaliar cliente
            resultado = self.sistema.avaliar_cliente(cliente)

            # Armazenar resultado
            resultado['perfil_esperado'] = cliente['perfil']
            self.resultados_teste.append(resultado)

            # Exibir resultado resumido
            print(f"     Risco: {resultado['risco_score']:5.1f} | Perfil: {cliente['perfil']}")

        print("\n" + "=" * 60)
        self.gerar_relatorio_testes()

    def gerar_relatorio_testes(self):
        """Gera relatório detalhado dos testes"""
        print("📊 RELATÓRIO DE TESTES")
        print("=" * 60)

        # Estatísticas gerais
        scores = [r['risco_score'] for r in self.resultados_teste]
        print(f"📈 ESTATÍSTICAS GERAIS:")
        print(f"   • Total de testes: {len(scores)}")
        print(f"   • Score médio: {np.mean(scores):.1f}")
        print(f"   • Score mínimo: {np.min(scores):.1f}")
        print(f"   • Score máximo: {np.max(scores):.1f}")
        print(f"   • Desvio padrão: {np.std(scores):.1f}")

        # Distribuição por faixas de risco
        print(f"\n🎯 DISTRIBUIÇÃO POR RISCO:")
        muito_baixo = len([s for s in scores if s <= 20])
        baixo = len([s for s in scores if 20 < s <= 40])
        medio = len([s for s in scores if 40 < s <= 60])
        alto = len([s for s in scores if 60 < s <= 80])
        muito_alto = len([s for s in scores if s > 80])

        print(f"   • Muito Baixo (≤20): {muito_baixo} clientes")
        print(f"   • Baixo (21-40): {baixo} clientes")
        print(f"   • Médio (41-60): {medio} clientes")
        print(f"   • Alto (61-80): {alto} clientes")
        print(f"   • Muito Alto (>80): {muito_alto} clientes")

        # Detalhamento por cliente
        print(f"\n📋 DETALHAMENTO POR CLIENTE:")
        print("-" * 60)

        for resultado in sorted(self.resultados_teste, key=lambda x: x['risco_score']):
            dados = resultado['dados_entrada']
            print(f"{resultado['nome']:20} | Risco: {resultado['risco_score']:5.1f} | "
                  f"Renda: R${dados['renda']:6,.0f} | "
                  f"Hist: {dados['historico_credito']}/10 | "
                  f"Idade: {dados['idade']:2d} | "
                  f"Dív: {dados['percentual_dividas']:2.0f}%")

    def teste_sensibilidade(self):
        """Testa a sensibilidade do sistema a mudanças nos parâmetros"""
        print("\n🔬 TESTE DE SENSIBILIDADE")
        print("=" * 60)

        cliente_base = {
            'nome': 'Cliente Teste',
            'renda': 5000,
            'historico_credito': 6,
            'idade': 30,
            'tempo_emprego': 5,
            'percentual_dividas': 40
        }

        print("Cliente Base:")
        resultado_base = self.sistema.avaliar_cliente(cliente_base)
        print(f"Score base: {resultado_base['risco_score']}")

        # Testar variação da renda
        print(f"\n📊 Impacto da RENDA:")
        for renda in [2000, 3500, 5000, 7500, 10000, 15000]:
            cliente_test = cliente_base.copy()
            cliente_test['renda'] = renda
            resultado = self.sistema.avaliar_cliente(cliente_test)
            variacao = resultado['risco_score'] - resultado_base['risco_score']
            print(f"   Renda R${renda:6,.0f}: Score {resultado['risco_score']:5.1f} ({variacao:+5.1f})")

        # Testar variação do histórico
        print(f"\n📊 Impacto do HISTÓRICO:")
        for hist in range(1, 11):
            cliente_test = cliente_base.copy()
            cliente_test['historico_credito'] = hist
            resultado = self.sistema.avaliar_cliente(cliente_test)
            variacao = resultado['risco_score'] - resultado_base['risco_score']
            print(f"   Histórico {hist:2d}/10: Score {resultado['risco_score']:5.1f} ({variacao:+5.1f})")

        # Testar variação das dívidas
        print(f"\n📊 Impacto das DÍVIDAS:")
        for divida in [10, 25, 40, 60, 80, 95]:
            cliente_test = cliente_base.copy()
            cliente_test['percentual_dividas'] = divida
            resultado = self.sistema.avaliar_cliente(cliente_test)
            variacao = resultado['risco_score'] - resultado_base['risco_score']
            print(f"   Dívidas {divida:2d}%: Score {resultado['risco_score']:5.1f} ({variacao:+5.1f})")

    def gerar_casos_extremos(self):
        """Gera e testa casos extremos para validar o sistema"""
        print("\n⚡ TESTE DE CASOS EXTREMOS")
        print("=" * 60)

        casos_extremos = [
            {
                'nome': 'Cliente Perfeito',
                'renda': 15000,
                'historico_credito': 10,
                'idade': 40,
                'tempo_emprego': 20,
                'percentual_dividas': 5,
                'esperado': 'Risco muito baixo'
            },
            {
                'nome': 'Cliente Péssimo',
                'renda': 1000,
                'historico_credito': 0,
                'idade': 20,
                'tempo_emprego': 0,
                'percentual_dividas': 100,
                'esperado': 'Risco muito alto'
            },
            {
                'nome': 'Jovem Rico Inexperiente',
                'renda': 20000,
                'historico_credito': 2,
                'idade': 22,
                'tempo_emprego': 1,
                'percentual_dividas': 80,
                'esperado': 'Conflito: alta renda vs inexperiência'
            },
            {
                'nome': 'Veterano Pobre Confiável',
                'renda': 2000,
                'historico_credito': 9,
                'idade': 55,
                'tempo_emprego': 25,
                'percentual_dividas': 20,
                'esperado': 'Conflito: baixa renda vs confiabilidade'
            }
        ]

        for caso in casos_extremos:
            resultado = self.sistema.avaliar_cliente(caso)
            print(f"\n{caso['nome']}:")
            print(f"   Score: {resultado['risco_score']}")
            print(f"   Esperado: {caso['esperado']}")

    def salvar_resultados_csv(self, filename='resultados_teste.csv'):
        """Salva os resultados dos testes em CSV"""
        if not self.resultados_teste:
            print("⚠️ Nenhum teste executado ainda!")
            return

        # Preparar dados para CSV
        dados_csv = []
        for resultado in self.resultados_teste:
            dados = resultado['dados_entrada']
            linha = {
                'nome': resultado['nome'],
                'risco_score': resultado['risco_score'],
                'renda': dados['renda'],
                'historico_credito': dados['historico_credito'],
                'idade': dados['idade'],
                'tempo_emprego': dados['tempo_emprego'],
                'percentual_dividas': dados['percentual_dividas'],
                'perfil_esperado': resultado.get('perfil_esperado', ''),
                'timestamp': resultado['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            }
            dados_csv.append(linha)

        # Salvar CSV
        df = pd.DataFrame(dados_csv)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Resultados salvos em: {filename}")


def main():
    """Função principal para executar todos os testes"""
    print("🧪 SISTEMA DE TESTES - AVALIAÇÃO DE RISCO FUZZY")
    print("=" * 70)

    # Criar testador
    testador = TestadorSistemaFuzzy()

    # Menu de opções
    while True:
        print("\n📋 OPÇÕES DE TESTE:")
        print("1. 🚀 Executar teste completo")
        print("2. 🔬 Teste de sensibilidade")
        print("3. ⚡ Casos extremos")
        print("4. 💾 Salvar resultados CSV")
        print("5. 📊 Relatório resumido")
        print("0. ❌ Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            testador.executar_teste_completo()
        elif opcao == '2':
            testador.teste_sensibilidade()
        elif opcao == '3':
            testador.gerar_casos_extremos()
        elif opcao == '4':
            filename = input("Nome do arquivo (Enter=resultados_teste.csv): ").strip()
            if not filename:
                filename = 'resultados_teste.csv'
            testador.salvar_resultados_csv(filename)
        elif opcao == '5':
            if testador.resultados_teste:
                testador.gerar_relatorio_testes()
            else:
                print("⚠️ Execute os testes primeiro!")
        elif opcao == '0':
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    main()
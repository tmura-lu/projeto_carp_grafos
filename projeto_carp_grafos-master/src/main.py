import os
import sys
import time
import signal
import gc
from contextlib import contextmanager
from multiprocessing import Pool, cpu_count
from utils_grafo import ler_arquivo_dat
from solucao_writer import salvar_solucao
from greedy_constructor import greedy_constructor
import csv

def carregar_clocks_melhor_sol(caminho_csv):
    clocks_dict = {}
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader:
            nome = row['Nome'].strip().lower()
            try:
                clocks_melhor_sol = int(row['clocks_melhor_sol'])
            except (KeyError, ValueError):
                clocks_melhor_sol = 0
            clocks_dict[nome] = clocks_melhor_sol
    return clocks_dict

def processar_arquivo(args):
    nome_arq, caminho_instancia, pasta_saida = args
    script_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.abspath(os.path.join(script_dir, '..', 'padroes', 'reference_values.csv'))
    clocks_melhor_sol_dict = carregar_clocks_melhor_sol(caminho_csv)
    try:
        print(f"\nProcessando {nome_arq}")
        grafo, capacidade = ler_arquivo_dat(caminho_instancia)
        print(f"Arquivo lido: {len(grafo.vertices)} vértices, {len(grafo.arestas)} arestas, {len(grafo.arcos)} arcos")
        inicio_clock = time.perf_counter()
        rotas = greedy_constructor(grafo, capacidade)
        clocks = int((time.perf_counter() - inicio_clock) * 1000)
        if not rotas:
            return False, nome_arq, "Nenhuma rota criada"
        nome_saida = f"sol-{os.path.splitext(nome_arq)[0]}.dat"
        caminho_saida = os.path.join(pasta_saida, nome_saida)
        nome_base = os.path.splitext(nome_arq)[0].strip().lower()
        clocks_melhor_sol = clocks_melhor_sol_dict.get(nome_base, 0)
        if clocks_melhor_sol == 0:
            print(f"AVISO: clocks_melhor_sol não encontrado para '{nome_base}'")
        salvar_solucao(rotas, grafo, capacidade, caminho_saida, clocks=clocks, clocks_melhor_sol=clocks_melhor_sol)
        del grafo
        del rotas
        gc.collect()
        return True, nome_arq, None
    except Exception as e:
        return False, nome_arq, f"Erro: {str(e)}"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_instancias = os.path.abspath(os.path.join(script_dir, '..', 'selected_instances'))
    pasta_saida = os.path.abspath(os.path.join(script_dir, 'solucoes'))
    os.makedirs(pasta_saida, exist_ok=True)
    arquivos = []
    for nome_arq in os.listdir(pasta_instancias):
        if nome_arq.endswith('.dat'):
            caminho = os.path.join(pasta_instancias, nome_arq)
            tamanho = os.path.getsize(caminho)
            arquivos.append((nome_arq, caminho, tamanho))
    arquivos.sort(key=lambda x: x[2])
    args = [(arq[0], arq[1], pasta_saida) for arq in arquivos]
    total_arquivos = len(args)
    num_cores = max(1, cpu_count() - 1)
    print(f"\nIniciando processamento de {total_arquivos} arquivos usando {num_cores} cores")
    print("Arquivos ordenados por tamanho (processando menores primeiro)")
    inicio = time.time()
    arquivos_processados = 0
    arquivos_com_erro = 0
    with Pool(processes=num_cores) as pool:
        try:
            for i, (sucesso, nome_arq, erro) in enumerate(pool.imap_unordered(processar_arquivo, args), 1):
                if sucesso:
                    arquivos_processados += 1
                    print(f"[{i}/{total_arquivos}] ✓ {nome_arq}")
                else:
                    arquivos_com_erro += 1
                    print(f"[{i}/{total_arquivos}] ✗ {nome_arq}: {erro}")
                porcentagem = (i / total_arquivos) * 100
                tempo_decorrido = time.time() - inicio
                tempo_medio = tempo_decorrido / i
                tempo_restante = tempo_medio * (total_arquivos - i)
                print(f"Progresso: {porcentagem:.1f}% | "
                      f"Tempo decorrido: {tempo_decorrido:.1f}s | "
                      f"Tempo restante estimado: {tempo_restante:.1f}s")
                if i % 5 == 0:
                    gc.collect()
        except KeyboardInterrupt:
            print("\nProcessamento interrompido pelo usuário")
            pool.terminate()
        except Exception as e:
            print(f"\nErro no processamento: {str(e)}")
            pool.terminate()
    tempo_total = time.time() - inicio
    print(f"\nResumo do processamento:")
    print(f"Total de arquivos .dat: {total_arquivos}")
    print(f"Arquivos processados com sucesso: {arquivos_processados}")
    print(f"Arquivos com erro: {arquivos_com_erro}")
    print(f"Tempo total: {tempo_total:.1f}s")
    print(f"Tempo médio por arquivo: {tempo_total/total_arquivos:.1f}s")

if __name__ == '__main__':
    main() 
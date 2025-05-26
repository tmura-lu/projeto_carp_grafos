import os
import sys
from heapq import heappush, heappop
from collections import defaultdict
from functools import lru_cache

def criar_lista_adjacencia(grafo):
    adj = defaultdict(list)
    for (u, v), peso in grafo.arestas.items():
        if isinstance(peso, list):
            peso = peso[0]
        adj[u].append((v, peso))
        adj[v].append((u, peso))  
    for (u, v), peso in grafo.arcos.items():
        if isinstance(peso, list):
            peso = peso[0]
        adj[u].append((v, peso))
    return adj

def dijkstra(grafo, origem, destino=None):
    dist = {v: float('inf') for v in grafo.vertices}
    dist[origem] = 0
    prev = {v: None for v in grafo.vertices}
    pq = [(0, origem)]
    visitados = set()

    adj = criar_lista_adjacencia(grafo)

    while pq:
        d, u = heappop(pq)
        
        if u in visitados:
            continue
            
        visitados.add(u)
        
        if destino and u == destino:
            break

        for v, peso in adj[u]:
            if v not in visitados:
                novo_custo = d + peso
                if novo_custo < dist[v]:
                    dist[v] = novo_custo
                    prev[v] = (u, 'aresta' if (u, v) in grafo.arestas or (v, u) in grafo.arestas else 'arco')
                    heappush(pq, (dist[v], v))
    
    return dist, prev

def reconstruir_caminho(prev, origem, destino, grafo):
    if destino not in prev or prev[destino] is None:
        return [], float('inf')
        
    caminho = []
    custo = 0
    atual = destino
    
    while atual != origem:
        anterior, tipo = prev[atual]
        caminho.append((anterior, atual, tipo))
        if tipo == 'aresta':
            peso = grafo.get_peso(anterior, atual)
            if isinstance(peso, list):
                peso = peso[0]
            custo += peso
        else:  
            peso = grafo.get_peso(anterior, atual)
            if isinstance(peso, list):
                peso = peso[0]
            custo += peso
        atual = anterior
        
    return list(reversed(caminho)), custo

def calcular_distancia_entre_vertices(grafo, origem, destino, deposito):
    if not hasattr(grafo, 'cache_distancias'):
        grafo.cache_distancias = {}
    chave = (origem, destino, deposito)
    if chave in grafo.cache_distancias:
        return grafo.cache_distancias[chave]
    dist, prev = dijkstra(grafo, origem)
    if destino not in dist:
        resultado = (float('inf'), None)
    else:
        resultado = (dist[destino], prev)
    grafo.cache_distancias[chave] = resultado
    return resultado

def calcular_custo_rota(rota, grafo, deposito):
    if not rota:
        return 0
    
    custo_total = 0

    primeiro_servico = rota[0]
    dist_inicial, prev_inicial = calcular_distancia_entre_vertices(grafo, deposito, primeiro_servico['u'], deposito)
    if dist_inicial == float('inf'):
        return float('inf')
    custo_total += dist_inicial

    for i, servico in enumerate(rota):
        if servico['tipo'] == 'aresta':
            custo_total += servico['custo']
        else:  
            if not grafo.tem_arco(servico['u'], servico['v']):
                return float('inf')  # Caminho impossível
            custo_total += servico['custo']

        if i < len(rota) - 1:
            proximo = rota[i + 1]
            dist, _ = calcular_distancia_entre_vertices(grafo, servico['v'], proximo['u'], deposito)
            if dist == float('inf'):
                return float('inf')
            custo_total += dist

    ultimo_servico = rota[-1]
    dist_final, _ = calcular_distancia_entre_vertices(grafo, ultimo_servico['v'], deposito, deposito)
    if dist_final == float('inf'):
        return float('inf')
    custo_total += dist_final
    
    return custo_total

def encontrar_servicos_proximos(servico, servicos_disponiveis, grafo, max_dist=float('inf')):
    proximos = []
    for s in servicos_disponiveis:
        if s == servico:
            continue
        dist, _ = calcular_distancia_entre_vertices(grafo, servico['v'], s['u'], None)
        if dist != float('inf'):
            proximos.append((s, dist))
    return sorted(proximos, key=lambda x: x[1])

def encontrar_melhor_insercao(servicos_disponiveis, rota_atual, grafo, deposito, capacidade):
    melhor_servico = None
    melhor_posicao = None
    menor_custo_adicional = float('inf')
    
    carga_atual = sum(s['demanda'] for s in rota_atual)

    if not rota_atual:
        dist_deposito, prev_deposito = dijkstra(grafo, deposito)
        for s in servicos_disponiveis:
            if s['demanda'] > capacidade:
                continue

            if s['tipo'] == 'arco' and not grafo.tem_arco(s['u'], s['v']):
                continue

            dist_ida = dist_deposito[s['u']]
            if dist_ida == float('inf'):
                continue
                
            dist_volta, _ = calcular_distancia_entre_vertices(grafo, s['v'], deposito, deposito)
            if dist_volta == float('inf'):
                continue
                
            custo_total = dist_ida + s['custo'] + dist_volta
            if custo_total < menor_custo_adicional:
                menor_custo_adicional = custo_total
                melhor_servico = [s]
                melhor_posicao = 0
                
        return melhor_servico, melhor_posicao, menor_custo_adicional

    custo_atual = calcular_custo_rota(rota_atual, grafo, deposito)
    
    for s in servicos_disponiveis:
        if carga_atual + s['demanda'] > capacidade:
            continue
            
        if s['tipo'] == 'arco' and not grafo.tem_arco(s['u'], s['v']):
            continue
            
        for i in range(len(rota_atual) + 1):
            nova_rota = rota_atual[:i] + [s] + rota_atual[i:]
            novo_custo = calcular_custo_rota(nova_rota, grafo, deposito)
            
            if novo_custo == float('inf'):
                continue  # Inserção impossível nesta posição
                
            custo_adicional = novo_custo - custo_atual
            
            fator_capacidade = (carga_atual + s['demanda']) / capacidade
            custo_ajustado = custo_adicional * (1 - fator_capacidade * 0.1)
            
            if custo_ajustado < menor_custo_adicional:
                menor_custo_adicional = custo_ajustado
                melhor_servico = [s]
                melhor_posicao = i
    
    return melhor_servico, melhor_posicao, menor_custo_adicional

def greedy_constructor(grafo, capacidade, deposito='1'):
    """Constrói uma solução usando estratégia gulosa melhorada"""
    rotas = []
    servicos = []
    for (u, v), peso in grafo.arestas_req.items(): 
        if isinstance(peso, list) and len(peso) > 1 and peso[1] > 0: 
            servicos.append({
                'u': u,
                'v': v,
                'tipo': 'aresta',
                'custo': peso[0],
                'demanda': peso[1]
            })
    
    for (u, v), peso in grafo.arcos_req.items():  
        if isinstance(peso, list) and len(peso) > 1 and peso[1] > 0: 
            servicos.append({
                'u': u,
                'v': v,
                'tipo': 'arco',
                'custo': peso[0],
                'demanda': peso[1]
            })
    
    if not servicos:
        print("Nenhum serviço requerido encontrado no grafo")
        return []
        

    servicos.sort(key=lambda x: x['demanda'], reverse=True)
    
    servicos_restantes = servicos.copy()
    rota_atual = []
    carga_atual = 0
    
    while servicos_restantes:
        servicos_inserir, posicao, custo = encontrar_melhor_insercao(
            servicos_restantes, rota_atual, grafo, deposito, capacidade
        )
        
        if not servicos_inserir or carga_atual + sum(s['demanda'] for s in servicos_inserir) > capacidade:
            if rota_atual:
                rotas.append(rota_atual)
            rota_atual = []
            carga_atual = 0
            continue
        
        for s in servicos_inserir:
            rota_atual = rota_atual[:posicao] + [s] + rota_atual[posicao:]
            servicos_restantes.remove(s)
            carga_atual += s['demanda']
            posicao += 1
    
    if rota_atual:
        rotas.append(rota_atual)
    
    return rotas 
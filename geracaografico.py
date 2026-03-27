import random
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from scipy.optimize import curve_fit
import statistics

# --------------------------------------------------------
# Funções de ordenação
# --------------------------------------------------------
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                trocou = True
        if not trocou:
            break
 
def insertion_sort(arr):
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = chave
 
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# --------------------------------------------------------
# Geração de datas aleatórias
# --------------------------------------------------------
def gerar_datas(n):
    base = datetime(2000, 1, 1)
    datas = [base + timedelta(days=random.randint(0, 9000)) for _ in range(n)]
    return datas

# --------------------------------------------------------
# Medição de tempo com suavização e filtro de ruído
# --------------------------------------------------------
def medir_tempo(algoritmo, n, repeticoes=500):
    """
    Mede o tempo de execução (melhor e pior caso) com suavização:
    - repete várias vezes
    - remove outliers
    - ignora tempos muito pequenos (ruído)
    - usa mediana para estabilidade
    """
    tempos_melhor = []
    tempos_pior = []
    for _ in range(repeticoes):
        dados = gerar_datas(n)
        dados_pior = sorted(dados, reverse=True)
        dados_melhor = sorted(dados)

   # Melhor caso
    inicio = time.perf_counter()
    algoritmo(dados_melhor.copy())
    t = time.perf_counter() - inicio
    tempos_melhor.append(t)
    

    # Pior caso
    inicio = time.perf_counter()
    algoritmo(dados_pior.copy())
    t = time.perf_counter() - inicio
    tempos_pior.append(t)
    
    def suavizar(valores):
        return statistics.median(valores)
 
    return suavizar(tempos_melhor), suavizar(tempos_pior)

# --------------------------------------------------------
# Ajuste de curvas teóricas (usando curve_fit)
# --------------------------------------------------------
def ajustar_curva(N, tempos, funcao):
    popt, _ = curve_fit(funcao, N, tempos)
    return popt
 
# Modelos teóricos de complexidade
def linear(n, a, b):          # O(n)
    return a * n + b
 
def nlogn(n, a, b):           # O(n log n)
    return a * n * np.log(n) + b
 
def quadratic(n, a, b, c):       # O(n²)
    return a * n**2 + b*n + c


# --------------------------------------------------------
# Função principal para gerar gráficos
# --------------------------------------------------------

def legenda_fit(modelo_teorico, popt, qual):
    nome = "Fit " + qual
    if modelo_teorico is linear and len(popt) == 2:
        a, b = popt
        return f"{nome}: y = {a:.3e}*N + {b:.3e}"
    if modelo_teorico is nlogn and len(popt) == 2:
        a, b = popt
        return f"{nome}: y = {a:.3e}*N·log(N) + {b:.3e}"
    if modelo_teorico is quadratic and len(popt) == 3:
        a, b, c = popt
        return f"{nome}: y = {a:.3e}*N^2 + {b:.3e}*N + {c:.3e}"
    # fallback genérico pelo número de params
    if len(popt) == 2:
        a, b = popt
        return f"{nome}: y = {a:.3e}*f(N) + {b:.3e}"
    if len(popt) == 3:
        a, b, c = popt
        return f"{nome}: y = {a:.3e}*f1(N) + {b:.3e}*f2(N) + {c:.3e}"
    return f"{nome}: parâmetros = " + ", ".join(f"{p:.3e}" for p in popt)

def analisar_algoritmo(nome, algoritmo, modelo_teorico, cor_melhor, cor_pior):
    N = np.arange(100, 1001, 100)
    tempos_melhor = []
    tempos_pior = []
 
    for n in N:
        t_melhor, t_pior = medir_tempo(algoritmo, n)
        tempos_melhor.append(t_melhor)
        tempos_pior.append(t_pior)

    # Ajuste das curvas teóricas
    popt_melhor = ajustar_curva(N, tempos_melhor, modelo_teorico)
    popt_pior = ajustar_curva(N, tempos_pior, modelo_teorico)
 
    fit_melhor = modelo_teorico(N, *popt_melhor)
    fit_pior = modelo_teorico(N, *popt_pior)
    print(fit_pior)
    # Gráfico
    plt.figure(figsize=(10, 6))
    plt.semilogy(N, tempos_melhor, 'o', color=cor_melhor, label='Melhor caso (dados)')
    plt.semilogy(N, tempos_pior, 'o', color=cor_pior, label='Pior caso (dados)')
    plt.semilogy(N, fit_melhor, '--', color=cor_melhor,
             label=legenda_fit(modelo_teorico, popt_melhor, "melhor"))
    plt.semilogy(N, fit_pior, '--', color=cor_pior,
             label=legenda_fit(modelo_teorico, popt_pior, "pior"))
    plt.title(nome)
    plt.xlabel('N (quantidade de datas)')
    plt.ylabel('Tempo (s) [escala logarítmica]')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(f'{nome.lower().replace(" ", "_")}.png', dpi=300)
    plt.show()
 
    return N, tempos_pior, popt_pior

# --------------------------------------------------------
# Execução de cada algoritmo
# --------------------------------------------------------
bubble_N, bubble_pior, _ = analisar_algoritmo("Bubble Sort", bubble_sort, quadratic, 'blue', 'red')
insertion_N, insertion_pior, _ = analisar_algoritmo("Insertion Sort", insertion_sort, quadratic, 'green', 'orange')
merge_N, merge_pior, _ = analisar_algoritmo("Merge Sort", merge_sort, nlogn, 'purple', 'brown')
 

# --------------------------------------------------------
# Gráfico comparando PIORES CASOS
# --------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.semilogy(bubble_N, bubble_pior, 'o--', color='red', label='Bubble Sort (pior caso, O(n²))')
plt.semilogy(insertion_N, insertion_pior, 'o--', color='orange', label='Insertion Sort (pior caso, O(n²))')
plt.semilogy(merge_N, merge_pior, 'o--', color='brown', label='Merge Sort (pior caso, O(n log n))')
plt.title('Comparação dos piores casos (ordenando datas)')
plt.xlabel('N (quantidade de datas)')
plt.ylabel('Tempo (s) [escala logarítmica]')
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.tight_layout()
plt.savefig('comparacao_pior_caso.png', dpi=300)
plt.show()
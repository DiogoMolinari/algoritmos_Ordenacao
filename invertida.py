import time
import matplotlib.pyplot as plt
import numpy as np
import statistics

# -----------------------------
# Algoritmos de ordenação
# -----------------------------
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

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

# -----------------------------
# Função para medir tempo
# -----------------------------
def medir_tempo(sort_func, arr, repeticoes=3):
    tempos = []
    for _ in range(repeticoes):
        arr_copy = arr.copy()
        start = time.perf_counter()
        sort_func(arr_copy)
        tempos.append(time.perf_counter() - start)
    return statistics.mean(tempos)

# -----------------------------
# Configuração dos testes
# -----------------------------
sizes = list(range(100, 1001, 100))
repeticoes = 5

tempos = {'Bubble': [], 'Insertion': [], 'Merge': []}

# -----------------------------
# Execução dos testes (pior caso)
# -----------------------------
for size in sizes:
    arr_invertido = list(range(size, 0, -1))  # pior caso

    tempos['Bubble'].append(medir_tempo(bubble_sort, arr_invertido, repeticoes))
    tempos['Insertion'].append(medir_tempo(insertion_sort, arr_invertido, repeticoes))
    tempos['Merge'].append(medir_tempo(merge_sort, arr_invertido, repeticoes))

# -----------------------------
# Função de ajuste (fit)
# -----------------------------
def fit_curve(x, y, degree=2):
    """Ajuste polinomial no log dos dados"""
    coeffs = np.polyfit(np.log10(x), np.log10(y), degree)
    poly = np.poly1d(coeffs)
    return poly

# -----------------------------
# Gráfico único (pior caso)
# -----------------------------
plt.figure(figsize=(10,6))
for nome, cor, teorico in zip(
    ['Bubble', 'Insertion', 'Merge'],
    ['r', 'g', 'b'],
    ['n²', 'n²', 'n log n']
):
    y = np.array(tempos[nome])
    x = np.array(sizes)

    # Pontos experimentais
    plt.semilogy(x, y, 'o', color=cor, label=f'{nome} Sort (exp)')

    # Curva ajustada (fit)
    poly = fit_curve(x, y, degree=2 if nome != 'Merge' else 1)
    y_fit = 10**poly(np.log10(x))
    plt.semilogy(x, y_fit, '-', color=cor)

    # Curva teórica (normalizada)
    if teorico == 'n²':
        y_teorico = x**2
    elif teorico == 'n log n':
        y_teorico = x * np.log2(x)
    y_teorico = y_teorico / max(y_teorico) * max(y)
    plt.semilogy(x, y_teorico, '--', color=cor, alpha=0.6, label=f'{nome} teórico O({teorico})')

plt.xlabel('Tamanho da lista (n)')
plt.ylabel('Tempo (s)')
plt.title('Desempenho dos algoritmos de ordenação (lista invertida — pior caso)')
plt.legend()
plt.grid(True)
plt.show()

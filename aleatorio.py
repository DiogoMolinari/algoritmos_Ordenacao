import random
import time
import matplotlib.pyplot as plt
import statistics
import math

# Funções de ordenação
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

# Configurações de teste
sizes = list(range(100, 1001, 100))
repeticoes = 5

# Guardar tempos médios
times_bubble, times_insertion, times_merge = [], [], []

for size in sizes:
    arr = [random.randint(1, 10000) for _ in range(size)]

    # Bubble Sort
    tempos = []
    for _ in range(repeticoes):
        arr_copy = arr.copy()
        start = time.perf_counter()
        bubble_sort(arr_copy)
        tempos.append(time.perf_counter() - start)
    times_bubble.append(statistics.mean(tempos))

    # Insertion Sort
    tempos = []
    for _ in range(repeticoes):
        arr_copy = arr.copy()
        start = time.perf_counter()
        insertion_sort(arr_copy)
        tempos.append(time.perf_counter() - start)
    times_insertion.append(statistics.mean(tempos))

    # Merge Sort
    tempos = []
    for _ in range(repeticoes):
        arr_copy = arr.copy()
        start = time.perf_counter()
        merge_sort(arr_copy)
        tempos.append(time.perf_counter() - start)
    times_merge.append(statistics.mean(tempos))

# Cálculo das curvas teóricas
theoretical_bubble = [1e-8 * n**2 for n in sizes]
theoretical_insertion = [1e-8 * n**2 for n in sizes]
theoretical_merge = [5e-7 * n * math.log2(n) for n in sizes]

# Plotagem com estilo padronizado
plt.figure(figsize=(10, 6))
plt.semilogy(sizes, times_bubble, 'o-', color='red', label='Bubble Sort (exp)')
plt.semilogy(sizes, times_insertion, 'o-', color='green', label='Insertion Sort (exp)')
plt.semilogy(sizes, times_merge, 'o-', color='blue', label='Merge Sort (exp)')

plt.semilogy(sizes, theoretical_bubble, '--', color='red', alpha=0.6, label='Bubble teórico O(n²)')
plt.semilogy(sizes, theoretical_insertion, '--', color='green', alpha=0.6, label='Insertion teórico O(n²)')
plt.semilogy(sizes, theoretical_merge, '--', color='blue', alpha=0.6, label='Merge teórico O(n log n)')

plt.xlabel('Tamanho da lista (n)')
plt.ylabel('Tempo (s)')
plt.title('Desempenho dos algoritmos de ordenação (lista aleatória)')
plt.legend()
plt.grid(True, which="both", linestyle='--', linewidth=0.6)
plt.tight_layout()
plt.show()

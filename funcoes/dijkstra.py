import numpy as np

def dijkstra(A, s):
    A = np.asarray(A)
    n = A.shape[0]
    dist = np.full(n, np.inf, dtype=float)
    predecessores = np.full(n, -1, dtype=int)
    visit = np.zeros(n, dtype=bool)

    dist[s] = 0

    for _ in range(n):
        candidatos = np.where(~visit, dist, np.inf)
        u = int(np.argmin(candidatos))

        if np.isinf(dist[u]):
            break

        visit[u] = True

        vizinhos = np.flatnonzero(A[u])

        for vizinho in vizinhos:
            if visit[vizinho]:
                continue 

            if dist[vizinho] > dist[u] + 1:
                dist[vizinho] = dist[u] + 1
                predecessores[vizinho] = u

    return dist, predecessores


import heapq

def main():
    n, m, st, ed, K = map(int, input().split())
    K = min(K, n)
    
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))
        
    dst = [[float('inf')] * (K + 1) for _ in range(n)]
    dst[st][0] = 0
    pq = [(0, st, 0)]
    
    ans = -1
    while pq:
        d, u, k = heapq.heappop(pq)
        
        if d > dst[u][k]: 
            continue
            
        if u == ed:
            ans = d
            break
            
        for v, w in adj[u]:
            if d + w < dst[v][k]:
                dst[v][k] = d + w
                heapq.heappush(pq, (d + w, v, k))
                
            if k < K and d < dst[v][k + 1]:
                dst[v][k + 1] = d
                heapq.heappush(pq, (d, v, k + 1))
                
    print(ans)

if __name__ == '__main__':
    main()
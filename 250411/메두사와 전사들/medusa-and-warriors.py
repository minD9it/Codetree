import heapq # 최단 경로 다익스트라
from collections import deque

# 이동 좌표: 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

INF = int(1e9)

def bfs(start, v, visited):
    q = deque([start])
    visited[start] = True

    while q:
        v = q.popleft()
        print(v, end=' ')

        for i in graph[v]:
            if not visited[i]:
                q.append(i)
                visited[i] = True

def medusa_sight(current, direction):
    if 
    
def manhattan_dist(a, b):
    return abs(a[0] - b[0]) - abs(a[1]-b[1])


n, m = map(int, input().split()) # 마을 크기, 전사 수

medusas = list(map(int, input().split()))
medusa_home = medusas[:2] # 메두사 집 좌표
park = medusas[2:] # 공원 좌표

warriors_m = list(map(int, input().split())) # 전사 초기 위치 좌표
warriors = list(warriors[i:i+2] for i in range(0, m*2, 2))

village = [[] for i in range(n+1)] # 마을 지도
distance = [INF] * (n+1) # 거리 계산
for i in range(n):
    road_info = list(map(int, input().split())) # 마을 도로 정보
    village[n].append(road_info)



def dijkstra(start):
    q = []
    heapq.heappush(q, (0, start))
    distance[start] = 0

    while q:
        dist, now = heapq.heappop(q)
        if distance[now] < dist: continue
        for i in village[now]:
            cost = dist + i[1]
            if cost < distnace[i[0]]:
                distance[i[0]] = cost
                heapq.heappush(q, (cost, i[0]))


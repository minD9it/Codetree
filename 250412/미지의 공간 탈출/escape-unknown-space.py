from collections import deque

# 시간의 벽에서 시작 위치는 항상 윗면
def time_start(arr):
    length = len(arr[0])
    for i in range(length):
        for j in range(length):
            if arr[4][i][j] == 2: # 윗면의 좌표 중에 2가 있으면 그 곳이 시작 위치
                return 4, i, j
    

# 미지의 공간에서의 탈출구
def unknown_end(arr):
    length = len(arr)
    for i in range(length):
        for j in range(length):
            if arr[i][j] == 4:
                return i, j

def timewall_loc(arr):
    length = len(arr)
    for i in range(length):
        for j in range(length):
            if arr[i][j] == 3:
                return i, j

# 시간의 벽 탈출 -> 미지의 공간 시작
def time2unknow(arr, m): # 미지의 공간, 시간의 벽, 시간의 벽 크기
    # 미지의 공간에서 시간의 벽이 시작하는 위치
    si, sj = timewall_loc(arr)
    
    # m X m 크기의 시간의 벽이기 때문에 그 주변에 1이 아니고 0인 곳을 찾아야 함, 시간의 벽: 면 위치도 같이 파악해야 함
    d = 0 # 동서남북 중 하나 (0,1,2,3)
    ui, uj = 0, 0
    for i in range(-1, m+1): # (-1,0,1,2,3) 주변을 둘러싸고 있는 벽
        if i == 0: d = 3 # 북
        elif i == m+1: d = 2 # 남
        for j in range(m+2):
            if j == 0:d = 1 # 서
            elif j == m+1: d = 0 # 동
            if arr[si+i][sj+j] == 0:
                ui, uj = i, j

    # 시간의 벽 탈출구: 행은 항상 같음 , [d][m-1][?]
    ti, tj = 0, 0
    if d == 0: # 동, 행 반대로
        ti, tj = m-1, ui-si
    elif d == 1: # 서, 행-1
        ti, tj = m-1, ui-1
    elif d == 2: # 남, 열-1
        ti, tj = m-1, uj-1
    elif d == 3: # 북, 열 반대로
        ti, tj = m-1, uj-sj
    else:
        return -1

    return d, ti, tj, ui, uj


def time_bfs(arr, sd, si, sj, ed, ei, ej):
    length = len(arr)
    v = [[[0] * len(arr) for _ in range(len(arr))] for _ in range(5)] # 동서남북위 -> 각각 m X m 배열의 방문 그래프

    q = deque([sd, si, sj])
    v[sd][si][sj] = 1

    while q: 
        qd, qi, qj = deque.popleft()

        # 출구 찾음
        if (qd, qi, qj) == (ed, ei, ej):
            return v[qd][qi][qj] # 최단 거리 결과값

        # 상하좌우로 한 칸 이동: 다른 면으로 이동(범위 벗어남), 막힌 길
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = qi+di, qj+dj

            # 방향 설정: 네 방향으로 이동 가능
            if nj < 0: # 왼쪽 면으로 이동
                turn_left = [1, 3, 0, 2, 1]
                if qd == 5: nd = 1
                else: nd = turn_left[turn_left.index(qd)+1]

            # 오른쪽 면으로 이동
            if nj >= length:
                turn_right = [0, 3, 1, 2, 0]
                if qd == 5: nd = 0
                else: nd = turn_right[turn_right.index(qd)+1]

            # 위쪽 면으로 이동
            if ni < 0:
                if qd == 5: nd = 4
                else: nd = 5

            # 아래쪽 면으로 이동
            if pd == 5 and ni >= length: nd = 3

            #  미방문, 갈 수 있는 길
            if v[nd][ni][nj] == 0 and arr[nd][ni][nj] == 0:
                q.append([nd, ni, nj])
                v[nd][ni][nj] = v[qd][qi][qj] + 1 # 최단 거리 계산을 위해서 계속 +1을 하면서 진행
                
    return -1
        


def unknown_bfs(dist, arr, si, sj, ei, ej):
    length = len(arr)
    v = [[0]*len(arr) for _ in range(len(arr))] # 미지의 공간 만큼의 방문 그래프
    
    q = dqeue([si, sj])
    v[si][sj] = 1
        
    while q: #
        qi, qj = q.popleft()

        # 탈출구 찾음
        if (qi, qj) == (ei, ej):
            return dist + v[qi][qj]

        # 상하좌우로 한 칸 이동: 범위 벗어남, 시간 이상 현상, 막힌 길(1)
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = qi+di, qj+dj

            # 범위 안, 이동 가능한 길
            if 0<=ni<length and 0<=nj<length and arr[ni][nj] == 0:
                q.append([ni, nj])
                v[ni][nj] = v[qi][qj] + 1
    return -1

            

n, m, f = map(int, input().split()) # 미지의 공간, 시간의 벽, 시간 이상 현상 개수
unknown = [list(map(int, input().split())) for _ in range(n)] # 미지의 공간 생성
timewall = [[list(map(int, input().split())) for _ in range(m)] for _ in range(5)] # 동서남북 순서로 입력 -> 시간의 벽 생성
anomaly = [list(map(int, input().split())) for _ in range(f)] # 시간 이상 현상 생성


# 시작 위치, 종료 위치 찾기: 시간의 벽, 미지의 공간 각각의 위치
t_sd, t_si, t_sj = time_start(timewall)
t_ed, t_ei, t_ej, u_si, u_sj = time2unknow(unknown, m)
u_ei, u_ej = unknown_end(unknown)

# 시간의 벽에서 팀색 진행
dist = time_bfs(timewall, t_sd, t_si, t_sj, t_ed, t_ei, t_ej)

if dist != -1:
    # 미지의 공간에서 탐색 진행
    dist = unknown_bfs(dist, unknown, u_si, u_sj, u_ei, u_ej)

print(rdist)
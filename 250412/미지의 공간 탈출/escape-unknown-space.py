from collections import deque

# 시간의 벽에서 시작 위치는 항상 윗면
def time_start(arr):
    length = len(arr[0])
    for i in range(length):
        for j in range(length):
            if arr[4][i][j] == 2: # 윗면의 좌표 중에 2가 있으면 그 곳이 시작 위치
                return, 4, i, j
    

# 미지의 공간에서의 탈출구
def unknown_end(arr):
    length = len(arr)
    for i in range(length):
        for j in range(length):
            if arr[i][j] == 4:
                return i, j

# 시간의 벽 탈출 -> 미지의 공간 시작
def time2unknow(arr, arr2, m):
    ti, tj = 0, 0
    length = len(arr)
    for i in range(length):
        for j in range(length):
            if arr[i][j] == 3:
                ti, tj = i-1, j-1
                break
    # m X m 크기의 시간의 벽이기 때문에 그 주변에 1이 아니고 0인 곳을 찾아야 함, 시간의 벽 면 위치도 같이 파악해야 함
    d = 0 # 동서남북 중 하나 (0,1,2,3)
    ui, uj = 0, 0
    for i in range(m+2): # m + 2: 주변을 둘러싸고 있는 벽
        if i == 0: d = 3 # 북
        elif i == m+1: d = 2 # 남
        for j in range(m+2):
            if j == 0:d = 1 # 서
            elif j == m+1: d = 0 # 동
            if arr[ti+i][tj+j] == 0:
                ui, uj = i, j

    # 시간의 벽 탈출구: 행은 항상 같음 , [d][m-1][?]
    ti, tj = 0, 0
    if d == 0 or d == 2: # 동, 남
        ti, tj = m-1, j
    elif d == 1 or d == 3: # 서, 북
        return d, m-1, i
    

n, m, f = map(int, input().split()) # 미지의 공간, 시간의 벽, 시간 이상 현상 개수
unknown = [list(map(int, input().split())) for _ in range(n)] # 미지의 공간 생성
timewall = [[list(map(int, input().split())) for _ in range(m)] for _ in range(5)] # 동서남북 순서로 입력 -> 시간의 벽 생성
anomaly = [list(map(int, input().split())) for _ in range(f)] # 시간 이상 현상 생성


# 시작 위치, 종료 위치 찾기: 시간의 벽, 미지의 공간 각각의 위치
t_si, t_sj = time_start(timewall)
t_ei, t_ej = time_end(timewall)
u_si, u_sj = unknown_start(unknown)
u_ei, u_ej = unknown_end(unknown)

def time_bfs(timewall, si, sj, ei, ej): # 시작 위치, 종료 위치
    q = deque((si, sj))


    
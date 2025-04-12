from collections import deque

K, M = map(int, input().split())  # 탐사 반복 횟수, 벽면 유물 조각 개수
arr = [list(map(int, input().split())) for _ in range(5)] # 5x5 격자
scatter = list(map(int, input().split())) # 벽면 유물 조각

# 회전 각도
degree = [90, 180, 270]
# 회전 중심 좌표: 작은 열 -> 작은 행
c_xy = [(1,1), (2,1), (3,1), (1,2), (2,2), (3,2), (1,3), (2,3), (3,3)]

# 3x3 시계 방향 회전
def rotate(arr, n):
    n_arr = [[0]*3 for _ in range(3)]
    
    if n == 90:
        for i in range(3):
            for j in range(3):
                n_arr[i][j] = arr[2-j][i]

    elif n == 180:
        for i in range(3):
            for j in range(3):
                n_arr[i][j] = arr[2-i][2-j]

    elif n == 270:
        for i in range(3):
            for j in range(3):
                n_arr[i][j] = arr[j][2-i]

    return n_arr
    

def best_grid(arr):
    # 작은 각도 -> 작은 열 -> 작은 행 (같은 점수를 가지는 경우)
    best_score = 0
    best_x, best_y = 0, 0

    for x, y in c_xy:
        temp_arr = []
        temp_arr.append([arr[x-1][y-1], arr[x-1][y], arr[x-1][y+1]])
        temp_arr.append([arr[x][y-1], arr[x][y], arr[x][y+1]])
        temp_arr.append([arr[x+1][y-1], arr[x+1][y], arr[x+1][y+1]])

        for d in degree: # 90 -> 180 -> 270 순차 회전
            n_arr = rotate(temp_arr, d)
            arr[x-1][y-1], arr[x-1][y], arr[x-1][y+1] = n_arr[0]
            arr[x][y-1], arr[x][y], arr[x][y+1] = n_arr[1]
            arr[x+1][y-1], arr[x+1][y], arr[x+1][y+1] = n_arr[2]

            score, n_arr = find_bfs(arr)
            if score == 7: return score, n_arr
            if best_score < score: 
                best_score = score
                best_x, best_y = x, y

    return best_score, n_arr



def find_bfs(arr): # 5x5 격자
    # 제거할 위치는 어떻게 하면 좋을까
    tracking = [] # 격자 안에 있는 숫자들만큼
    result = 0

    q = deque()
    v = [[0]*5 for _ in range(5)] 

    q.append((0, 0))
    v[0][0] = 1
    cnt = 1 # 같은 값이 3개 이상 있어야 함


    while q:
        pi, pj = q.popleft() # 이 값이랑 같은 값 찾아야 함
        temp = []
        temp.append((pi, pj))

        # 상하좌우로 움직이면서 인접한 같은 값 탐색
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = pi+di, pj+dj # 상하좌우로 한 칸 움직인 위치

            # 범위내, 미방문이면서 같은 값을 가짐
            if 0<=ni<5 and 0<=nj<5 and v[ni][nj] == 0 and arr[pi][pj] == arr[ni][nj]:
                q.append((ni, nj))
                v[ni][nj] = 1
                cnt += 1
            
            if cnt >= 3: # 제거할 위치 표시
                result += cnt
        tracking.append([temp])

    # 제거할 유물 표시
    for t in tracking:
        if len(t) >= 3:
            for x, y in t:
                arr[x][y] = -1

    return result, arr


def new_grid(score, arr, v):
    result = 0
    # [1] -1인 위치 탐색: 작은 열 -> 큰 행
    x, y = [], []
    for j in range(5):
        for i in range(4, -1):
            if arr[i][j] == -1:
                arr[i][j] = v[0]
                v = v[1:]

    score, arr = find_bfs(arr)
    result += score
    return result, arr, v 

score = 0
v = scatter
for i in range(K):
    # [1] 3x3 시계 방향 회전 -> 최고의 격자 찾기, [2] 유물 획득 가치 최대화 - BFS
    score, n_arr = best_grid(arr)

    # [3] 새로운 조각 생성
    score, n_arr, v = new_grid(score, n_arr, v)

    # [4] [1]~[3] 반복 / 유물 획득 실패 시 종료
    if score == 0: break
    else: print(score, end=' ')
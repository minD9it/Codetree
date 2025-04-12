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


# def time_bfs(arr, sd, si, sj, ed, ei, ej):
#     length = len(arr)
#     q = deque()
#     v = [[[0] * length for _ in range(length)] for _ in range(5)] # 동서남북위 -> 각각 m X m 배열의 방문 그래프

#     q.append((sd, si, sj))
#     v[sd][si][sj] = 1
 
#     while q:
#         qd, qi, qj = q.popleft()

#         # 출구 찾음
#         if (qd, qi, qj) == (ed, ei, ej):
#             return v[qd][qi][qj] # 최단 거리 결과값

#         # 상하좌우로 한 칸 이동: 다른 면으로 이동(범위 벗어남), 막힌 길
#         for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
#             nd, ni, nj = qd, qi+di, qj+dj

#             # 방향 설정: 네 방향으로 이동 가능
#             # 동서남북면 -> 윗면
#             if ni < 0:
#                 if qd == 4: nd, ni, nj = 3, 0, (m-1)-qj
#                 elif qd == 0: nd, ni, nj = 4, (m-1)-qj, m-1
#                 elif qd == 1: nd, ni, nj = 4, qj, 0
#                 elif qd == 2: nd, ni, nj = 4, m-1, qj
#                 elif qd == 3: nd, ni, nj = 4, 0, (m-1)-qj

#             elif ni >= length and qd == 4: # 윗면만 아래로 이동 가능, 행은 항상 0
#                 nd, ni, nj = 2, 0, qj

#             elif nj < 0: # 왼쪽 면으로 이동, 행은 유지, 열은 마지막 인덱스
#                 if qd == 4: nd, ni, nj = 1, 0, qi
#                 else:
#                     turn_left = {0:2, 1:3, 2:1, 3:0}
#                     nd, ni, nj = turn_left[qd], qi, m-1

#             # 오른쪽 면으로 이동, 행 유지, 열 첫 인덱스
#             elif nj >= length:
#                 if qd == 4: nd, ni, nj = 0, 0, (m-1)-qi
#                 else:
#                     turn_right = {0:3, 1:2, 2:0, 3:1}
#                     nd, ni, nj = turn_right[qd], qi, 0
            
#             #  미방문, 갈 수 있는 길
#             if (v[nd][ni][nj]==0) and (arr[nd][ni][nj]==0):
#                 q.append((nd, ni, nj))
#                 v[nd][ni][nj] = v[qd][qi][qj] + 1 # 최단 거리 계산을 위해서 계속 +1을 하면서 진행

#     return -1

left_nxt = {0:2, 2:1, 1:3, 3:0}
right_nxt = {0:3, 2:0, 1:2, 3:1}
# dist = bfs_3d(sk_3d, si_3d, sj_3d,ek_3d, ei_3d, ej_3d)
from collections import deque
def time_bfs(sk, si, sj,ek, ei, ej):
    q = deque()
    v = [[[0]*M for _ in range(M)] for _ in range(5)]

    q.append((sk,si,sj))
    v[sk][si][sj]=1

    while q:
        ck,ci,cj = q.popleft()

        if (ck,ci,cj)==(ek,ei,ej):
            # myprint_3d(v)
            return v[ck][ci][cj]

        # 네방향, 범위내/범위밖->다른평명 이동처리, 미방문
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj

            # 범위밖
            if ni<0:    # 위쪽 범위 이탈
                if ck==0:   nk,ni,nj = 4,(M-1)-cj,M-1
                elif ck==1: nk,ni,nj = 4,cj,0
                elif ck==2: nk,ni,nj = 4,M-1,cj
                elif ck==3: nk,ni,nj = 4,0,(M-1)-cj
                elif ck==4: nk,ni,nj = 3,0,(M-1)-cj
            elif ni>=M: # 아래쪽 범위이탈
                if ck==4:   nk,ni,nj = 2,0,cj
                else:       continue
            elif nj<0:  # 왼쪽 범위이탈
                if ck==4:   nk,ni,nj = 1,0,ci
                else:
                    nk,ni,nj = left_nxt[ck],ci,M-1
            elif nj>=M: # 오른쪽 범위이탈
                if ck==4:   nk,ni,nj = 0,0,(M-1)-ci
                else:
                    nk,ni,nj = right_nxt[ck],ci,0
            else:       # 이탈아니면 같은 평면
                nk=ck

            # 미방문, 조건 맞으면
            if v[nk][ni][nj]==0 and timewall[nk][ni][nj]==0:
                q.append((nk,ni,nj))
                v[nk][ni][nj]=v[ck][ci][cj]+1        

def unknown_bfs(v, dist, arr, si, sj, ei, ej):
    length = len(arr)
    q = deque()
    
    q.append((si, sj))
    v[si][sj] = 1
        
    while q:
        qi, qj = q.popleft()

        # 탈출구 찾음
        if (qi, qj) == (ei, ej):
            return dist + v[qi][qj]

        # 상하좌우로 한 칸 이동: 범위 벗어남, 시간 이상 현상, 막힌 길(1)
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = qi+di, qj+dj

            # 범위 안, 이동 가능한 길
            if 0<=ni<length and 0<=nj<length and v[qi][qj]+1<v[ni][nj] and arr[ni][nj] == 0:
                q.append((ni, nj))
                v[ni][nj] = v[qi][qj] + 1
    return -1

            

N, M, f = map(int, input().split()) # 미지의 공간, 시간의 벽, 시간 이상 현상 개수
unknown = [list(map(int, input().split())) for _ in range(n)] # 미지의 공간 생성
timewall = [[list(map(int, input().split())) for _ in range(M)] for _ in range(5)] # 동서남북윗면 순서로 입력 -> 시간의 벽 생성
anomaly = [list(map(int, input().split())) for _ in range(f)] # 시간 이상 현상 생성


# 시작 위치, 종료 위치 찾기: 시간의 벽, 미지의 공간 각각의 위치
t_sd, t_si, t_sj = time_start(timewall)
t_ed, t_ei, t_ej, u_si, u_sj = time2unknow(unknown, M)
u_ei, u_ej = unknown_end(unknown)

# 시간의 벽에서 팀색 진행
# dist = time_bfs(timewall, t_sd, t_si, t_sj, t_ed, t_ei, t_ej)
dist = time_bfs(t_sd, t_si, t_sj, t_ed, t_ei, t_ej)

# 동 서 남 북
di=[ 0, 0, 1,-1]
dj=[ 1,-1, 0, 0]
if dist!=-1:
    # [3] 2차원 탐색 준비: 시간이상현상 처리해서 v에 시간표시: BFS확산시 그보다 작으면 통과하게표시
    v = [[401]*N for _ in range(N)]
    for wi,wj,wd,wv in wall:        # wv 단위로 wd방향으로 확산표시(출구가 아닌경우만 확산)
        v[wi][wj]=1
        for mul in range(1, N+1):
            wi,wj = wi+di[wd], wj+dj[wd]
            if 0<=wi<N and 0<=wj<N and arr[wi][wj]==0 and (wi,wj)!=(ei,ej):
                if v[wi][wj]>wv*mul:    # 더 큰 값 일때만 갱신(겹칠수있으니)
                    v[wi][wj]=wv*mul
            else:
                break
    dist = unknown_bfs(v, dist, unknown, u_si, u_sj, u_ei, u_ej)

# if dist != -1:
#     # 시간 이상 처리, 방문 그래프 활용하여 미리 벽을 만들어 놓기
#     v = [[401]*n for _ in range(n)]
    
#     # 장애물과 탈출구가 있으면 시간 이상 현상 사라짐
#     for ai, aj, ad, av in anomaly:
#         v[ai][aj] = 1 # 시작 위치는 1
#         # 한 방향으로 이동
#         if ad == 0: # 동 -> 오른쪽
#             move = [0, 1] * av # 상수의 배수만큼 씩 움직임
#             ni, nj = ai+move[0], aj+move[1]
#             if 0<=ni<M and 0<=nj<M and known[ni][nj] == 0 and (ni, nj) != (u_ei, u_ej):
#                 if v[ni][nj] > v[ai][aj] * av: v[ni][nj] = v[ai][aj] * av
#             else: break

#         elif ad == 1: # 서 -> 왼쪽
#             move = [0, -1] * av
#             ni, nj = ai+move[0], aj+move[1]
#             if 0<=ni<M and 0<=nj<M and known[ni][nj] == 0 and (ni, nj) != (u_ei, u_ej):
#                 if v[ni][nj] > v[ai][aj] * av: v[ni][nj] = v[ai][aj] * av
#             else: break

#         elif ad == 2: # 남 -> 아래
#             move = [1, 0] * av
#             ni, nj = ai+move[0], aj+move[1]
#             if 0<=ni<M and 0<=nj<M and known[ni][nj] == 0 and (ni, nj) != (u_ei, u_ej):
#                 if v[ni][nj] > v[ai][aj] * av: v[ni][nj] = v[ai][aj] * av
#             else: break

#         elif ad == 3: # 북 -> 위
#             move = [-1, 0] * av 
#             ni, nj = ai+move[0], aj+move[1]
#             if 0<=ni<M and 0<=nj<M and known[ni][nj] == 0 and (ni, nj) != (u_ei, u_ej):
#                 if v[ni][nj] > v[ai][aj] * av: v[ni][nj] = v[ai][aj] * av
#             else: break

#     # 미지의 공간에서 탐색 진행
#     dist = unknown_bfs(v, dist, unknown, u_si, u_sj, u_ei, u_ej)

print(dist)
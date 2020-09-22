import itertools

def print_result(result):
    (L, M, N, E, J) = result 
    print("Loes woont op verdieping {}".format(L))
    print("Marja woont op verdieping {}".format(M))
    print("Niels woont op verdieping {}".format(N))
    print("Erik woont op verdieping {}".format(E))
    print("Joep woont op verdieping {}".format(J))

floors = [0, 1, 2, 3, 4]

for (L, M, N, E, J) in list(itertools.permutations(floors)):
    # Loes woont niet op de bovenste verdieping
    if L == 4:
        continue
    # Marja woont niet op de begane grond
    if M == 0:
        continue
    # Erik woont tenminste één verdieping) hoger dan Marja
    if E <= M:
        continue
    # Niels woont niet op de bagane grond en niet op de bovenste verdieping
    if N == 0 or N == 4:
        continue
    # Joep woont niet op een verdieping één hoger of lager dan Niels
    if J == N - 1 or J == N + 1:
        continue
    # Niels woont niet op een verdieping één hoger of lager dan Marja
    if N == M - 1 or N == M + 1:
        continue
    
    print_result((L, M, N, E, J))

import sys

def print_lines(S):
    M = []
    for i in range(len(S)):
        M.append(shift(S, i))
    M.sort()
    f = open("table.txt", "w")
    for i in range(len(M)):
        if (M[i][-1] != '\n'):
            f.write(M[i][-1] + "  " + M[i][:30].replace('\n', "\\n") + "\n")    
    f.close()

# Shifts the given string to the right by the given distance amount.
def shift(text, dist):
    dist %= len(text)
    return text[-dist:] + text[:-dist]

# Applies Burrows-Wheeler transformation on the given string.
def bwt_encode(S):
    M = []
    for i in range(len(S)):
        M.append(shift(S, i))
    M.sort()
    L = ""
    for i in range(len(M)):
        L += M[i][-1]
    return L, M.index(S)

# Reverses the Burrows-Wheeler transformation on the given string.
def bwt_decode(L, I):
    F = sorted(L)
    F = "".join(F)
    T = []
    for ch in L:
        j = F.index(ch)
        while j in T:
            j += 1
        T.append(j)
    S = ""
    for i in range(len(L)):
        idx = I
        for n in range(i):
            idx = T[idx]
        S = L[idx] + S
    return S

def mtf_encode(L, alpha):
    alpha_mod  = alpha.copy()
    R = []
    for ch in L:
        idx = alpha_mod.index(ch)
        R.append(idx)
        alpha_mod.insert(0, alpha_mod.pop(idx))
    return R

def mtf_decode(R, alpha):
    alpha_mod  = alpha.copy()
    L = ""
    for idx in R:
        L += alpha_mod[idx]
        alpha_mod.insert(0, alpha_mod.pop(idx))
    return L

def bwt_quicksort_encode(S, k=8):
    S_prime = S + '\000' * k
    alpha = sorted(list(dict.fromkeys(S_prime)))
    W = []
    for i in range(len(S)):
        W.append(S_prime[i:i+k])
    V = list(range(len(W)))
    N = len(W)
    for ch_idx in range(2):
        V_sort = [0] * N
        count = dict((k, 0) for k in alpha)
        for i in range(N):
            count[W[i][ch_idx]] += 1
        print(count)
        for i in range(1, len(alpha)):
            count[alpha[i]] += count[alpha[i - 1]]
        
        i = N - 1
        while i >= 0:
            ch = W[i][ch_idx]
            V_sort[count[ch] - 1] = V[i]
            count[ch] -= 1
            i -= 1

        for i in range(0, N):
            V[i] = V_sort[i]
    print(V)

if __name__ == "__main__":
    # original = input("Enter the text to be compressed: ")
    # print()
    # alpha = sorted(list(dict.fromkeys(original))) # the min. alphabet for the string
    # print("Original text : " + str(original))
    
    # L, I = bwt_encode(original)
    # R    = mtf_encode(L, alpha)
    # print("BWT Encoded   : " + str(L))
    # print("MTF Encoded   : " + str(R))

    # L      = mtf_decode(R, alpha)
    # result = bwt_decode(L, I)
    # print("MTF Decoded   : " + str(L))
    # print("BWT Decoded   : " + str(result))
    # print()

    # bwt_quicksort_encode(original)

    transform = True
    file_name = sys.argv[1]

    if transform:
        with open(file_name + ".txt", "r") as f:
            original = f.read()

        alpha = sorted(list(dict.fromkeys(original)))


        print_lines(original)

        # L, I = bwt_encode(original)
        # R    = mtf_encode(L, alpha)

        # string = "".join([chr(i) for i in R])

        # f = open("alpha", "w")
        # f.write(alpha)
        # f.close()
        # f = open(file_name + ".out", "w")
        # f.write(string)
        # f.close()
        # f = open("rank", "w")
        # f.write(str(I))
        # f.close()
    else:
        with open("output", "r") as f:
            L = f.read()
        with open("rank", "r") as f:
            I = int(f.read())
        result = bwt_decode(L, I)
        f = open("result", "w")
        f.write(result)
        f.close()
    
from numpy import array, reshape, zeros

def F(U,t):
    Nc = 3
    Nb =4
    h =8
    
    pu = reshape (U, (Nb, Nc, 2))
    r = reshape (U [:, :, 0], (Nb, Nc))
    v = reshape (U [:, :, 1], (Nb, Nc))
    Fs = zeros (2 * Nb * Nc)
    pFs = reshape (Fs, (Nb, Nc, 2))
    drdt = reshape (pFs [:, :, 0], (Nb, Nc))
    dvdt = reshape (pFs [:, :, 1], (Nb, Nc))
    
    for i in range (1, Nb-1):
        for j in range (1, Nc-1):
            drdt [i, j] = v [i, j]
            dvdt [i, j] = (r [i+1, j] - 2 * r [i, j] + r [i-1, j]) / (h ** 2) + (r [i, j+1] - 2 * r [i, j] + r [i, j-1]) / (h ** 2)
from numpy import array, reshape

# ALIAS
V = array ([1, 2, 3])
pV = V  # ALIAS
pV [0] = 4
print (V) 
print (id (V))
print (id (pV)) # Mismo id, son los mismo

# CLONING
V = array ([1, 2, 3])
U = V.copy() # CLONING
U [0] = 4
print (V) 
print (id (V))
print (id (U)) # Diferente id, son diferentes

# ALIAS con reshape
U = array([1, 2, 3, 4])
pU = reshape(U, (2,2)) # Hace un ALIAS, pero es una matriz
pU [0,0] = 8
print(pU)
print(U)
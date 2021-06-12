def lisible(filename, seuil = 35):
    alphabet = "AÀÂBCÇDEÉÈÊËFGHIÎÏÍJKLMNOÔÖPQRSTUÛÙÜVWXYZ"
    f_alphabet = [7.11 ,0.31 ,0.03 ,1.14 ,3.18 ,0.06 ,3.67 ,12.10 ,1.94 ,0.31 ,0.08 ,0.01 ,1.11 ,1.23 ,1.11 ,6.59 ,0.03 ,0.01 ,0.01 ,0.34 ,0.29 ,4.96 ,2.62 ,6.39 ,5.02 ,0.04 ,0.01 ,2.49 ,0.65 ,6.07 ,6.51 ,5.92 ,4.49 ,0.02 ,0.02 ,0.01 ,1.11 ,0.17 ,0.38 ,0.46 ,0.15]
    N = len(alphabet)

    file = open(filename, 'r')
    freq = letter_freq(file, alphabet)
    file.close()

    error = 0

    for i in range(N):
        error += (f_alphabet[i]-freq[i])**2

    return error <= seuil
    
def letter_freq(file, alphabet):
    N = len(alphabet)
    n = 0
    freq = [0 for i in range(N)]
    
    for line in file:
        line = line.upper()
        for char in line:
            i = 0
            while i < N:
                if char == alphabet[i]:
                    freq[i] += 1
                    n += 1
                i += 1

    if n > 0:
        for i in range(N):
            freq[i] *= 100/n
    return freq

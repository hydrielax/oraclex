def lisible(filename, seuil = 0.9, alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "):
    file = open(filename, 'r')

    n = 0
    nChar = 0

    for line in file:
        line = line[:len(line)-2]
        for char in line:
            n += 1
            if char in alphabet:
                nChar += 1

    file.close()

    if n > 0:
        return [(nChar/n) >= seuil, nChar/n]
    else:
        return [False, 0]

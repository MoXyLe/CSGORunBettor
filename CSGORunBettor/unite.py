file1 = open("csgorun\data2.txt", "r")

file2 = open("csgorun\data.txt", "a+")

for i in file1:
    file2.write(i)

file2.close()

file1.close()

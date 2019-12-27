def merge_token_map(file_name_1, file_name_2, output_file_name):
    file1 = open(file_name_1, "r")
    file2 = open(file_name_2, "r")
    outFile = open(output_file_name, "a")
    line1 = file1.readline()
    line2 = file2.readline()
    while line1 != '' and line2 != '':
        word1 = line1.split()
        word2 = line2.split()
        if word1[0] < word2[0]:
            outFile.write(line1)
            line1 = file1.readline()
        elif word1[0] > word2[0]:
            outFile.write(line2)
            line2 = file2.readline()
        else:
            word1 += word2[1:]
            outFile.write(' '.join(word1))
            outFile.write("\n")
            line1 = file1.readline()
            line2 = file2.readline()
    while line1 != "":
        outFile.write(line1)
        line1 = file1.readline()
    while line2 != "":
        outFile.write(line2)
        line2 = file2.readline()


merge_token_map("token_map1.txt", "token_map2.txt", "token_map_merged_12.txt")
merge_token_map("token_map_merged_12.txt", "token_map3.txt", "token_map_fully_merged.txt")


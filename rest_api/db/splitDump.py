#splits the large dump file into smaller ones 

lines_per_file = 50000
smallfile = None
with open('pg_dump.sql',encoding="utf8") as bigfile:
    for lineno, line in enumerate(bigfile):
        
        if lineno % lines_per_file == 0:
            print(lineno)
            if smallfile:
                smallfile.close()
            small_filename = 'splitDump/small_file_{}.txt'.format(lineno + lines_per_file)
            smallfile = open(small_filename, "w+",encoding='utf8')
        smallfile.write(line)
    if smallfile:
        smallfile.close()
# Assembles a large dump file from the small files
#splits the large dump file into smaller ones 

lines_per_file = 50000
smallfile = None
with open('pg_dump.sql',"w+",encoding="utf8") as bigfile:
    while True:
        try:
            print(lines_per_file)
            with open(f"splitDump/small_file_{lines_per_file}.txt","r",encoding="utf8") as sf:
                for line in sf:
                    bigfile.write(line)
            lines_per_file+=50000
        except Exception as e:
            print(e)
            break
        

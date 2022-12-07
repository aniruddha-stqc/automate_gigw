import re
file = open('crawler_output/gospider.txt', 'r')

lines_all = file.readlines()
for line in lines_all:
    url_line = re.search('[url]',line) and re.search('[dahd.nic.in]',line)

    if url_line:
        try:
            print ( re.search("(?P<url>https?://[^\s]+)", line).group("url") )
        except AttributeError:
            pass
        #print(line.strip())

file.close()
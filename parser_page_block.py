import sys
import random
import time
import os.path
import urllib.request


LINK = 'https://www.clalbit.co.il/'
LINK_google = 'http://www.google.com/'
FILE_NAME = 'index.html'


class ReturnPage:

    def __init__(self):
        size = 0
        while size < 6000:
            fp = urllib.request.urlopen(LINK)
            mybytes = fp.read()

            mystr = mybytes.decode("utf8")
            fp.close()
            size = len(mystr)
            if os.path.exists(FILE_NAME):
                os.remove(FILE_NAME)
            with open(FILE_NAME, 'a') as f:
                for line in mystr:
                    try:
                        f.write(line)
                    except:
                        g = ''
            r = random.randint(1, 60)
            print(size)
            time.sleep(r)

def main():
    page = ReturnPage()

if __name__ == '__main__':
    main()

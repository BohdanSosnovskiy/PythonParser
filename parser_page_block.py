import sys
import random
import time
import os.path
import requests
import urllib.request


LINK = 'https://www.clalbit.co.il/'
LINK_google = 'http://www.google.com/'
FILE_NAME = 'index.html'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

class ReturnPage:

    def __init__(self):
        size = 0
        session = requests.Session()
        while size < 6000:
            req = urllib.request.Request(
                LINK,
                data=None,
                headers={
                    'User-Agent': USER_AGENT
                }
            )
            print('load page')
            fp = urllib.request.urlopen(req)
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
            if size < 6000:
                response = session.get(LINK)
                print('Part page')
                print('Headers:')
                print(fp.headers)
                print(session.cookies.get_dict())
            else:
                response = session.get(LINK)
                print('Full page')
                print('Headers:')
                print(fp.headers)
                print(session.cookies.get_dict())
            print(size)


def main():
    page = ReturnPage()

if __name__ == '__main__':
    main()

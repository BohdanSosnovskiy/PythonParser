import requests


def main():
    res = requests.post('http://localhost:5000/new')
    print('response from server:' + res.text)

if __name__ == '__main__':
    main()

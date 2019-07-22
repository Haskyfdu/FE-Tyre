import requests


def flask_test():
    url = 'http://127.0.0.1:9000/run'
    data = '2019-07-05'
    rq = requests.post(url=url, json=data)
    print(rq.text)


if __name__ == '__main__':

    flask_test()
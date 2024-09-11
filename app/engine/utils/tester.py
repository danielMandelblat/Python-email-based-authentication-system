import requests


def send_code():
    url = "http://localhost:1717/start/"
    data = {
        'email': 'daniel.mandelblat1@hp.com'
    }

    result = requests.post(
        url=url,
        data=data
    )

    return {
        'result': result.json(),
        'code': result.status_code,
        'status': result.ok
    }


def auth():
    url = "http://localhost:80/auth/"
    data = {
        'email': 'daniel.mandelblat1@hp.com',
        'code': 'Sw&tRk=u71?uuY5N#H)-Q7(24MXh.f23'
    }

    result = requests.post(
        url=url,
        data=data
    )

    print(result.text)

    return {
        'result': result.json(),
        'code': result.status_code,
        'status': result.ok
    }




if __name__ == "__main__":
    res = send_code()

    print(res)
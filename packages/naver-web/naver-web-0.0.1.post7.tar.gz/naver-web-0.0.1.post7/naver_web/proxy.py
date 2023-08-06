from flask import request, Response
import requests


class Proxy():
    def __init__(self): pass

    def _proxy(self, *args, **kwargs):
        newdomain, newport, = kwargs.get('newdomain'), kwargs.get('newport')
        resp = requests.request(
            method=request.method,
            url=request.url.replace(request.host_url, newdomain + ':' + newport),
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                if name.lower() not in excluded_headers]

        response = Response(resp.content, resp.status_code, headers)
        return response
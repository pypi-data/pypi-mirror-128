from lariat.config import TracerConfig
import zlib
from urllib import request

def _compress(data):
    return zlib.compress(data)

def _make_request(url, data):
    data = data.encode("utf-8")
    req = request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Lariat-Api-Key", TracerConfig.api_key)
    req.add_header("X-Lariat-Application-Key", TracerConfig.application_key)

    resp = request.urlopen(req)

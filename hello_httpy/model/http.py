from __future__ import annotations
from pydantic import BaseModel
from enum import Enum


class HttpHeader(BaseModel):
    pairs: dict

class HttpBody(BaseModel):
    value: str

class RequestMethod(str, Enum):
    get = "get"
    post = "post"
    update = "update"
    delete = "delete"
    patch = "patch"
    put = "put"

class Request:
    def __init__(self, httpHeader: HttpHeader, requestMethod: RequestMethod, httpBody: HttpBody):
        self.httpHeader: HttpHeader = httpHeader
        self.requestMethod: RequestMethod = requestMethod
        self.httpBody: HttpBody = httpBody

    def __repr__(self):
        return f"Request({self.httpHeader}, {self.requestMethod}, {self.httpBody})"
    
    def __str__(self):
        return f"Request({self.httpHeader}, {self.requestMethod}, {self.httpBody})"

    @classmethod
    def createRequestFromByteString(cls, byteString: bytes) -> Request:
        ls = tuple(byteString.decode().split('\r\n'))
        headers = dict()

        for pair in ls[1:-1]:
            if not pair:
                continue
            key, value = pair.split(':', maxsplit=1)
            headers[key.strip()] = value.strip()

        httpHeader = HttpHeader(pairs=headers)
        httpBody = HttpBody(value=ls[-1])

        return Request(httpHeader, ls[0].split()[0].lower(), httpBody)


class Response:
    def __init__(self):
        self.httpHeader: HttpHeader | None = None
        self.statusCode: int = 0
        self.httpBody: HttpBody | None = None
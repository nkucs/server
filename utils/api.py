import json
import logging
from collections import OrderedDict

from django.core.files import File
from django.http import HttpResponse, QueryDict, FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView as RestfulAPIView

logger = logging.getLogger("")


class APIError(Exception):
    def __init__(self, msg, err=None):
        self.err = err
        self.msg = msg
        super().__init__(err, msg)


class ContentType(object):
    json_request = "application/json"
    json_response = "application/json;charset=UTF-8"
    url_encoded_request = "application/x-www-form-urlencoded"
    binary_response = "application/octet-stream"


class JSONParser(object):
    content_type = ContentType.json_request

    @staticmethod
    def parse(body):
        return json.loads(body.decode("utf-8"))


class URLEncodedParser(object):
    content_type = ContentType.url_encoded_request

    @staticmethod
    def parse(body):
        return QueryDict(body)


class JSONResponse(object):
    content_type = ContentType.json_response

    @classmethod
    def response(cls, data):
        resp = HttpResponse(json.dumps(data, indent=4), content_type=cls.content_type)
        resp.data = data
        return resp


class FILEResponse(object):

    @classmethod
    def response(cls, data):
        if isinstance(data, File):
            resp = FileResponse(data, as_attachment=True)
        else:
            resp = JSONResponse.response(data)
        return resp


class APIView(RestfulAPIView):
    """
    Django view的父类, 和django-rest-framework的用法基本一致
     - request.data获取解析之后的json或者urlencoded数据, dict类型
     - self.success, self.error和self.invalid_serializer可以根据业需求修改,
        写到父类中是为了不同的人开发写法统一,不再使用自己的success/error格式
     - self.response 返回一个django HttpResponse, 具体在self.response_class中实现
     - parse请求的类需要定义在request_parser中, 目前只支持json和urlencoded的类型, 用来解析请求的数据
    """

    @staticmethod
    def success(data=None):
        return Response({"error": None, "data": data})

    @staticmethod
    def error(msg="error", err="error"):
        return Response({"error": err, "data": msg})

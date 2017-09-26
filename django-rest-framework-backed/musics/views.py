# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from musics.models import Music
from musics.serializers import MusicSerializer
import json


# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    # permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    # [GET] /api/music/{pk}/detail/
    @detail_route(methods=['get'])
    def detail(self, request, pk=None):
        music = get_object_or_404(Music, pk=pk)
        result = {
            'singer': music.singer,
            'song': music.song
        }
        response = HttpResponse(json.dumps(result))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    # [GET] /api/music/all_singer/
    @list_route(methods=['get'])
    def all_singer(self, request):
        result = 'callback' + "(" + json.dumps({"key": "value", "key2": "value"}) + ")"
        response = HttpResponse(result)
        return response

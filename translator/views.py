from django.http import HttpResponse, JsonResponse
import json

from translator.linggletranslate import spg_translate
# Create your views here.


def translate_json_view(request):
    if request.method == 'GET':
        return HttpResponse(status=404)
    elif request.method == 'POST':
        request_body = json.loads(request.body)
        return JsonResponse(spg_translate(request_body['text']))

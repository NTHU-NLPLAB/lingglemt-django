from django.http import HttpResponse, JsonResponse
import json

from lingglemt.linggletranslate import spg_translate
# Create your views here.


def translate_json_view(request):
    if request.method == 'GET':
        return HttpResponse(status=404)
    elif request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        request_body = json.loads(body_unicode)
        return JsonResponse(spg_translate(request_body['text']))

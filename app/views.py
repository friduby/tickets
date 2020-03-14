from django.http import JsonResponse
import requests
import json
from .models import Global

def get_prices(request):
    g = Global.get()
    response = json.loads(requests.post('http://localhost:8081/start_procedure', data={
            'args': json.dumps({
                'callback_url': 'http://localhost:8000/callback',
            }),
            'ref_code': str(g.counter),
            'procedure_id': 6
        }).text)
    g.counter += 1
    g.save()
    return JsonResponse({"status": response['status']})


def callback(request):
    body_unicode = request.body.decode("utf-8")
    print (json.loads(request.POST.get('variables'))['tickets'][0])
    print ('callback is ', body_unicode)
    return JsonResponse({"status": True})
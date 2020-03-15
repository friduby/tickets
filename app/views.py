from django.http import JsonResponse
import requests
import json
from .models import Global, Request

def get_prices(request):
    g = Request.objects.create()
    response = json.loads(requests.post('http://localhost:8081/start_procedure', data={
            'args': json.dumps({
                'callback_url': 'http://localhost:8000/callback',
                'source': request.GET.get('source'),
                'target': request.GET.get('target'),
                'adult': request.GET.get('adult'),
                'date': request.GET.get('date')
            }),
            'ref_code': 'req'+str(g.pk),
            'procedure_id': 1
        }).text)
    response = json.loads(requests.post('http://localhost:8081/start_procedure', data={
            'args': json.dumps({
                'callback_url': 'http://localhost:8000/callback',
            }),
            'ref_code': 'req'+str(g.pk),
            'procedure_id': 2
        }).text)
    return JsonResponse({"status": response['status']})

def find_ticket_in_list(ticket, ls):
    c = 0
    for i in ls:
        if i['class'] == ticket['class'] and i['time'] == ticket['time']:
            return c
        c += 1
    return -1

def callback(request):
    body_unicode = request.body.decode("utf-8")
    r = Request.objects.get(pk=request.POST.get('ref_code')[3:])
    for i in range(1, 4):
        if getattr(r, 'data{}'.format(i)) is None:
            setattr(r, 'data{}'.format(i), request.POST.get('variables'))

            if i == 2:
                result = []
                for t in json.loads(r.data1)['tickets']+json.loads(r.data2)['tickets']+json.loads(r.data3)['tickets']:
                    t['class'] = t['class'].split()[-1]
                    ind = find_ticket_in_list(t, result)
                    if ind != -1:
                        if result[ind]['price'] > t['price']:
                            del result[ind]
                            result.append(t)
                    else:
                        result.append(t)
                
                print ('#RESULT ', result)
            break
    r.save()
    return JsonResponse({"status": True})
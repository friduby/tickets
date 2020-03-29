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
                 'source': request.GET.get('source'),
                'target': request.GET.get('target'),
                'adult': request.GET.get('adult'),
                'date': request.GET.get('date')
            }),
            'ref_code': 'rek'+str(g.pk),
            'procedure_id': 2
        }).text)
    with open('app/static/{}.txt'.format(g.pk), 'a') as f:
        f.write(json.dumps({
                 'source': request.GET.get('source'),
                'target': request.GET.get('target'),
                'adult': request.GET.get('adult'),
                'date': request.GET.get('date')
            }) + "\n")
    return JsonResponse({"status": response['status'], "id": g.pk})

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
                for t in json.loads(r.data1)['tickets']+json.loads(r.data2)['tickets']:
                    t['class'] = t['class'].split()[-1]
                    ind = find_ticket_in_list(t, result)
                    if ind != -1:
                        if result[ind]['price'] > t['price']:
                            del result[ind]
                            result.append(t)
                    else:
                        result.append(t)
                
                print ('#RESULT ', result)
                r.data3 = json.dumps(sorted(result, key=lambda x: x['price'])[-1])
            break
    
    with open('app/static/{}.txt'.format(r.pk), 'a') as f:
        f.write('\n'.join([r.data1, r.data2, r.data3]))
    r.save()
    return JsonResponse({"status": True})
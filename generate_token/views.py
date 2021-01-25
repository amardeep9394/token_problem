from django.shortcuts import render
from django.http import JsonResponse
from generate_token.models import TokenModel
from django.core import serializers
from django.http import HttpResponse
from django.http import Http404
import uuid 
import json
from django.db.models.aggregates import Count
from random import randint
# Create your views here.
def unique_token(request):
    token_value = uuid.uuid4()
    token_object = TokenModel(token = str(token_value), assign = 'free') 
    token_object.save()
    qs = TokenModel.objects.all()
    data = serializers.serialize('json', qs, fields=('token', 'assign'))
    data = json.dumps(json.loads(data), indent=4)
    return HttpResponse(data, content_type='application/json')

def assign_token(request,username):
    
    if TokenModel.objects.filter(assigned_to=username).exists():
        qs = TokenModel.objects.filter(assigned_to=username)
        data = serializers.serialize('json', qs, fields=('token', 'assign','assigned_to'))
        data = json.dumps(json.loads(data), indent=4)
        return HttpResponse(data, content_type='application/json')
    else:
        token_set = TokenModel.objects.exclude(assign='blocked').values_list('id', flat=True)
        print(len(token_set))
        if len(token_set)>0:
            TokenModel.objects.filter(id=token_set[0]).update(assign='blocked',assigned_to=username)
            qs = TokenModel.objects.filter(assigned_to=username)
            data = serializers.serialize('json', qs, fields=('token', 'assign','assigned_to'))
            data = json.dumps(json.loads(data), indent=4)
            
            return HttpResponse(data, content_type='application/json')
        else:
            return render(request,'404.html')


def unblock_token(request,username):
    print("hi")
    if TokenModel.objects.filter(assigned_to=username).exists():
        print("here")
        TokenModel.objects.filter(assigned_to=username).update(assign='free',assigned_to='')
    qs = TokenModel.objects.all()
    data = serializers.serialize('json', qs, fields=('token', 'assign','assigned_to'))
    data = json.dumps(json.loads(data), indent=4)
    return HttpResponse(data, content_type='application/json')

def delete_token(request,username):
    print("hi")
    if TokenModel.objects.filter(assigned_to=username).exists():
        print("here")
        TokenModel.objects.filter(assigned_to=username).delete()
    qs = TokenModel.objects.all()
    data = serializers.serialize('json', qs, fields=('token', 'assign','assigned_to'))
    data = json.dumps(json.loads(data), indent=4)
    return HttpResponse(data, content_type='application/json')
            
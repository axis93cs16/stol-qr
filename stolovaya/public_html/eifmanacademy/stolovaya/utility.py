# coding=utf-8
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from stolovaya.models import stolovaya as modelstol
from stolovaya.models import stolovayainfodata, stolovayainfopit, stolovayapodacha, stolovayatalon, stolovayacategory, get_typesofeda,get_typesofinternat, stolovayapriemipishi, stolovayamedflag, stolovayainfopitafter, stolovayafactstol
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, HttpResponse, render
from datetime import datetime



# views.py
from rest_framework import viewsets, permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response


class api_gb_stol_show(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    def get(self, request):
        #redirect_url = reverse('stolovaya:index')
        #redirect_url = reverse('indexpage', args=(backend,))
        #parameters = urlencode(form.cleaned_data)
        #return redirect(f'{redirect_url}?{parameters}')
        return redirect(reverse('stolovaya:index'))
        #return Response({"Error": "forbidden"})
    def post(self, request):
        user = request.user
        if user:
            queryset = modelstol.objects.all().values()
            #queryset2 = stolovayainfodata.objects.all().values()
            #queryset3 = stolovayainfopit.objects.all().values()
            #queryset4 = stolovayacategory.objects.all().values()
            #queryset5 = stolovayamedflag.objects.all().values()
            return Response({'stolovaya':queryset,
                #'stolovayainfodata':queryset2,
                #'stolovayainfopit':queryset3,
                #'stolovayainfocategory':queryset4,
                #'stolovayamedflag':queryset5,
                })
    def put(self, request, pk):
        return Response({"success": "Updated successfully"})
    pass

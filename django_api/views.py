from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView



class HelloView(APIView):
    def get(self, request):
        return Response({'hello': 'world'})
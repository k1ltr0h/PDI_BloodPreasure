from rest_framework.response import Response
from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.views import APIView

# Create your views here.

class Upload(APIView):
    def post(self, request):
        file = request.FILES['video']
        file_name = default_storage.save('data/'+file.name, file)


        return Response({'status': 'success',
                        'DIA': 120.34,
                        'SYS': 90.23,
                        })
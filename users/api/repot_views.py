import base64
from rest_framework.views import APIView
from typing import Literal, Optional
from decimal import Decimal
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from users.models import ReportModel
from users.serializers.report_serializers import ReportUploadSerializer

class ReportUploadAPIView(APIView):
    # parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        print(request.data.get('report_file'))
        req_data = request.data.get('report_file')
        format, imgstr = req_data.split(';base64,') 
        ext = format.split('/')[-1] 
        cont_data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
       
        try:
          email = request.data.get('email')
          user = ReportModel.objects.get(email=email)
        except ReportModel.DoesNotExist:
            return Response({'error': 'User not found with the provided email.'}, status=status.HTTP_404_NOT_FOUND)
        
        # data = {'user': user.id, 'report_file': request.data.get('report_file')}
        data = {'user': user.id, 'report_file': cont_data}

        file_serializer = ReportUploadSerializer(data=data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("file_serializer.errors,", status=status.HTTP_201_CREATED)

from typing import TypedDict, Union

class SkillInfo(TypedDict):
    text: str
    result: str
    education_score: Union[float, None]
    language_score: Union[float, None]
    special_skills_score: Union[float, None]
    sport_score: Union[float, None]
    work_experiance_score: Union[float, None]
    program_score: Union[float, None]


class ReportInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        rep = ReportModel.objects.select_related('user').filter(user__email='tami@mail.ru').defer('report_file').values()
        data: TypedDict[str, SkillInfo] = {'education':{'text': 'Education', 'result':''}, 
                'language': {'text': 'Language skills', 'result':''},
                'special': {'text': 'Special talent', 'result':''},
                'sport': {'text': 'Sport skills', 'result':''},
                'work': {'text': 'Work experience', 'result':''},
                'program': {'text': 'Program skills', 'result':''}}
        rep_data = rep[0]

        for key, value in rep_data.items():
            for d_key, d_value in data.items():
                if d_key in key:
                    if isinstance(value, Decimal):
                        float_value = float(value)
                        result = ''
                        if 1 <= float_value <= 20:
                            result = 'limited'
                        elif 21 <= float_value <= 40:
                            result = 'decent'
                        elif 41 <= float_value <= 60:
                            result = 'moderate'
                        elif 61 <= float_value <= 80:
                            result = 'solid'
                        elif 81 <= float_value <= 100:
                            result = 'extensive'
                        d_value[key] = float_value
                        d_value['result'] = result
                    else:
                        d_value[key] = value
            
        return Response({"data":data}, status=status.HTTP_200_OK)

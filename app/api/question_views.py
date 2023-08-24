#from django.db.models import Prefetch
from django.db.models import Q
from django.http import JsonResponse
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import Question
from app.serializers import QuestionListSerializer

class QuestionListApiView(APIView): 

    def get(self, request):
        question = Question.objects.prefetch_related('answers')

        serializer =  QuestionListSerializer(question, many = True)

        return Response({"questions": serializer.data})
    
class GetQuestionApiView(APIView):
    def get(self, request, language, level):
        query = Q()
        for index in request.data['data']:
            query.add(Q(question_dependens_on_answer=index), Q.OR)

        questions = Question.objects.filter(query).values("id", "question_title", "question_type")
        question_list = [question for question in questions]
        return JsonResponse({"questions": question_list})
   
    
class AddQuestionApiView(APIView):
    def post(self, request):        
        cache.set("user_info", request.data, 24*3600) #TODO: add user email ass cache key
        if cache.get("user_info") is not None:
            return Response({
                'data': cache.get("user_info", status=status.HTTP_200_OK),
            })
        return Response("Problem", status=status.HTTP_400_BAD_REQUEST)

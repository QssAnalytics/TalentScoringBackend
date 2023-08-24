from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from app.models import Answer

# class GetAnswerWeight(APIView):
#     def get(self, request, language, level):
#         user = "tami@mail.ru" #TODO: chacge request user email
#         redis_language = language.replace(" ", "_")
#         redis_level = level.replace(" ", "_")
#         key = f"{user}_{redis_language}_{redis_level}"
#         if cache.get(key) is not None:
#            return Response(cache.get(key), status=status.HTTP_200_OK)
        
#         answer = Answer.objects.filter(answer_title=language).first()
#         if answer != None:
#           if answer.answer_weight_store.get(level) is not None:
#             key = f"{user}_{redis_language}_{redis_level}"
#             cache.set(key, answer.answer_weight_store[level], 120)
#             return Response(answer.answer_weight_store[level], status=status.HTTP_200_OK)
          
#           return Response("Language level is wrong", status=status.HTTP_404_NOT_FOUND)
        
#         return Response("Data is wrong", status=status.HTTP_404_NOT_FOUND)
    
class GetAnswerWeight(APIView):
    def get(self, request, language, level):  
        answer = Answer.objects.filter(answer_title=language).first()
        if answer != None:
          if answer.answer_weight_store.get(level) is not None:
            return Response(answer.answer_weight_store[level], status=status.HTTP_200_OK)
          
          return Response("Language level is wrong", status=status.HTTP_404_NOT_FOUND)
        
        return Response("Data is wrong", status=status.HTTP_404_NOT_FOUND)
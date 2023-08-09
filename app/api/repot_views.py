from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from app.models import UserAccount
from app.serializers.report_serializers import ReportUploadSerializer

class ReportUploadAPIView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        try:
          email = request.data.get('email')
          user = UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found with the provided email.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {'user': user.id, 'report_file': request.data.get('report_file')}
        file_serializer = ReportUploadSerializer(data=data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
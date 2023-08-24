# from app.models import UserProfile
from rest_framework import serializers

from users.models import ReportModel

class ReportUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = "__all__"
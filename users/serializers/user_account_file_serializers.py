from rest_framework import serializers

from users.models import UserAccountFilePage

# class ReportUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ReportModel
#         fields = "__all__"

class UserAccountFilePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountFilePage
        fields = ("user", "file", "file_category")
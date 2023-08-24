from rest_framework import serializers
from users.models import UserAccount, CertificateModel
class CertificateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateModel
        fields = ['user', 'cert_file', 'cert_unique_key', 'date_created']
    
    # def validate_cert_file(self, value):
    #     # Check if the uploaded file is a PDF
    #     if not value.name.lower().endswith('.pdf'):
    #         raise serializers.ValidationError("Only PDF files are allowed.")

    #     return value
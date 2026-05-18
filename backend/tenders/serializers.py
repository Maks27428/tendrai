from rest_framework import serializers
from .models import Tender, Requirement


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['id', 'text', 'category', 'status', 'details', 'order']


class TenderListSerializer(serializers.ModelSerializer):
    requirements_count = serializers.IntegerField(source='requirements.count', read_only=True)

    class Meta:
        model = Tender
        fields = ['id', 'title', 'status', 'risk_score', 'page_count', 'summary', 'requirements_count', 'created_at']


class TenderDetailSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, read_only=True)

    class Meta:
        model = Tender
        fields = [
            'id', 'title', 'status', 'progress_message',
            'page_count', 'summary', 'risk_score', 'risk_explanation',
            'pitfalls', 'technical_proposal', 'requirements',
            'created_at', 'updated_at',
        ]


class TenderUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id', 'pdf_file']

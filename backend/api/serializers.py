from rest_framework import serializers
from .models import Application
from django.contrib.auth.models import User


class ApplicationSerializer(serializers.ModelSerializer):
    cv_url = serializers.SerializerMethodField()
    # Explicitly mark as optional
    cv = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'company_name', 'job_title',
            'application_date', 'status', 'cv', 'cv_url',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'cv_url', 'user']

    def get_cv_url(self, obj):
        request = self.context.get('request')
        if obj.cv and request:
            return request.build_absolute_uri(obj.cv.url)
        return None

    def validate_cv(self, value):
        if value:
            # Validate file size (e.g., max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if value.size > max_size:
                raise serializers.ValidationError("File size exceeds 5MB.")
            # Validate file type (only PDF allowed)
            if not value.name.endswith('.pdf'):
                raise serializers.ValidationError(
                    "Invalid file type. Only PDF files are allowed.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

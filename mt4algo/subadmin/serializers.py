from rest_framework import serializers
from .models import sub_adminDT, Subadmin_client_limit

# Serializer for Subadmin_client_limit
class SubadminClientLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subadmin_client_limit
        fields = '__all__'

# Serializer for sub_adminDT
class SubAdminDTSerializer(serializers.ModelSerializer):
    subadmin_client_limit = SubadminClientLimitSerializer(read_only=True)  # Nested serializer

    class Meta:
        model = sub_adminDT
        fields = '__all__'

    # Ensure unique subadmin_id is generated if missing
    def create(self, validated_data):
        instance = sub_adminDT(**validated_data)
        if not instance.subadmin_id:
            instance.subadmin_id = instance.generate_unique_id()
        instance.save()
        return instance

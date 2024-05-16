
from rest_framework import serializers
from literals.models import University


class ListAllLiteralsSerializer(serializers.Serializer):
    lead_types = serializers.SerializerMethodField()

    def get_universities(self, obj: University):
        return University.objects.values()

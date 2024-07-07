from django.forms.models import model_to_dict
from literals.api_docs import HOSTELS_SWAGGER_DOCS
from literals.models import Hostel
from literals.serializers import ListAllLiteralsSerializer
from literals.serializers import UnauthenticatedLiteralsSerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ListLiteralsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ListAllLiteralsSerializer(context={"request": request}, data={})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


class UnauthenticatedListLiteralsView(APIView):
    def get(self, request):
        serializer = UnauthenticatedLiteralsSerializer(
            context={"request": request}, data={}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


class HostelApiView(APIView):
    @HOSTELS_SWAGGER_DOCS
    def get(self, request, code):
        if not code:
            raise serializers.ValidationError(
                code="hostel_code", detail="please provide hostel  code"
            )
        instance = Hostel.objects.filter(code=code).first()

        response = model_to_dict(instance) if instance else {}

        return Response(response, status=status.HTTP_200_OK)

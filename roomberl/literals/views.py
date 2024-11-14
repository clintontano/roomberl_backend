from literals.filters import HostelFilter
from literals.models import Hostel
from literals.serializers import HostelSerializer
from literals.serializers import ListAllLiteralsSerializer
from literals.serializers import UnauthenticatedLiteralsSerializer
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
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


class HostelApiView(ListAPIView, RetrieveAPIView):
    serializer_class = HostelSerializer
    queryset = Hostel.objects.order_by("created_at")
    lookup_field = "code"
    filterset_class = HostelFilter

# Create your views here.
from question.models import Category
from question.serializers import CategorySerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class CategoryApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.order_by("-updated_at")
    pagination_class = None

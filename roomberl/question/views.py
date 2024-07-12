# Create your views here.
from question.models import Category
from question.serializers import CategorySerializer
from rest_framework.generics import ListAPIView


class CategoryApiView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.order_by("created_at")
    pagination_class = None

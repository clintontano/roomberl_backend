# Create your views here.
from comments.models import Comment
from comments.serializers import CreateCommentSerializer
from comments.serializers import GetCommetsSerialiser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class CommentApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method != "GET":
            return CreateCommentSerializer

        return GetCommetsSerialiser

    def get_object(self):
        object_id = self.request.parser_context.get("kwargs").get("pk")

        commets = Comment.objects.filter(object_id=object_id).first()

        return commets

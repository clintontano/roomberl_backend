# Create your tests here.
from accounts.factories import UserFactory
from comments.factory import CommentFactory
from comments.models import Comment
from company.factories import CompanyFactory
from django.urls import reverse
from emission_factors.factories import PurchasedCoolingEmissionFactor
from entity.factories import EntityFactory
from rest_framework import status
from testing.base import BaseAPITest


class CommentAPITestCase(BaseAPITest):
    def setUp(self):
        self.user = UserFactory()

        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.entity = EntityFactory()
        self.company = CompanyFactory()

    def test_create_comment_api(self):
        data = {
            "object_id": PurchasedCoolingEmissionFactor().id,
            "object_type": Comment.OBJECT_TYPE.EMISSION_FACTOR,
            "content": "First comment",
        }
        url = reverse("comments:comments-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_comment_api(self):
        #  Given a company
        CommentFactory()
        CommentFactory()

        url = reverse("comments:comments-list")

        # WHEN I call the list API
        response = self.client.get(url)

        # THEN I should see the company in the list
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_update_company_api(self):
        # Given a company
        comment = CommentFactory()
        updated_data = {"object_type": Comment.OBJECT_TYPE.EMISSION_SOURCE_RECORD}

        # WHEN I call the update API
        url = reverse("comments:comments-detail", kwargs={"pk": comment.object_id})
        response = self.client.patch(url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.object_type, updated_data["object_type"])

    def test_delete_company_api(self):
        comment: Comment = CommentFactory()
        url = reverse("comments:comments-detail", kwargs={"pk": comment.object_id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

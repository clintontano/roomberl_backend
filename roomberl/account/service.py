from account.models import UserAdditionalDetail
from crum import get_current_request
from rest_framework.request import Request


class AccountService:
    def calculate_match_percentage(self, user1_responses, user2_responses):
        total_questions = 0
        matching_answers = 0

        user2_responses_dict = {
            category["id"]: {
                question["id"]: {
                    option.get("text", option.get("id", ""))
                    for option in question["option"]
                    if option["chosen"]
                }
                for question in category["question"]
            }
            for category in user2_responses
        }

        for category in user1_responses:
            category_id = category["id"]
            if category_id in user2_responses_dict:
                for question in category["question"]:
                    question_id = question["id"]
                    if question_id in user2_responses_dict[category_id]:
                        user1_answers = {
                            option.get("text", option.get("id", ""))
                            for option in question["option"]
                            if option["chosen"]
                        }
                        user2_answers = user2_responses_dict[category_id][question_id]
                        total_questions += 1
                        if user1_answers == user2_answers:
                            matching_answers += 1

        if total_questions == 0:
            return 0
        return (matching_answers / total_questions) * 100

    def get_match_percentage(self, obj: UserAdditionalDetail) -> UserAdditionalDetail:
        request: Request = get_current_request()

        if not request.user:
            return "0%"

        logged_in_user_detail = UserAdditionalDetail.objects.filter(
            user=request.user
        ).first()

        if (
            not logged_in_user_detail
            or not logged_in_user_detail.responses
            or not obj.responses
        ):
            return "0%"

        match_percentage = self.calculate_match_percentage(
            logged_in_user_detail.responses, obj.responses
        )
        return f"{match_percentage:.1f}%"

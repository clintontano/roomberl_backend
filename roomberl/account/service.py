from account.models import User


def extract_chosen_options(responses):
    chosen_options = set()
    for category in responses.get("categories", []):
        for question in category.get("questions", []):
            for option in question.get("options", []):
                if option.get("chosen"):
                    chosen_options.add(option.get("id"))
    return chosen_options


def find_matching_users():
    all_users = User.objects.exclude(useradditionaldetail__isnull=True)
    matching_users_dict = {}

    for user in all_users:
        user: User
        if hasattr(user, "useradditionaldetail"):
            user_responses = user.useradditionaldetail.responses
            user_chosen_options = extract_chosen_options(user_responses)
            matching_users_dict[user.id] = {"user": user, "matches": []}

            for other_user in all_users:
                other_user: User
                if other_user.id != user.id and hasattr(
                    other_user, "useradditionaldetail"
                ):
                    other_user_responses = other_user.useradditionaldetail.responses
                    other_user_chosen_options = extract_chosen_options(
                        other_user_responses
                    )

                    if user_chosen_options.intersection(other_user_chosen_options):
                        matching_users_dict[user.id]["matches"].append(other_user)

    return matching_users_dict

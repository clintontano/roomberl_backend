from account.models import User
from django.http import Http404


def extract_chosen_options(responses):
    chosen_options = set()
    for category in responses.get("categories", []):
        for question in category.get("questions", []):
            for option in question.get("options", []):
                if option.get("chosen"):
                    chosen_options.add(option.get("id"))
    return chosen_options


def find_matching_users(current_user: User, hostel):
    all_users: User = User.objects.filter(
        useradditionaldetail__isnull=False, hostel=hostel
    ).select_related("useradditionaldetail")

    if (
        not hasattr(current_user, "useradditionaldetail")
        or current_user.useradditionaldetail is None
    ):
        raise Http404("%s does not have additional detail" % current_user)

    current_user_responses = current_user.useradditionaldetail.responses
    current_user_chosen_options = extract_chosen_options(current_user_responses)

    user_chosen_options_map = {}
    for user in all_users:
        user: User
        user_responses = user.useradditionaldetail.responses
        user_chosen_options = extract_chosen_options(user_responses)
        user_chosen_options_map[user.id] = user_chosen_options

    matching_users_dict = {}
    for user in all_users:
        if user.id == current_user.id:
            continue  # Skip comparing current_user with themselves

        user_chosen_options = user_chosen_options_map[user.id]
        if current_user_chosen_options.intersection(user_chosen_options):
            matching_users_dict[user.id] = {"user": user, "matches": []}

    return matching_users_dict

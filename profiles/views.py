from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import json

from .selectors import get_profile_by_user_id


@api_view(["GET"])
def profile_status_detail(request, user_id):
    profile = get_profile_by_user_id(user_id)

    return HttpResponse(json.dumps(profile.status), content_type="application/json")

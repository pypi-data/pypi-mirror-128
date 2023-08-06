from http import HTTPStatus

from django.shortcuts import render
from lotide_luna.utils import (authenticated_request, handle_error,
                               prepare_context)


def user(request, user_id, page=None):
    """View user and their posts."""
    context = prepare_context(request)
    user_response = authenticated_request(request, 'GET', f'/users/{user_id}')
    if user_response.status_code != HTTPStatus.OK:
        return handle_error(user_response)
    timeline_url = f'/users/{user_id}/things'
    if page is not None:
        timeline_url += f'&page={page}'
    timeline_response = authenticated_request(request, 'GET', timeline_url)
    if timeline_response.status_code != HTTPStatus.OK:
        return handle_error(timeline_response)
    context['user'] = user_response.json()
    timeline_json = timeline_response.json()
    context['items'] = timeline_json['items']
    context['next_page'] = timeline_json['next_page']
    context['timeline_type'] = 'user',
    return render(request, 'user.html', context)

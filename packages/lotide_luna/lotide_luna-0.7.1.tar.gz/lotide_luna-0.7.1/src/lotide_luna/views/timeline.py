from http import HTTPStatus

from django.shortcuts import redirect, render
from lotide_luna.utils import (authenticated_request, get_minimal_post,
                               handle_error, prepare_context)


def index(request):
    """Return default feed: all posts."""
    instance = request.COOKIES.get('instance')
    context = prepare_context(request)
    if instance is None:
        return render(request, 'index.html', context)
    return redirect('timeline', 'home')


def timeline(request, timeline_type='all', page=None):
    """View timeline of posts.

    timeline_type: string
        `all`: all posts from local and connected instances
        `local`: only posts from local instance
        `home`: posts from communities the user follow

    page: string
        the page ID assigned by lotide
    """
    context = prepare_context(request)
    endpoint = '/posts?limit=20'
    if timeline_type == 'local':
        endpoint += '&in_any_local_community=true'
    elif timeline_type == 'home':
        endpoint += '&include_your_follow=true'
    if page is not None:
        endpoint += f'&page={page}'
    response = authenticated_request(request, 'GET', endpoint)
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    json = response.json()
    context['posts'] = [get_minimal_post(post) for post in json['items']]
    context['timeline_type'] = timeline_type
    context['next_page'] = json['next_page']
    return render(
        request, 'timeline.html', context)

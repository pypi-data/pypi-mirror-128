from http import HTTPStatus

from django.shortcuts import render
from lotide_luna.utils import (authenticated_request, get_minimal_post,
                               handle_error, prepare_context)


def list_communities(request):
    """View list of communities."""
    context = prepare_context(request)
    response = authenticated_request(request, 'GET', '/communities')
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    communities = response.json()['items']
    context['local'] = [community for community in communities
                        if community['local']]
    context['remote'] = [community for community in communities
                         if not community['local']]
    return render(request, 'communities.html', context)


def community(request, community_id, page=None):
    """View community and its posts."""
    context = prepare_context(request)
    community_response = authenticated_request(
        request, 'GET', f'/communities/{community_id}')
    if community_response.status_code != HTTPStatus.OK:
        return handle_error(community_response)
    timeline_url = f'/posts/?community={community_id}'
    if page is not None:
        timeline_url += f'&page={page}'
    timeline_response = authenticated_request(request, 'GET', timeline_url)
    if timeline_response.status_code != HTTPStatus.OK:
        return handle_error(timeline_response)

    json = timeline_response.json()
    context['community'] = community_response.json()
    context['posts'] = [get_minimal_post(post) for post in json['items']]
    context['timeline_type'] = 'community',
    context['next_page'] = json['next_page']

    return render(request, 'community.html', context)

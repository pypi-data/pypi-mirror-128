from http import HTTPStatus
from json import loads

from django.shortcuts import redirect, render
from lotide_luna.utils import (authenticated_request, handle_error,
                               prepare_context)


def post(request, post_id):
    """View post and its comment."""
    context = prepare_context(request)
    post_response = authenticated_request(request, 'GET', f'/posts/{post_id}')
    if post_response.status_code != HTTPStatus.OK:
        return handle_error(post_response)
    comment_response = authenticated_request(
        request, 'get', f'/posts/{post_id}/replies')
    if comment_response.status_code != HTTPStatus.OK:
        return handle_error(comment_response)
    comment_json = comment_response.json()
    context['post'] = post_response.json()
    context['comments'] = comment_json['items']
    context['next_page'] = comment_json['next_page']
    return render(request, 'post.html', context)


def new_post(request, community_id):
    context = prepare_context(request)
    context['community_id'] = community_id
    if request.method == 'GET':
        return render(request, 'new-post.html', context)
    content = request.POST['content-type']
    payload = {
        'community': community_id,
        'title': request.POST['title'],
        content: request.POST['text'],
    }
    url = request.POST['url']
    if url is not None and url != '':
        payload['href'] = url
    # TODO: allow uploading media
    response = authenticated_request(request, 'POST', '/posts', json=payload)
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    post_id = loads(response.content)['id']
    return redirect('post', post_id)

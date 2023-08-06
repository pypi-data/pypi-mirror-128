from http import HTTPStatus
from json import loads

from django.shortcuts import redirect, render
from lotide_luna.utils import (authenticated_request, handle_error,
                               prepare_context)


def create_comment(request, post_id):
    """Create a new comment; only POST request."""
    if request.method != 'POST':
        return HttpResponse(
            'Method not allowed', status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    context = prepare_context(request)
    context['post_id'] = post_id
    content = request.POST['content-type']
    # TODO: Implement uploading media
    payload = {
        content: request.POST['comment'],
    }
    response = authenticated_request(
        request, 'POST', f'/posts/{post_id}/replies', json=payload)
    if response.status_code != HTTPStatus.OK:
        # TODO: It should be CREATED, talk with lotide dev
        return handle_error(response)
    return redirect('post', post_id)


def reply_comment(request, post_id, comment_id):
    """Create a new comment replying to comment; only POST request."""
    if request.method != 'POST':
        return HttpResponse(
            'Method not allowed', status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    context = prepare_context(request)
    context['comment_id'] = comment_id
    content = request.POST['content-type']
    # TODO: Implement uploading media
    payload = {
        content: request.POST['comment'],
    }
    response = authenticated_request(
        request, 'POST', f'/comments/{comment_id}/replies', json=payload)
    if response.status_code != HTTPStatus.OK:
        # TODO: It should be CREATED, talk with lotide dev
        return handle_error(response)
    return redirect('post', post_id)

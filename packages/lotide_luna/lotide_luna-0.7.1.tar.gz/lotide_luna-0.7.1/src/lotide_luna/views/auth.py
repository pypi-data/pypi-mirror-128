from django.shortcuts import redirect, render
from lotide_luna.utils import authenticated_request


def login(request):
    """View for login form."""
    theme = request.COOKIES.get('luna-theme', 'auto')
    if request.method == 'GET':
        request.session.set_test_cookie()
        return render(request, 'login.html', {'luna_theme': theme})
    username = request.POST['username']
    instance = request.POST['instance']
    password = request.POST['password']
    payload = {
        'username': username,
        'password': password
    }
    response = authenticated_request(request, 'POST', '/logins',
                                     instance=instance, json=payload)
    json = response.json()
    cookies = {
        'username': username,
        'instance': instance,
        'token': json['token'],
        'user_id': json['user']['id'],
        'is_site_admin': json['user']['is_site_admin'],
        'has_unread_notifications': json['user']['has_unread_notifications']
    }
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = redirect('index')
        for k, v in cookies.items():
            response.set_cookie(k, v, secure=True, httponly=True, samesite='Strict')
        return response
    else:
        return render('error/no_cookie.html')


def logout(request):
    """Log out endpoint."""
    response = authenticated_request(request, 'DELETE', '/logins/~current')
    response = redirect('index')
    cookies = [
        'username',
        'instance',
        'token',
        'user_id',
        'is_site_admin',
        'has_unread_notifications'
    ]
    for cookie in cookies:
        response.delete_cookie(cookie)
    return response

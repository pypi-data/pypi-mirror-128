from django.shortcuts import redirect, render
from lotide_luna.utils import prepare_context


def settings(request):
    """Setting client preferences."""
    context = prepare_context(request)
    if request.method == 'GET':
        return render(request, 'settings.html', context)
    theme = request.POST['theme']
    response = redirect('settings')
    response.set_cookie('luna-theme', theme, secure=True, httponly=True, samesite='Strict')
    return response

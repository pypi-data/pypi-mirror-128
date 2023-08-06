from django.urls import path

from . import views

urlpatterns = [
    # Timeline
    path('', views.index, name='index'),
    path('timeline/<timeline_type>', views.timeline, name='timeline'),
    path('timeline/<timeline_type>/page/<page>',
         views.timeline, name='timeline_old'),

    # Community
    path('communities', views.list_communities, name='communities'),
    path('communities/<int:community_id>',
         views.community, name='community'),
    path('communities/<int:community_id>/page/<page>',
         views.community, name='community_old'),

    # User
    path('users/<int:user_id>', views.user, name='user'),
    path('users/<int:user_id>/page/<page>', views.user, name='user_old'),

    # Post
    path('posts/<int:post_id>', views.post, name='post'),
    path('communities/<int:community_id>/new',
         views.new_post, name='new_post'),

    # Comment
    path('posts/<int:post_id>/comment', views.create_comment, name='comment'),
    path('posts/<int:post_id>/<int:comment_id>/reply',
         views.reply_comment, name='reply_comment'),

    # Authentication & Setting
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
]

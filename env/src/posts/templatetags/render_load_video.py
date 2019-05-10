from django import template
from posts.models import Post



register = template.Library()

@register.inclusion_tag('posts/snippets/render_load_video.html')
def render_load_video(video_obj):
    video = None
    if isinstance(video_obj, Post):
        video = video_obj.embed_link
    return {'video': video}
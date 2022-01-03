from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from blog.models import Post
import logging

logger = logging.getLogger(__name__)
register = template.Library()

# @register.filter
# def author_details(author):
#   if not author:
#     return ''
#   if author.first_name and author.last_name:
#     name = f'{author.first_name} {author.last_name}'
#   else:
#     name = f'{author.username}'
#   name = escape(name)
#   if author.email:
#     prefix = f'<a href="mailto:{escape(author.email)}">'
#     suffix = '</a>'
#   else:
#     prefix = ''
#     suffix = ''
#   html_content = mark_safe(f'{prefix}{name}{suffix}')
#   return html_content

@register.filter
def author_details(author, current_user):
  if not author:
    return ''
  if author == current_user:
    print('The same')
    return format_html('<strong>me</strong>')
  else:
    print('Not the same')
  if author.first_name and author.last_name:
    name = f'{author.first_name} {author.last_name}'
  else:
    name = f'{author.username}'
  if author.email:
    prefix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html('</a>')
  else:
    prefix = ''
    suffix = ''
  print(f"return is {format_html('{}{}{}', prefix, name, suffix)}")
  return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag
def row(cls=''):
  return format_html('<div class="row {}">', cls)
@register.simple_tag
def endrow():
  return format_html("</div>")

@register.simple_tag
def col(cls=''):
  return format_html('<div class="col {}">', cls)
@register.simple_tag
def endcol():
  return format_html('</div>')

@register.simple_tag(takes_context=True)
def author_details_tag(context):
  request = context['request']
  current_user = request.user
  post = context['post']
  author = post.author
  if author == current_user:
    return format_html("<strong>me</strong>")

  if author.first_name and author.last_name:
    name = f"{author.first_name} {author.last_name}"
  else:
    name = f"{author.username}"

  if author.email:
    prefix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html("</a>")
  else:
    prefix = ""
    suffix = ""

  return format_html("{}{}{}", prefix, name, suffix)

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk)[:5]
  logger.debug('Load %d recent posts for post %d', len(posts), post.pk)
  print('Load {0} recent posts for post {1}'.format(len(posts), post.pk))
  return {'title': 'Recent Posts', 'posts': posts}
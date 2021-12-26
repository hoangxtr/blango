from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html

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
    suffix = '</a>'
  else:
    prefix = ''
    suffix = ''
  return format_html('{}{}{}', prefix, name, suffix)


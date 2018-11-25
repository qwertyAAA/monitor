from django import template

register=template.Library()

@register.inclusion_tag('rbac/menu.h-tml')
def get_meun(request,):
    menu_list = request.session.get('menu_permission_list')

    return {'menu_list':menu_list}

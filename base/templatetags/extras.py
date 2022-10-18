from django import template

register = template.Library()


@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)

@register.filter
def phone_to_int(value):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if not value:
        return ""
    return value.replace(" ", "").replace("(", "").replace(")", "").replace(".", "").replace("-", "")
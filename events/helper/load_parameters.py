from ..models import Parameter


def footer_link():
    prms = Parameter.objects.filter(site='dsn_site').filter(parameter_name='finish_link')
    footer_link_value = ''
    if prms:
        footer_link_value = prms[0].value

    return footer_link_value

from django import conf
from importlib import import_module

LANGUAGE_CODE = 'en-us'
REST_STRUCTURE_CONF = {
    'response_handler': 'django_rest_structure.results.structure.response_structure',
    'log_handler': 'django_rest_structure.logs.console.emmit',
}

if hasattr(conf, 'settings'):
    LANGUAGE_CODE = conf.settings.LANGUAGE_CODE if hasattr(conf.settings, 'LANGUAGE_CODE') else LANGUAGE_CODE
    REST_STRUCTURE_CONF = {
        **REST_STRUCTURE_CONF,
        **conf.settings.REST_STRUCTURE_CONF
    } if hasattr(conf.settings, 'REST_STRUCTURE_CONF') else REST_STRUCTURE_CONF

    REST_STRUCTURE_CONF['response_handler'] = getattr(
        import_module('.'.join(REST_STRUCTURE_CONF['response_handler'].split('.')[:-1])),
        REST_STRUCTURE_CONF['response_handler'].split('.')[-1]
    )

    REST_STRUCTURE_CONF['log_handler'] = getattr(
        import_module('.'.join(REST_STRUCTURE_CONF['log_handler'].split('.')[:-1])),
        REST_STRUCTURE_CONF['log_handler'].split('.')[-1]
    )

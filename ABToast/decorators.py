from functools import wraps
from django.template.exceptions import TemplateDoesNotExist

def run_ab(*args, **kwargs):
    func = None
    if len(args) == 1 and callable(args[0]):
        func = args[0]
        template_kwarg = "template_name"
    else:
        template_kwarg = kwargs.get('template_kwarg')
    def _callable(func):
        @wraps(func)
        def _wrapped(request, *args, **kwargs):
            template_name = kwargs.get(template_kwarg)
            try:
                template_name = request.ab.run(template_name)
            except TemplateDoesNotExist:
                pass
            kwargs[template_kwarg] = template_name
            return func(request, *args, **kwargs)
        return _wrapped
    return _callable(func) if func else _callable


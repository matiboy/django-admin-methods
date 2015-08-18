import html2text
import django.utils.html
from .exceptions import InvalidFunctionName, ImproperlyConfigured
import django.template.loader

def short_text(field_name, length=200, name='', description='', suffix='...', strip_html=False):
    """
        Returns a function that can be used as a field on a Django admin list view
        It shortens the text field, optionally stripping HTML first.
        If the result is longer than specified length (default 200), it returns the shortened text followed by the suffix (default '...'')
        Otherwise the plain (or html-stripped) text is returned
    """
    def fn(self, instance):
        text = getattr(instance, field_name)
        if strip_html:
            text = html2text.html2text(text)
        if text.__len__() > length:
            return u'{short_text}{suffix}'.format(short_text=text[:length], suffix=suffix)
        return text

    if not name:
        name = field_name

    if not description:
        description = name

    fn.short_description = description

    # Django uses this internally to differentiate between functions, so needs to follow name
    try:
        fn.__name__ = str(name)
    except UnicodeEncodeError:
        raise InvalidFunctionName('Name parameter is used as the function name. It must be a string (not unicode). For translations, use the description parameter instead')

    return fn


def count(field_name, name='', description='', format='{}', format_plural=None, format_none=None):
    """
        Returns a function that can be used to count one-to-many and many-to-many relationship
        on a Django admin list view.
    """
    def fn(self, instance):
        count = getattr(instance, field_name).count()

        formatter = format_plural
        if count == 0:
            formatter = format_none
        elif count == 1:
            formatter = format

        return formatter.format(count)

    if format_none is None:
        format_none = format
    if format_plural is None:
        format_plural = format

    if not name:
        name = "count_{}".format(field_name)

    if not description:
        description = 'No. of {}'.format(field_name)

    fn.short_description = description

    # Django uses this internally to differentiate between functions, so needs to follow name
    try:
        fn.__name__ = str(name)
    except UnicodeEncodeError:
        raise InvalidFunctionName('Name parameter is used as the function name. It must be a string (not unicode). For translations, use the description parameter instead')

    return fn

def toggle(field_name, url_field=None, name='', description_true='', description_false='', header_title=''):
    """
        Returns a function that can allow to toggle a field. This is meant to be an inline action
    """
    if not description_true:
        description_true = field_name

    if not description_false:
        description_false = field_name


    def fn(self, instance):
        current = getattr(instance, field_name)
        if current:
            description = description_true
        else:
            description = description_false

        # If provided, assume url_field will be defined on instance, otherwise use default
        field = url_field
        if field is None:
            field = '{}_url'.format(field_name)
        # Try to get the url field
        try:
            url = getattr(instance, field)
        except AttributeError:
            raise ImproperlyConfigured('Model does not have attribute "{}".'.format(field))


        return django.template.loader.render_to_string('admin_methods/list/toggle.html', {
            'instance': instance,
            'description': description,
            'url': url
            })

    if not name:
        name = "toggle_{}".format(field_name)

    fn.short_description = header_title

    fn.allow_tags = True

    # Django uses this internally to differentiate between functions, so needs to follow name
    try:
        fn.__name__ = str(name)
    except UnicodeEncodeError:
        raise InvalidFunctionName('Name parameter is used as the function name. It must be a string (not unicode). For translations, use the description parameter instead')

    return fn

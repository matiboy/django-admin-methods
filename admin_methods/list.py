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

def toggle(field_name, url_field=None, name='', description_true='', description_false='', header_title='', template_path='admin_methods/list/toggle.html'):
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


        return django.template.loader.render_to_string(template_path, {
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

def list(related_name, separator=', ', model_attribute=None, name='', description='', limit=None):
    """
        Returns a function that can be used to display a (comma separated) list of related items - via a foreign key
        If model_attribute is not provided, __unicode__ will be used for each item. If it is a callable, will be called and its allow_tags flag will be used for the list flag
    """
    def fn(self, instance):
        # Work on the items
        items = getattr(instance, related_name).all()

        # Limit them if provided
        if limit is not None:
            items = items[:limit]
        # Either use model_attribute or __unicode__ otherwise
        def model_display(x):
            if model_attribute is None:
                return x.__unicode__()
            attr = getattr(x, model_attribute)
            # Could be a method
            if callable(attr):
                fn.allow_tags = attr.allow_tags
                return attr()
            return attr

        # Prepare the content
        return separator.join([model_display(x) for x in items])

    # Work on functions itself
    if not name:
        name = "list_{}".format(related_name)

    if not description:
        description = 'List of {}'.format(related_name)

    fn.short_description = description

    # Django uses this internally to differentiate between functions, so needs to follow name
    try:
        fn.__name__ = str(name)
    except UnicodeEncodeError:
        raise InvalidFunctionName('Name parameter is used as the function name. It must be a string (not unicode). For translations, use the description parameter instead')

    return fn


def attribute(dot_separated, name='', description=''):
    """
        Returns a function that can be used to display an attribute of an attribute etc
        For each item, if it is a callable, will be called
    """
    def fn(self, instance):
        # Work on the items
        path = dot_separated.split('.')
        item = instance
        for p in path:
            attr = getattr(item, p)
            if callable(attr):
                item = attr()
            else:
                item = attr

        return item

    # Work on functions itself
    if not name:
        name = "{}".format(dot_separated)

    if not description:
        description = 'Related'

    fn.short_description = description

    # Django uses this internally to differentiate between functions, so needs to follow name
    try:
        fn.__name__ = str(name)
    except UnicodeEncodeError:
        raise InvalidFunctionName('Name parameter is used as the function name. It must be a string (not unicode). For translations, use the description parameter instead')

    return fn

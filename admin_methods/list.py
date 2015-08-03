import html2text
from .exceptions import InvalidFunctionName

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

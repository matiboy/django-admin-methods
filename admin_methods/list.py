import html2text

def short_text(field_name, length=200, name='', suffix='...', strip_html=False):
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
            return '{short_text}{suffix}'.format(short_text=text[:length], suffix=suffix)
        return text

    if name:
        fn.short_description = name
    else:
        fn.short_description = field_name

    # Django uses this internally to differentiate between functions, so needs to follow name
    fn.__name__ = fn.short_description

    return fn

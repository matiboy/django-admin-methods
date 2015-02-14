
def image_thumb(field_name, name='', width=100, description=False, if_no_image=''):
    """ 
        Returns a function that can be used as a field on a Django admin list view
        It tries to use an ImageField's url and render it as an image of specified width (defaults to 100)
        If no description is given, short description will be left empty.
        An additional if_no_image named argument can be passed which will be shown if the entry has no image or a url can't be determined
    """
    # Self will be the model instance
    def fn(self):
        try:
            url = getattr(self, field_name).url
        except:
            return if_no_image
        return '<img src="{url}" width="{width}" />'.format(url=url, width=width)
    fn.allow_tags = True

    if not name:
        name = '{}_preview'.format(field_name)
    # Name is needed by Django for unicity
    fn.__name__ = name
    # Description is not
    if description:
        fn.short_description = name
    else:
        fn.short_description = ''

    return fn
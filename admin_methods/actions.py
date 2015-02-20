from .exceptions import InvalidFunctionName

def _set_name(fn, name, description):
    if not description:
        description = name
    fn.short_description = description
    try:
        fn.__name__ = str(name)
    except UnicodeEncodeError:
        raise InvalidFunctionName('Name parameter is used as the function name. It must be a string (not unicode). For translations, use the description parameter instead')

def toggle(field_name, name='', description=''):
    """
        Returns a function for setting field_name to the opposite of its current value
        If true_name is provided, it will be used as both Django admin's short_description
        and as the method __name__
        If not, those two values will receive a default value using the field name
    """
    def fn(modeladmin, request, queryset):
        """
            Will create a function which matches admin actions signature
        """
        # Simply set the field to true/false depending on direction
        for prop in queryset:
            setattr(prop, field_name, not getattr(prop, field_name))
            prop.save()

    # Give short description, either the one provided or a default
    if not name:
        name = 'Toggle {field}'.format(field=field_name)

    _set_name(fn, name, description)

    return fn

def true_false(field_name, true_name='', true_description='', false_name='', false_description=''):
    """
        Returns two functions, one for setting field_name to true and one for false
        If true_name is provided, it will be used as both Django admin's short_description
        and as the method __name__
        If not, those two values will receive a default value using the field name
    """
    def fn(modeladmin, request, queryset, direction):
        """
            Will create a function which matches admin actions signature
        """
        # Simply set the field to true/false depending on direction
        for prop in queryset:
            setattr(prop, field_name, direction)
            prop.save()

    def true_fn(modeladmin, request, queryset):
        """
            Function to set to true
        """
        return fn(modeladmin, request, queryset, True)

    def false_fn(modeladmin, request, queryset):
        """
            Function to set to false
        """
        return fn(modeladmin, request, queryset, False)

    # Give short description, either the one provided or a default
    if not true_name:
        true_name = 'Set as {field}'.format(field=field_name)
    # Django uses __name__ internally to differentiate between functions
    _set_name(true_fn, true_name, true_description)

    # Same as above for false function
    if not false_name:
        false_name = 'Set as non {field}'.format(field=field_name)
    _set_name(false_fn, false_name, false_description)

    # return the 2 functions
    return (true_fn, false_fn,)
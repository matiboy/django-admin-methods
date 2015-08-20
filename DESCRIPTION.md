# Django admin methods
Easily create [admin actions](https://docs.djangoproject.com/en/1.7/ref/contrib/admin/actions/) methods, [list field methods](https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) and [model methods](https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fields) for Django ModelAdmin
## Common usage
Use to quickly create Django admin items such as:

- *"Set as published"*, *"Set as unpublished"* actions in the admin list view
- Shortened description (limit to *n* characters) for use in the admin list view
- *Publish*, *Unpublish* links in admin list view
- Image thumbnail in change view

## Installation

```
pip install django-admin-methods
```

## API

### Actions

The *actions* module provides methods to build [admin actions](https://docs.djangoproject.com/en/1.7/ref/contrib/admin/actions/) and should be used within a **admin.ModelAdmin** declaration

#### true_false(field_name)

Returns two functions, one to set the model's *field_name* as true, one as false.  

##### Parameters

| Parameter         | Default | Description                                                                          |
|-------------------|---------|--------------------------------------------------------------------------------------|
| field_name        |         | the model field name                                                                 |
| true_name         | ''      | name for the "true" function. Defaults to "Set as *field_name*                       |
| false_name        | ''      | name for the "false" function. Defaults to "Set as non *field_name*                  |
| true_description  | ''      | displayed description for the "true" function. Defaults to "Set as *field_name*      |
| false_description | ''      | displayed description for the "false" function. Defaults to "Set as non *field_name* |

##### Notes

- *true_name* is used as the function name (make sure it is unique for this AdminModel)
- If *true_description* is given it will be used as the *short_description* value on the "true" function (which will be shown in the admin actions list).
- If no name is given, defaults to *"Set as [field_name]"* and *"Set as non [field_name]"
- *true_name* must be a string (not unicode). For translations, use *true_description* instead

##### Usage

```python
import admin_methods.actions

class PropertyAdmin(admin.ModelAdmin):
  set_published, set_unpublished = admin_methods.actions.true_false('published')
  set_highlighted, set_unhighlighted = admin_methods.actions.true_false('highlighted')
  actions = [set_published, set_unpublished, set_highlighted, set_unhighlighted]
```

Results in the actions below which would set the selected items' *published* value to true or false

![admin actions](https://cloud.githubusercontent.com/assets/487758/6201646/5da29110-b4f0-11e4-9b28-645906e4d2e0.png)

#### toggle(field_name, name='', description='')
Returns a function which sets the model's *field_name* as the opposite of its current value for each selected items.  
If no name is given, defaults to *"Toggle [field_name]"*  
If *description* is given it will be used as the *short_description* value on the function (which will be shown in the admin actions list). Otherwise *name* is used

**Note** *name* must be a string (not unicode). For translations, use *description* instead

### List

The *list* module provides methods to create extra fields for use in the list view and should be used within a **admin.ModelAdmin** declaration

#### short_text(field_name)

Returns a function to be used as a *list_display* entry.

##### Parameters

| Parameter   | Default | Description                                                                                                                                                             |
|-------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| field_name  |         | the model field name                                                                                                                                                    |
| length      | 200     | maximum length of short text (not inclusive of suffix)                                                                                                                  |
| name        | ''      | the name for the function. Will be set to the *field_name* if not provided. **Note** *name* must be a string (not unicode). For translations, use *description* instead |
| description | ''      | header title                                                                                                                                                            |
| suffix      | '...'   | suffix if length of short text is greater than *length*                                                                                                                 |
| strip_html  | False   | set true to strip html from short text                                                                                                                                  |

##### Notes

- If no name is given, *field_name* is used.  
- You may change the suffix which will be appended to **shortened** text only.  
- Use *strip_html* to remove HTML tags **before** length calculation
- *name* must be a string (not unicode). For translations, use *description* instead

##### Usage

```python
import admin_methods.list

class PropertyAdmin(admin.ModelAdmin):
  list_display = ('short_description',)
  short_description = admin_methods.list.short_text('description', length=150, strip_html=True)
```

Description will be shortened to 150 characters where necessary:  
![shortened text](https://cloud.githubusercontent.com/assets/487758/6201671/27c5ff4e-b4f2-11e4-878c-1c258f50f44c.png)

*Strip html* transforms this  
![nostrip](https://cloud.githubusercontent.com/assets/487758/6201670/27c4228c-b4f2-11e4-9611-b2696c3fd66e.png)

into this  
![stripped](https://cloud.githubusercontent.com/assets/487758/6201672/27c76794-b4f2-11e4-93d7-96a576285604.png)

#### count(field_name)

Returns a function that can be used to count one-to-many and many-to-many relationship on a Django admin list view.

##### Parameters

| Parameter     | Default | Description                                                                                                                                                                   |
|---------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| field_name    |         | the model field name                                                                                                                                                          |
| name          | ''      | the name for the function. Will be set to the count_{field_name} if not provided. **Note** *name* must be a string (not unicode). For translations, use *description* instead |
| format        | {}      | within the list, *format* is used for 1 item                                                                                                                                  |
| format_none   | format  | within the list, *format_none* is used for 0 items. If not provided, *format* is used                                                                                         |
| format_plural | format  | within the list, *format_plural* is used for more than 1 items. If not provided, *format* is used                                                                             |  

##### Notes

- If no name is given, count_*field_name* is used.
- Within the list, *format_none* is used for 0 items, *format* is used for 1 item and *format_plural* for more than 1 items. They all default to simply displaying the number of items.
- *name* must be a string (not unicode). For translations, use *description* instead

##### Usage

```python
import admin_methods.list

class UnitGroupAdmin(admin.ModelAdmin):
  unit_count = admin_methods.list.count('units', format='{} unit', format_plural='{} units', format_none='Nothing')
  list_display = ('name', 'unit_count')
```

**Result**
![image thumb](https://cloud.githubusercontent.com/assets/487758/9029641/902c05ae-39c9-11e5-9bf3-4bdf977020a4.png)

#### list(related_name)

Returns a function that can be used to display a comma separated list of items.  

##### Parameters

| Parameter       | Default | Description                                                                                                                                                                 |
|-----------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| related_name    |         | the model's related query set name                                                                                                                                          |
| name            | ''      | name for the function. Defaults to list_*related_name*                                                                                                                      |
| separator       | ', '    | separator between the values                                                                                                                                                |
| model_attribute | None    | for each model in the related queryset, call this method to get display value. If not provided, __unicode__() will be called. Refer to the notes below for more information |
| description     | ''      | displayed description for the header. Defaults to "List of *related_name*                                                                                                   |
| limit           | None    | Limit the number of results from the query set.                                                                                                                             |

##### Notes

- Related name is expected to be the name of the related queryset manager. `.all()` will be called on that property
- If no *name* is given, list_*related_name* is used.
- If no *model_attribute* is provided, the model's `__unicode__` method will be called.
- If *model_attribute* is a callable, it will be called for each model. Also, the function returned by `list` will have the same value for `allow_tags` as the callable, meaning that you may display html inside each list item
- If no *limit* is given, displays all the items
- *name* must be a string (not unicode). For header value, use *description* instead  

##### Usage

```python

import admin_methods.list

class UnitAdmin(admin.ModelAdmin):
    unit_tenant = admin_methods.list.list('tenants', model_attribute='name')

    list_display = ('name', 'unit_tenant',)
```

**Result**  
![image thumb](https://cloud.githubusercontent.com/assets/487758/9350541/566c4c30-4684-11e5-8437-bbab80f02277.png)


#### toggle(field_name)

**Important note**  
If you wish to us this method, either add `admin_methods` to your `INSTALLED_APPS` setting, or provide an available template

Returns a function that can be used to display a toggle link for a single field in a Django admin list view.  

##### Parameters

| Parameter         | Default                        | Description                                                                                                                                                                    |
|-------------------|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| field_name        |                                | the model field name                                                                                                                                                           |
| url_field         | None                           | the model field used to generate the url for the toggle link. If None, *field_name*_url is used                                                                                |
| name              | ''                             | the name for the function. Will be set to the count_{field_name} if not provided. **Note** *name* must be a string (not unicode). For translations, use *header_title* instead |
| description_true  | ''                             | within the list, the text for the link when the model field is true                                                                                                            |
| description_false | ''                             | within the list, the text for the link when the model field is false                                                                                                           |
| header_title      | ''                             | column title                                                                                                                                                                   |
| template_path     | admin_methods/list/toggle.html | the path to a template loaded via Django's templating engine. Override to use own templates                                                                                    |

##### Notes

- If no *name* is given, toggle_*field_name* is used.
- If no *url_field* is given, *field_name*_url is used.
- When the boolean to be toggled is true, *description_true* will be used in display. This defaults to field_name.
- When the boolean to be toggled is false, *description_false* will be used in display. This defaults to field_name.
- *name* must be a string (not unicode). For header value, use *header_title* instead  

##### Usage

```python
import admin_methods.list

class UnitGroupAdmin(admin.ModelAdmin):
  unit_publish = admin_methods.list.toggle('published', description_true='Unpublish', description_false='Publish')
  list_display = ('name', 'unit_publish')
```

**Result**
![image thumb](https://cloud.githubusercontent.com/assets/487758/9326721/81772c44-45ce-11e5-9156-e2f3b20b6758.png)

### Model
The *model* module provides methods to create extra fields for use in the add or change view and should be used within a **models.Model** declaration

#### image_thumb(field_name, name='', width=100, description=False, if_no_image='')

Returns a function to be set on a model, which can then be used in the *fields* and *readonly_fields* declaration of a ModelAdmin

##### Parameters

| Parameter        | Default | Description                                                                                                                                                                                                                                 |
|------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| field_name       |         | the model ImageField name                                                                                                                                                                                                                   |
| name             | ''      | the name for the function. Will be set to the field_name if not provided. **Note** Django needs a name to detect unique methods, but you can make sure that it does not get displayed on the page by setting description to False (default) |
| width            | 100     | image width                                                                                                                                                                                                                                 |
| description      | False   | display short description or not.                                                                                                                                                                                                           |
| description_text | ''      | If description is set to true, use this value as short_description. If not provided (and description is True), *name* will be used                                                                                                          |
| if_no_image      | ''      | value to display if no image is found                                                                                                                                                                                                       |

##### Sample code

**models.py**
```python
class Property(django.db.models.Model):
  top_image = django.db.models.ImageField(max_length=255, upload_to='properties/top')
  # Admin fields
  top_image_preview = admin_actions.model.image_thumb('top_image')
```

**admin.py**
```python
class PropertyAdmin(admin.ModelAdmin):
  fields = ('top_image', 'top_image_preview',)
  readonly_fields = ('top_image_preview',)
```

**Result**
![image thumb](https://cloud.githubusercontent.com/assets/487758/6201736/b9a489e6-b4f5-11e4-8ac3-da43a75fe5d1.png)

## Dependencies

- Uses [html2text](https://github.com/aaronsw/html2text) for stripping html in *list.short_text*

## Releases

###0.1.7

- [FEATURE] Added toggle in list
- [FEATURE] Added comma separated values in list
- [DOCUMENTATION] Changed example for short description to avoid confusion
- Special thanks to [andybak](https://github.com/andybak) for his suggestions

###0.1.6

- Added format parameter in count method

###0.1.5

- Added count in list module

###0.1.4

- Allow Unicode in short description

###0.1.3

Changelog

- Separated name and description in all methods. Allows to handle non-ascii translations

###0.1.2

Changelog

- Improved README

###0.1.1

Changelog

- Improved README

###0.1.0

Initial release

## TODO

- Testing!

#Django admin methods
Easily create [admin actions](https://docs.djangoproject.com/en/1.7/ref/contrib/admin/actions/) methods, [list field methods](https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) and [model methods](https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fields) for Django ModelAdmin
##Common usage
Use to quickly create Django admin items such as:

- *"Set as published"*, *"Set as unpublished"* actions in the admin list view
- Shortened descpription (limit to *n* characters) for use in the admin list view
- Image thumbnail in change view

## API

###Actions

The *actions* module provides methods to build [admin actions](https://docs.djangoproject.com/en/1.7/ref/contrib/admin/actions/) and should be used within a **admin.ModelAdmin** declaration

#### true_false(field_name, true_name='', false_name='', true_description='', false_description='')

Returns two functions, one to set the model's *field_name* as true, one as false.  
*true_name* is used as the function name (make sure it is unique for this AdminModel)
If *true_description* is given it will be used as the *short_description* value on the "true" function (which will be shown in the admin actions list).  
If no name is given, defaults to *"Set as [field_name]"* and *"Set as non [field_name]"

**Note** *true_name* must be a string (not unicode). For translations, use *true_description* instead

##### Sample code

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

#### short_text(field_name, length=200, name='', description='', suffix='...', strip_html=False)
Returns a function to be used as a *list_display* entry.  
If no name is given, *field_name* is used. 
You may change the suffix which will be appended to **shortened** text only.  
Use *strip_html* to remove HTML tags **before** length calculation

**Note** *name* must be a string (not unicode). For translations, use *description* instead

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

### Model
The *model* module provides methods to create extra fields for use in the add or change view and should be used within a **models.Model** declaration

#### image_thumb(field_name, name='', width=100, description=False, if_no_image='')

Returns a function to be set on a model, which can then be used in the *fields* and *readonly_fields* declaration of a ModelAdmin

#####Parameters

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

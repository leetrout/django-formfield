from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json


class AdminJSONFieldWidget(AdminTextareaWidget):
    """Provide value parsing at render time if using the raw JSON field in
    the admin.
    """
    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {'cls': DjangoJSONEncoder})
        super(AdminJSONFieldWidget, self).__init__(*args, **kwargs)
    
    def render(self, name, value, **kwargs):
        # try to dump to a string if needed
        if isinstance(value, dict):
            try:
                value = json.dumps(value, **self.dump_kwargs)
            except ValueError:
                pass
        return super(AdminJSONFieldWidget, self).render(name, value, **kwargs)


class FormFieldWidget(forms.MultiWidget):
    """
    This widget will render each field found in the supplied form.
    """
    def __init__(self, fields, attrs=None):
        self.fields = fields
        # Retreive each field widget for the form
        widgets = [f.field.widget for f in self.fields]
        
        super(FormFieldWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        """
        Retreieve each field value or provide the initial values
        """
        if value:
            return [value.get(field.name, None) for field in self.fields]
        return [field.field.initial for field in self.fields]
        
    def format_label(self, field, counter):
        """
        Format the label for each field
        """
        return '<label for="id_formfield_%s" %s>%s</label>' % (
            counter, field.field.required and 'class="required"', field.label)
            
    def format_help_text(self, field, counter):
        """
        Format the help text for the bound field
        """
        return '<p class="help">%s</p>' % field.help_text
        
    def format_output(self, rendered_widgets):
        """
        This output will yeild all widgets grouped in a un-ordered list
        """
        ret = ['<ul class="formfield">']
        for i, field in enumerate(self.fields):
            label = self.format_label(field, i)
            help_text = self.format_help_text(field, i)
            ret.append('<li>%s %s %s</li>' % (
                label, rendered_widgets[i], field.help_text and help_text))
            
        ret.append('</ul>')
        return u''.join(ret)

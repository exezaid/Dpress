from django import newforms as forms
 
class TypedForm(forms.Form):

    def __init__(self, names, type_parameters, *args, **kwargs):
        super(TypedForm, self).__init__(*args, **kwargs)
        if len(names) == len(type_parameters):
            self.names = names
            self.type_parameters = type_parameters
            for i in range(0, len(names)):
                self.fields[names[i]] = forms.CharField(max_length = 50)

    def clean(self):
        for i in range(0, len(self.names)):
            val = self.cleaned_data[self.names[i]]
            exp_type = self.type_parameters[i]
            if exp_type == 'int':
                val = int(val)
            elif exp_type == 'float':
                val = float(val)
            elif exp_type == 'string':
                val = val.encode('utf8')
            self.cleaned_data[self.names[i]] = val
#        if 'jobs' not in self.cleaned_data or \
#           len(self.cleaned_data['jobs']) == 0:
#            raise forms.ValidationError(
#                u'You must select at least one Job for invoice.')
        return self.cleaned_data

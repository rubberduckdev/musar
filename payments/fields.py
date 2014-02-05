from django import forms


class FullNameFileField(forms.FileField):
    def get_full_name(self):
        if getattr(instance, self.attname):
            file_name = getattr(instance, 'get_{}_filename'.format(self.name))()
            if os.path.exists(file_name):
                return file_name
        else:
            raise ValueError

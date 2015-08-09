# Alan project
# Forms.py
# Version 0.1
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django import forms


class UploadFileForm(forms.Form):
    docfile = forms.FileField()

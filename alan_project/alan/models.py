# Alan project
# Models.py
# Version 0.1
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.db import models

class Investor(models.Model):
    name = models.CharField(max_length=42, verbose_name='Name')
    url = models.URLField(blank=True, verbose_name='Url')
    
    def __str__(self):
        return self.name
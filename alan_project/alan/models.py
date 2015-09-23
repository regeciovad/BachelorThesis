# Alan project
# Models.py
# Version 0.3
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.db import models


class Nonterminal(models.Model):
    char = models.CharField(max_length=1, verbose_name='Nonterminal')

    def __str__(self):
        return self.char


class Terminal(models.Model):
    char = models.CharField(max_length=1, verbose_name='Terminal')

    def __str__(self):
        return self.char


class Rule (models.Model):
    left_hand_side = models.CharField(max_length=1, verbose_name='Left hand side')
    right_hand_side = models.CharField(max_length=42, verbose_name='Right hand side')

    def __str__(self):
        arrow = ' \u2192 '
        return self.left_hand_side + arrow + self.right_hand_side

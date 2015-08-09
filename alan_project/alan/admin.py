from django.contrib import admin
from .models import Nonterminal, Terminal, Rule


class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    search_fields = ['left_side']
    list_filter = ['left_side']

admin.site.register(Rule, RuleAdmin)


class NonterminalAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')

admin.site.register(Nonterminal, NonterminalAdmin)


class TerminalAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')

admin.site.register(Terminal, TerminalAdmin)

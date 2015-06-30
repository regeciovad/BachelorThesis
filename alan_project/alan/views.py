from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from .models import *
import re

def about(request):
    return render(request, 'alan/about.html', {})

def parser(input):
    input = re.sub(r'\s', '', input)
    output = []
    iter_input = iter(input)
    for char in iter_input:
        if char == '{':
            while char != '}':
                try:
                    char = next(iter_input)
                except StopIteration:
                    output.append('[error]')
                    return output
            continue
        elif char == 'i':
            output.append('[id,i]')
        elif char == '+':
            output.append('[op,+]')
        elif char == '*':
            output.append('[op,*]')
        elif char == '(':
            output.append('[op,(]')
        elif char == ')':
            output.append('[op,)]')
        else:
            output.append('[error]')
    return output


def index(request):
    grammar = Rule.objects.order_by('id')
    if request.method == 'POST':
        code = ''
        if 'lex_code' in request.POST and request.POST['lex_code']:
            code = request.POST['lex_code']
        lex = parser(code)
        return render(request, 'alan/index.html', {'code':code, 'lex':lex, 'grammar':grammar})
    return render(request, 'alan/index.html', {'grammar':grammar})
    
def grammar(request):
    grammar = Rule.objects.order_by('id')
    terminals = Terminal.objects.order_by('id')
    terminals = ', '.join([terminals.char for terminals in terminals]) 
    nonterminals = Nonterminal.objects.order_by('id')
    nonterminals = ', '.join([nonterminals.char for nonterminals in nonterminals])
    return render(
        request, 'alan/grammar.html', {'grammar':grammar, 'terminals': terminals,
        'nonterminals':nonterminals})
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from .models import *
from .scanner import *

def about(request):
    return render(request, 'alan/about.html', {})

def index(request):
    scanner = Scanner()
    grammar = Rule.objects.order_by('id')
    if request.method == 'POST':
        code = ''
        if 'lex_code' in request.POST and request.POST['lex_code']:
            code = request.POST['lex_code']
        lex = scanner.scanner_analysis(code)
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
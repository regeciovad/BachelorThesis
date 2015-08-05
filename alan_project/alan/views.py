# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q
from django.db.models.query import QuerySet
from .models import *
from .scanner import *
from .forms import UploadFileForm

scanner = Scanner()

def about(request):
    return render(request, 'alan/about.html', {})

def man(request):
    return render(request, 'alan/man.html', {})

def index(request):
    code = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            path = (request.FILES['docfile'])
            for chunk in path.chunks():
                code = code + str(chunk.decode('utf-8', 'ignore'))
    else:
        form = UploadFileForm()
    return render(request, 'alan/index.html', {'code':code, 'form':form}, context_instance=RequestContext(request))


def run_scanner(request):
    code = ''
    lex_code = ''
    if request.method == 'POST':
        if 'fun_code_area' in request.POST and request.POST['fun_code_area']:
            code = request.POST['fun_code_area']
            lex_code = scanner.new_scanner(code)
    return render(request, 'alan/scanner.html', {'code':code, 'lex_code':lex_code})

def run_parser(request):
    code = ''
    lex_code = ''
    parser_code = ''
    if request.method == 'POST':
        code = scanner._code
        lex_code = scanner._scanner
        parser_code = 'Výsledek SA'
    return render(request, 'alan/parser.html', {'code':code, 'lex_code':lex_code, 'parser_code':parser_code})
    
def grammar(request):
    grammar = Rule.objects.order_by('id')
    terminals = Terminal.objects.order_by('id')
    terminals = ', '.join([terminals.char for terminals in terminals]) 
    nonterminals = Nonterminal.objects.order_by('id')
    nonterminals = ', '.join([nonterminals.char for nonterminals in nonterminals])
    keywords = scanner._keywords
    return render(
        request, 'alan/grammar.html', {'grammar':grammar, 'terminals': terminals,
        'nonterminals':nonterminals, 'keywords':keywords})
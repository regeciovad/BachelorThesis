# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from .models import Nonterminal, Terminal, Rule
from .scanner import Scanner
from .parser import Parser
from .forms import UploadFileForm
import os
import zipfile
from io import StringIO

scanner = Scanner()
parser = Parser()


def about(request):
    return render(request, 'alan/about.html', {})


def man(request):
    return render(request, 'alan/man.html', {})

def changelog (request):
    changelog = []
    with open('../CHANGELOG.md') as f:
        for line in f.readlines():
            changelog.append(line)
    return render(request, 'alan/changelog.html', {'changelog':changelog})


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
    return render(request, 'alan/index.html', {'code': code, 'form': form},
                  context_instance=RequestContext(request))


def run_scanner(request):
    code = ''
    lex_code = []
    next = True
    if request.method == 'POST':
        if 'fun_code_area' in request.POST and request.POST['fun_code_area']:
            code = request.POST['fun_code_area']
            lex_code = scanner.scanner_analysis(code)
            if not lex_code:
                lex_code.append('[chyba, prazdny program]')
            if any("chyba," in s for s in lex_code):
                next = False
    return render(request, 'alan/scanner.html', {'code': code,
                  'lex_code': lex_code, 'next': next})


def run_parser(request):
    code = ''
    lex_code = ''
    parser_code = ''
    grammar = Rule.objects.order_by('id')
    grammar_list = []
    grammar_list.append({'id':0, 'left':'', 'right':''})
    for g in grammar:
        grammar_list.append({'id':g.id, 'left':g.left_hand_side, 'right':g.right_hand_side})
    if request.method == 'POST':
        code = scanner._code
        lex_code = scanner._scanner
        #lex_code = ['[i, a]', '[+]', '[i, b]']
        #lex_code = ['[i, a]', '[+]', '[i, b]', '[;]', '[i, b]', '[-]', '[i, c]']
        stack, state, parser_code = parser.parser_analysis(lex_code, grammar_list)
    return render(request, 'alan/parser.html', {'code': code,
                  'lex_code': lex_code, 'parser_code': parser_code,
                  'stack':stack, 'state':state})


def grammar(request):
    grammar = Rule.objects.order_by('id')
    terminals = Terminal.objects.order_by('id')
    t_list = ', '.join([t.char for t in terminals])
    nonterminals = Nonterminal.objects.order_by('id')
    n_list = ', '.join([n.char for n in nonterminals])
    return render(request, 'alan/grammar.html', {'grammar': grammar,
                  'terminals': t_list, 'nonterminals': n_list})

def lrtable(request):
    table_action, table_goto = parser.generate_table_print()
    return render(request, 'alan/lrtable.html', {'table_action': table_action,
                  'table_goto':table_goto})


def download(request):
    zipf = zipfile.ZipFile('alanfiles.zip', 'w')
    fpath = 'files/'
    for root, dirs, files in os.walk(fpath):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    response = HttpResponse(open('alanfiles.zip', 'rb').read())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename=alanfiles.zip'
    return response


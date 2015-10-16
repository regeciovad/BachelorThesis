# -*- coding: utf-8 -*-
# Advanced Error Recovery during Bottom-Up Parsing
# File: views.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from .models import Nonterminal, Terminal, Rule
from .scanner import Scanner
from .parser import Parser
from .panic_mode import PanicModeParser
from .lrtable import LRTable
from .forms import UploadFileForm
import os
import zipfile


def get_grammar():
    """ Returns list of grammar rules order by id (number)  """
    grammar = Rule.objects.order_by('id')
    grammar_list = []
    grammar_list.append({'id': 0, 'left': '', 'right': ''})
    for g in grammar:
        grammar_list.append({'id': g.id, 'left': g.left_hand_side,
                             'right': g.right_hand_side})
    return grammar_list


def about(request):
    return render(request, 'alan/about.html', {})


def man(request):
    return render(request, 'alan/man.html', {})


def changelog(request):
    changelog = []
    with open('../CHANGELOG.md') as f:
        for line in f.readlines():
            changelog.append(line)
    return render(request, 'alan/changelog.html', {'changelog': changelog})


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
    """ This view is called by button 'Spustit lexikalni analyzu'
        in index.html and return results of Lexical analysis """
    scanner = Scanner()
    tokens = []
    next = True
    if request.method == 'POST':
        if 'fun_code_area' in request.POST and request.POST['fun_code_area']:
            source_code = request.POST['fun_code_area']
            request.session['source_code'] = source_code
            tokens, exit_code = scanner.scanner_analysis(source_code)
            if not tokens:
                tokens.append('[chyba, prazdny program]')
            else:
                request.session['tokens'] = tokens
            if exit_code:
                next = False
    return render(request, 'alan/scanner.html', {'source_code': source_code,
                  'tokens': tokens, 'next': next})


def run_parser(request):
    """ This view is called by button 'Spustit syntaktickou analyzu'
        in index.html and return results of Lexical analysis """
    parser = Parser()
    source_code = request.session.get('source_code', '')
    tokens = request.session.get('tokens', '')
    parser_result = ''
    grammar_list = get_grammar()
    if request.method == 'POST':
        parser_result, stack, state, exit_code = parser.parser_analysis(
            tokens, grammar_list)
    return render(request, 'alan/parser.html', {'source_code': source_code,
                  'tokens': tokens, 'parser_result': parser_result,
                  'stack': stack, 'state': state, 'exit_code': exit_code})


def run_panic_mode_parser(request):
    parser = PanicModeParser()
    code = ''
    tokens = ''
    parser_code = ''
    grammar_list = get_grammar()
    if request.method == 'POST':
        code = request.session.get('source_code', '')
        tokens = request.session.get('tokens', '')
        stack, state, parser_code, exit_code, panic_mode = parser.parser_analysis(tokens, grammar_list)
    return render(request, 'alan/panic_mode_parser.html', {'code': code,
                  'tokens': tokens, 'parser_code': parser_code,
                  'stack': stack, 'state': state, 'exit_code': exit_code,
                  'panic_mode': panic_mode})


def grammar(request):
    grammar = Rule.objects.order_by('id')
    terminals = Terminal.objects.order_by('id')
    t_list = ', '.join([t.char for t in terminals])
    nonterminals = Nonterminal.objects.order_by('id')
    n_list = ', '.join([n.char for n in nonterminals])
    return render(request, 'alan/grammar.html', {'grammar': grammar,
                  'terminals': t_list, 'nonterminals': n_list})


def lrtable(request):
    lrtable = LRTable()
    table_action, table_goto = lrtable.generate_table_print()
    return render(request, 'alan/lrtable.html', {'table_action': table_action,
                  'table_goto': table_goto})


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

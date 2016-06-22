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
from .panic_mode_first import PanicModeParserFirst
from .ad_hoc import ParserAdHoc
from .alan_method import AlanMethodParser
from .lrtable import LRTable
from .forms import UploadFileForm
import os
import zipfile
import time


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
    """ Render of about page """
    return render(request, 'alan/about.html', {})

def report(request):
    with open('./report.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed

def index(request):
    """ The page to obtain input for the scanner """
    # Initialization of input
    if 'source_code' in request.session:
        code = request.session['source_code']
    else:
        code = ''
    # Upload of file
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            code = ''
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
    # Initialization
    scanner = Scanner()
    tokens = []
    source_code = ''
    exit_code = 0
    # Run of Lexical analysis
    if request.method == 'POST':
        if 'fun_code_area' in request.POST and request.POST['fun_code_area']:
            source_code = request.POST['fun_code_area']
            request.session['source_code'] = source_code
            tokens, exit_code = scanner.scanner_analysis(source_code)
            request.session['tokens'] = tokens
    return render(request, 'alan/scanner.html', {'source_code': source_code,
                  'tokens': tokens, 'exit_code': exit_code})


def run_parser(request):
    """ This view is called by button 'Spustit syntaktickou analyzu'
        in scanner.html and return results of basic syntax analysis """
    parser = Parser()
    source_code = request.session.get('source_code', '')
    tokens = request.session.get('tokens', '')
    parser_result = stack = state = []
    exit_code = 0
    grammar_list = get_grammar()
    if request.method == 'POST':
        parser_result, stack, state, exit_code = parser.parser_analysis(
            tokens, grammar_list)
    return render(request, 'alan/parser.html', {'source_code': source_code,
                  'tokens': tokens, 'parser_result': parser_result,
                  'stack': stack, 'state': state, 'exit_code': exit_code})


def run_panic_mode_parser(request):
    """ This view is called by button 'Spustit Panic mode'
        in parser.html and return results of the first advanced
        syntax analysis """
    parser = PanicModeParser()
    source_code = request.session.get('source_code', '')
    tokens = request.session.get('tokens', '')
    parser_result = stack = state = panic_mode = []
    exit_code = 0
    grammar_list = get_grammar()
    begin = time.clock()
    if request.method == 'POST':
        parser_result, stack, state, exit_code, panic_mode = parser.parser_analysis(tokens, grammar_list)
    end = time.clock()
    mytime = end - begin
    parser_result.append("Celkový čas analýzy: %f \u03BCs" % mytime)
    parser_result.append('')
    return render(request, 'alan/panic_mode_parser.html', {
                  'source_code': source_code, 'tokens': tokens,
                  'parser_result': parser_result, 'stack': stack,
                  'state': state, 'exit_code': exit_code,
                  'panic_mode': panic_mode})

def run_panic_mode_parser_first(request):
    """ This view is called by button 'Spustit Panic mode'
        in parser.html and return results of the first advanced
        syntax analysis """
    parser = PanicModeParserFirst()
    source_code = request.session.get('source_code', '')
    tokens = request.session.get('tokens', '')
    parser_result = stack = state = panic_mode = []
    exit_code = 0
    grammar_list = get_grammar()
    begin = time.clock()
    if request.method == 'POST':
        parser_result, stack, state, exit_code, panic_mode = parser.parser_analysis(tokens, grammar_list)
    end = time.clock()
    mytime = end - begin
    parser_result.append("Celkový čas analýzy: %f \u03BCs" % mytime)
    parser_result.append('')
    return render(request, 'alan/panic_mode_parser_first.html', {
                  'source_code': source_code, 'tokens': tokens,
                  'parser_result': parser_result, 'stack': stack,
                  'state': state, 'exit_code': exit_code,
                  'panic_mode': panic_mode})

def run_parser_ad_hoc(request):
    """ This view is called by button 'Spustit Ad-hoc'
        in parser.html and return results of the first advanced
        syntax analysis """
    parser = ParserAdHoc()
    source_code = request.session.get('source_code', '')
    tokens = request.session.get('tokens', '')
    parser_result = stack = state = []
    exit_code = 0
    grammar_list = get_grammar()
    lrtable = LRTable()
    table_action, table_goto = lrtable.generate_ad_hoc_table_print()
    begin = time.clock()
    if request.method == 'POST':
        parser_result, stack, state, exit_code = parser.parser_analysis(tokens, grammar_list)
    end = time.clock()
    mytime = end - begin
    parser_result.append("Celkový čas analýzy: %f \u03BCs" % mytime)
    parser_result.append('')
    return render(request, 'alan/ad_hoc_parser.html', {
                  'source_code': source_code, 'tokens': tokens,
                  'parser_result': parser_result, 'stack': stack,
                  'state': state, 'exit_code': exit_code,
                  'table_action': table_action, 'table_goto': table_goto})

def run_alan_method_parser(request):
    """ This view is called by button 'Spustit Alan method'
        in parser.html and return results of the first advanced
        syntax analysis """
    parser = AlanMethodParser()
    source_code = request.session.get('source_code', '')
    tokens = request.session.get('tokens', '')
    parser_result = stack = state = alan_method = []
    exit_code = 0
    grammar_list = get_grammar()
    begin = time.clock()
    if request.method == 'POST':
        parser_result, stack, state, exit_code, alan_method = parser.parser_analysis(tokens, grammar_list)
    end = time.clock()
    mytime = end - begin
    parser_result.append("Čas zotavení: %f \u03BCs" % mytime)
    parser_result.append('')
    return render(request, 'alan/alan_method_parser.html', {
                  'source_code': source_code, 'tokens': tokens,
                  'parser_result': parser_result, 'stack': stack,
                  'state': state, 'exit_code': exit_code,
                  'alan_method': alan_method})

def comparison(request):
    return render(request, 'alan/comparison.html', {})


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

def ad_hoc_lrtable(request):
    lrtable = LRTable()
    table_action, table_goto = lrtable.generate_ad_hoc_table_print()
    return render(request, 'alan/ahlrtable.html', {'table_action': table_action,
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

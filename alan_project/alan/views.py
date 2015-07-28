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

def about(request):
    return render(request, 'alan/about.html', {})

def index(request):
    code = '{ Zde vložte svůj kód }'
    #with open(r'C:\Users\Public\BachelorThesis\alan_project\alan\files\fun_double.txt') as f:
        #code = f.read() 
        #print (code)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            code = ''
            path = (request.FILES['docfile'])
            for chunk in path.chunks():
                code = code + str(chunk.decode('utf-8'))
    else:
        form = UploadFileForm()
    return render(request, 'alan/index.html', {'code':code, 'form':form},context_instance=RequestContext(request))


def run_scanner(request):
    scanner = Scanner()
    if request.method == 'POST':
        if 'lex_code' in request.POST and request.POST['lex_code']:
            code = request.POST['lex_code']
        lex = scanner.scanner_analysis(code)
        return render(request, 'alan/index.html', {'code':code, 'lex':lex, 'grammar':grammar})
    return render(request, 'alan/index.html', {'code':code,'grammar':grammar})
    
def grammar(request):
    grammar = Rule.objects.order_by('id')
    terminals = Terminal.objects.order_by('id')
    terminals = ', '.join([terminals.char for terminals in terminals]) 
    nonterminals = Nonterminal.objects.order_by('id')
    nonterminals = ', '.join([nonterminals.char for nonterminals in nonterminals])
    return render(
        request, 'alan/grammar.html', {'grammar':grammar, 'terminals': terminals,
        'nonterminals':nonterminals})
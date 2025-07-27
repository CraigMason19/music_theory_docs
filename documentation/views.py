import inspect

from django.shortcuts import render

import music_theory as mt

def docs_view(request):
    functions = []
    
    for name, func in inspect.getmembers(mt, inspect.isfunction):
        functions.append({
            'name': name,
            'doc': inspect.getdoc(func)
        })

    return render(request, 'docs.html', {'functions': functions})

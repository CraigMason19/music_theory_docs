from django.shortcuts import render

from django.shortcuts import render
import music_theory as mt
import inspect

def docs_view(request):
    functions = []
    
    for name, func in inspect.getmembers(mt, inspect.isfunction):
        functions.append({
            'name': name,
            'doc': inspect.getdoc(func)
        })

    return render(request, 'docs/docs.html', {'functions': functions})

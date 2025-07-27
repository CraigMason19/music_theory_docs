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

    return render(request, 'documentation.html', {'functions': functions})


def notes_view(request):
    attrs = [name for name, _ in inspect.getmembers(mt.Note, inspect.ismethod)]


    return render(request, "notes.html", {"attributes": attrs})
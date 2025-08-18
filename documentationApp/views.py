import inspect

from django.shortcuts import render
from django.utils.safestring import mark_safe

import music_theory as mt

from .source.doc_extractor import ModuleDoc


def build_dynamic_docs(module):
    module_doc = ModuleDoc(module)
    doc_strs = []

    for f in module_doc.functions:
        doc_strs.append({ 
            "name": "Function: " + f.name, 
            "docstring": mark_safe(f.docstring) 
        })

    for c in module_doc.classes:
        doc_strs.append({ 
            "name": "Class: " + c.name, 
            "docstring": mark_safe(c.docstring) 
        })          

        for m in c.methods:      
            doc_strs.append({ 
                "name": f"Method: {c.name}.{m.name}", 
                "docstring": mark_safe(m.docstring) 
            })  

    return doc_strs

def docs_view(request):
    functions = []
    
    for name, func in inspect.getmembers(mt, inspect.isfunction):
        functions.append({
            'name': name,
            'doc': inspect.getdoc(func)
        })

    return render(request, 'documentation.html', {'functions': functions})


def notes_view(request):
    module = mt.notes

    context = {
        "module_name": module.__name__,
        "doc_strs": build_dynamic_docs(module),
    }

    return render(request, "notes.html", context)

def scales_view(request):
    module = mt.scales

    print(module)

    context = {
        "module_name": module.__name__,
        "doc_strs": build_dynamic_docs(module),
    }

    return render(request, "scales.html", context)
import inspect

from django.shortcuts import render
from django.utils.safestring import mark_safe

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
    attrs = [name for name, _ in inspect.getmembers(mt.Note)]
    # Note.next
    attrs = [name for name, _ in inspect.getmembers(mt.Note, inspect.ismethod)]
    # attrs = [name for name, _ in inspect.getmembers(mt.Note, inspect.ismethod) if not name.startswith("__")]


    target_class = mt.Note  # Replace with your actual class

    # Get methods defined *directly* in this class's file
    # attrs = []
    # for name, member in inspect.getmembers(target_class, inspect.isfunction):
    #     # Check if the method is defined in the same source file as the class
    #     if inspect.getsourcefile(member) == inspect.getsourcefile(target_class):
    #         attrs.append(name)


 


 
    # formatted = mark_safe(f"<pre>{mt.Note.__doc__}</pre>")
    formatted = mark_safe(f"{mt.Note.__doc__}")


    doc_strs = [
        { "name": "Class: " + mt.Note.__name__, "doc_str": formatted },
        { "name": "Method: " + mt.Note.from_index.__name__, "doc_str": mark_safe(f"{mt.Note.from_index.__doc__}") },
        { "name": "Function: " + mt.notes.transpose.__name__, "doc_str": mark_safe(f"{mt.Note.transpose.__doc__}") },
    ]

    context = {
        "module_name": mt.notes.__name__,
        "class_doc": mark_safe(formatted),
        "doc_strs": doc_strs,
    }

    return render(request, "notes.html", context)

 

 
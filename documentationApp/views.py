# Python
import inspect
import re
from pathlib import Path

# Django
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.safestring import mark_safe

# PIP modules
import markdown

# Custom
import music_theory as mt
from .source.doc_extractor import ModuleDoc


def strip_screenshots_from_markdown(raw_md):
    # Remove image embeds from screenshots folder
    no_images = re.sub(r'!\[.*?\]\(screenshots/.*?\)', '', raw_md, flags=re.MULTILINE)

    # Remove the '## Screenshots' heading
    no_heading = re.sub(r'^## Screenshots\s*$', '', no_images, flags=re.MULTILINE)

    # Collapse excessive blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', no_heading)

    return cleaned

def build_dynamic_docs(module):
    module_doc = ModuleDoc(module)
    doc_strs = []

    for f in module_doc.functions:
        doc_strs.append({ 
            "name": "Function: " + f.name, 
            "docstring": mark_safe(f.docstring),
            "tag": "h3",
        })

    for c in module_doc.classes:
        doc_strs.append({ 
            "name": "Class: " + c.name, 
            "docstring": mark_safe(c.docstring),
            "tag": "h2",
        })          

        for m in c.methods:      
            doc_strs.append({ 
                "name": f"Method: {c.name}.{m.name}", 
                "docstring": mark_safe(m.docstring),
                "tag": "h3",
            })  

    return doc_strs

def documentation_view(request):
    md_path = Path(__file__).parent.parent / "readme.md"

    if not md_path.exists():
        return HttpResponseNotFound(md_path)      

    raw_md = md_path.read_text(encoding="utf-8")
    clean_md = strip_screenshots_from_markdown(raw_md)

    html_content = markdown.markdown(clean_md, extensions=["fenced_code", "tables", "toc"])

    context = {
        "html_content": html_content,
    }

    return render(request, "documentation.html", context)


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

def examples_view(request):
    """
    Displays the examples Markdown file
    """
    md_path = Path(__file__).parent / "source" / "examples.md"

    if not md_path.exists():
        return HttpResponseNotFound(md_path)      

    raw_md = md_path.read_text(encoding="utf-8")
    html_content = markdown.markdown(raw_md, extensions=["fenced_code", "tables", "toc"])
 

    context = {
        "html_content": html_content,
    }

    return render(request, "examples.html", context)
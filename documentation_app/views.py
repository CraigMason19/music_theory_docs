# Python
from pathlib import Path
import logging
import pkgutil
import re

# Django
from django.conf import settings
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render
from django.utils.safestring import mark_safe

# PIP modules
import markdown

# Custom
import music_theory as mt

from music_theory.scales import modes_from_note 
from core.doc_extractor import DocExtractor
from core.mt_modules import get_available_modules
from core.parser import parse_note, parse_key_type, parse_bool

logger = logging.getLogger(__name__)

def strip_screenshots_from_markdown(raw_md):
    # Remove image embeds from screenshots folder
    no_images = re.sub(r'!\[.*?\]\(screenshots/.*?\)', '', raw_md, flags=re.MULTILINE)

    # Remove the '## Screenshots' heading
    no_heading = re.sub(r'^## Screenshots\s*$', '', no_images, flags=re.MULTILINE)

    # Collapse excessive blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', no_heading)

    return cleaned

def build_dynamic_doc_structure(module):
    de = DocExtractor(module)

    doc_structure = {
        "module_docstring": de.module_docstring,
        "functions": [],
        "classes": []
    }

    for f in de.functions:
        doc_structure["functions"].append({
            "name": f.name,
            "tag": "h2",
            "anchor": f"function-{f.name}",
            "docstring": mark_safe(f.docstring),
        })

    for c in de.classes:
        class_entry = {
            "name": c.name,
            "tag": "h2",
            "anchor": f"class-{c.name}",
            "docstring": mark_safe(c.docstring),
            "methods": []
        }

        for m in c.methods:
            class_entry["methods"].append({
                "name": m.name,
                "tag": "h3",
                "anchor": f"method-{c.name}-{m.name}",
                "docstring": mark_safe(m.docstring),
            })

        doc_structure["classes"].append(class_entry)

    return doc_structure

def documentation_view(request):
    md_path = Path(__file__).parent.parent / "readme.md"

    if not md_path.exists():
        return HttpResponseNotFound(md_path)      

    raw_md = md_path.read_text(encoding="utf-8")
    clean_md = strip_screenshots_from_markdown(raw_md)

    html_content = markdown.markdown(clean_md, extensions=["fenced_code", "tables", "toc"])

    context = {
        "BAKE_MODE": settings.BAKE_MODE,
        "doc_root": "",
        "html_content": html_content,
        "available_modules": get_available_modules(),
    }

    return render(request, "documentation.html", context)

def module_view(request, module_name):
    module = getattr(mt, module_name)
    
    if module is None:
        raise Http404(f"No such module: {module_name}")

    context = {
        "BAKE_MODE": settings.BAKE_MODE,
        "doc_root": "../",
        "module_name": module_name,
        "doc_structure": build_dynamic_doc_structure(module),
        "available_modules": get_available_modules(),
    }

    return render(request, "module_docs.html", context)

def examples_view(request):
    """
    Displays the examples Markdown file
    """
    md_path = Path(__file__).parent.parent / "static" / "Markdown" / "examples.md"

    if not md_path.exists():
        return HttpResponseNotFound(md_path)      
 
    raw_md = md_path.read_text(encoding="utf-8")
    clean_md = strip_screenshots_from_markdown(raw_md)

    html_content = markdown.markdown(
        clean_md, 
        extensions=["fenced_code", "codehilite", "tables", "toc"],
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "noclasses": True  # Use CSS classes for styling
            }
        }
    )

    context = {
        "BAKE_MODE": settings.BAKE_MODE,
        "doc_root": "../",
        "html_content": html_content,
        "available_modules": get_available_modules(),
    }

    return render(request, "examples.html", context)

def tools_view(request):

    # Tool 1
    tool_one_note_input = int(request.GET.get("tool-one-note-input", 0))
    tool_one_key_type_input = int(request.GET.get("tool-one-key-type-input", 0))

 

    n = parse_note(tool_one_note_input)
    kt = parse_key_type(tool_one_key_type_input) 


    key_generator_results = mt.Key(n, kt).to_string_array(dominant=True, parallel=True)



 


    # Tool 2
    tool_two_note_input = int(request.GET.get("tool-two-note-input", 0))
    
    mode_generator_results = [str(m) for m in modes_from_note(mt.Note.from_index(tool_two_note_input))] 
 


    context = {
        "available_modules": get_available_modules(),

        "notes": mt.Note.items(),
        "key_types": mt.KeyType.items(),
        "key_generator_results": "\n".join(key_generator_results),

        # Tool 1
        "tool_one_note_input": tool_one_note_input,
        "tool_one_key_type_input": tool_one_key_type_input,

        # Tool 2
        "mode_generator_results": "\n".join(mode_generator_results),
        "tool_two_note_input": tool_two_note_input,
    }

    return render(request, "tools.html", context)
# Python
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

def build_dynamic_doc_structure(module):
    module_doc = ModuleDoc(module)

    doc_structure = {
        "functions": [],
        "classes": []
    }

    for f in module_doc.functions:
        doc_structure["functions"].append({
            "name": f.name,
            "tag": "h2",
            "anchor": f"function-{f.name}",
            "docstring": mark_safe(f.docstring),
        })

    for c in module_doc.classes:
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
        "html_content": html_content
    }

    return render(request, "documentation.html", context)


def notes_view(request):
    module = mt.notes

    context = {
        "module_name": module.__name__,
        "doc_structure": build_dynamic_doc_structure(module),
    }

    return render(request, "notes.html", context)

def scales_view(request):
    module = mt.scales

    context = {
        "module_name": module.__name__,
        "doc_structure": build_dynamic_doc_structure(module),
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
        "html_content": html_content,
    }

    return render(request, "examples.html", context)
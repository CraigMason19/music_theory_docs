# Python
from pathlib import Path
import logging
import pkgutil
import re

# Django
from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponseNotFound, JsonResponse
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
        "doc_root": "",
        "html_content": html_content,
    }

    return render(request, "documentation.html", context)

def module_view(request, module_name):
    module = getattr(mt, module_name)
    
    if module is None:
        raise Http404(f"No such module: {module_name}")

    context = {
        "doc_root": "../",
        "module_name": module_name,
        "doc_structure": build_dynamic_doc_structure(module),
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
        "doc_root": "../",
        "html_content": html_content,
    }

    return render(request, "examples.html", context)


def mnemonics_view(request):
    """
    Displays the mnemonics Markdown file
    """
    md_path = Path(__file__).parent.parent / "static" / "Markdown" / "mnemonics.md"

    if not md_path.exists():
        return HttpResponseNotFound(md_path)      
 
    raw_md = md_path.read_text(encoding="utf-8")

    html_content = markdown.markdown(
        raw_md, 
        extensions=["fenced_code", "codehilite", "tables", "toc"],
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "noclasses": True  # Use CSS classes for styling
            }
        }
    )

    context = {
        "doc_root": "../",
        "html_content": html_content,
    }

    return render(request, "mnemonics.html", context)


def tools_view(request):
    is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    # Return the page, skip calculations
    if not is_ajax_request:
        context = {
            "doc_root": "../",

            "notes": mt.Note.items(),
            "key_types": mt.KeyType.items(),

            "tool_three_tuning_input_one": mt.Note.E.value,
            "tool_three_tuning_input_two": mt.Note.B.value,
            "tool_three_tuning_input_three": mt.Note.G.value,
            "tool_three_tuning_input_four": mt.Note.D.value,
            "tool_three_tuning_input_five": mt.Note.A.value,
            "tool_three_tuning_input_six": mt.Note.E.value,
        }

        return render(request, "tools.html", context)

    # Tool 1 - Chords in key generator
    tool_one_note_input = int(request.GET.get("tool-one-note-input", mt.Note.C.value))
    tool_one_key_type_input = int(request.GET.get("tool-one-key-type-input", mt.KeyType.Major.value))
    tool_one_dominant_input = request.GET.get("tool-one-dominant-input", "true")
    tool_one_parallel_input = request.GET.get("tool-one-parallel-input", "true") 

    n = parse_note(tool_one_note_input)
    kt = parse_key_type(tool_one_key_type_input) 
    d = parse_bool(tool_one_dominant_input)
    p = parse_bool(tool_one_parallel_input)

    key_generator_results = mt.Key(n, kt).to_string_array(dominant=d, parallel=p)

    # Tool 2 - Modes from note generator
    tool_two_note_input = int(request.GET.get("tool-two-note-input", 0))
    mode_generator_results = [str(m) for m in modes_from_note(parse_note(tool_two_note_input))] 

    # Tool 3 - Note Finder
    tool_three_tuning_input_one = int(request.GET.get("tool-three-tuning-input-one", mt.Note.E.value))
    tool_three_tuning_input_two = int(request.GET.get("tool-three-tuning-input-two", mt.Note.B.value))
    tool_three_tuning_input_three = int(request.GET.get("tool-three-tuning-input-three", mt.Note.G.value))
    tool_three_tuning_input_four = int(request.GET.get("tool-three-tuning-input-four", mt.Note.D.value))
    tool_three_tuning_input_five = int(request.GET.get("tool-three-tuning-input-five", mt.Note.A.value))
    tool_three_tuning_input_six = int(request.GET.get("tool-three-tuning-input-six", mt.Note.E.value))

    tool_three_fret_input_one = request.GET.get("tool-three-fret-input-one", 0)
    tool_three_fret_input_two = request.GET.get("tool-three-fret-input-two", 0)
    tool_three_fret_input_three = request.GET.get("tool-three-fret-input-three", 0)
    tool_three_fret_input_four = request.GET.get("tool-three-fret-input-four", 0)
    tool_three_fret_input_five = request.GET.get("tool-three-fret-input-five", 0)
    tool_three_fret_input_six = request.GET.get("tool-three-fret-input-six", 0)

    guitar = mt.StringInstrument([
        parse_note(tool_three_tuning_input_six),
        parse_note(tool_three_tuning_input_five),
        parse_note(tool_three_tuning_input_four),
        parse_note(tool_three_tuning_input_three),
        parse_note(tool_three_tuning_input_two),
        parse_note(tool_three_tuning_input_one),
    ])

    def note_name_at_fret(string_index: int, fret_input: str) -> str:
        try:
            if fret_input in ["x", "X"]:
                return 'X'
            
            value = int(fret_input)
            result = guitar.note_at_fret(string_index, value)

            if value < 0:
                messages.error(request, f"Fret value must be must be a interger number 0 or above: {value}")

            return str(result)

        except ValueError:
            messages.error(request, f"Cannot convert '{fret_input}' into a number. Fret value must be must be a interger number 0 or above")
            return 'X'
        
        
    tool_three_result_one = note_name_at_fret(5, tool_three_fret_input_one)
    tool_three_result_two = note_name_at_fret(4, tool_three_fret_input_two)
    tool_three_result_three = note_name_at_fret(3, tool_three_fret_input_three)
    tool_three_result_four = note_name_at_fret(2, tool_three_fret_input_four)
    tool_three_result_five = note_name_at_fret(1, tool_three_fret_input_five)
    tool_three_result_six = note_name_at_fret(0, tool_three_fret_input_six)

    message_list = [{ "tags": m.tags, "text": m.message } for m in messages.get_messages(request)]

    response = {
        "chords_in_key_generator_results": key_generator_results,
        "mode_generator_results": mode_generator_results,

        "tool_three_result_one": tool_three_result_one,
        "tool_three_result_two": tool_three_result_two,
        "tool_three_result_three": tool_three_result_three,
        "tool_three_result_four": tool_three_result_four,
        "tool_three_result_five": tool_three_result_five,
        "tool_three_result_six": tool_three_result_six,

        "messages": message_list,
    }

    return JsonResponse(response)
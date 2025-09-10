from enum import Enum
from pathlib import Path
import shutil

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

import urllib.request

from documentation_app.source.mt_modules import get_available_modules

BAKE_DIR = Path("docs")

CSS_DIR = Path("static", "CSS")
CSS_BLACKLIST = [
    "backend-styles.css",
]

JS_DIR = Path("static", "JS")
JSS_BLACKLIST = [
]

class Asset(Enum):
    CSS = 1
    JS = 2 


def bakeAsset(request, asset: Asset, ignore_list: list[str]) -> bool:
    try:
        if asset == Asset.CSS:
            shutil.copytree(CSS_DIR, BAKE_DIR / "CSS", ignore=shutil.ignore_patterns(*ignore_list), dirs_exist_ok=True)
            messages.success(request, "CSS pages baked successfully")

        elif asset == Asset.JS:
            shutil.copytree(JS_DIR, BAKE_DIR / "JS", ignore=shutil.ignore_patterns(*ignore_list), dirs_exist_ok=True)
            messages.success(request, "JS scripts baked successfully")

        else:
            raise ValueError(f"Unknown asset type: {asset}")
        
        return True
    
    except Exception as e:
        messages.error(request, f"Bake failed for {asset.name}: {e}")

        return False
    
def bakeHTML(request) -> bool:
    try:
        # index exception
        django_url = f"http://{settings.DEFAULT_PORT}/documentation"
        html = urllib.request.urlopen(django_url).read().decode("utf-8")

        output_path = (Path(__file__).parent.parent / "docs" /  "index").with_suffix(".html")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")





        # examploes
        django_url = f"http://{settings.DEFAULT_PORT}/documentation/examples"
        html = urllib.request.urlopen(django_url).read().decode("utf-8")

        output_path = (Path(__file__).parent.parent / "docs" / "documentation" / "examples").with_suffix(".html")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")




        pages = get_available_modules()

        for page in pages:
            django_url = f"http://{settings.DEFAULT_PORT}/documentation/{page}"
            html = urllib.request.urlopen(django_url).read().decode("utf-8")

            output_path = (Path(__file__).parent.parent / "docs" / "documentation" / page).with_suffix(".html")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        messages.success(request, "HTML pages baked successfully")
        return True

    except Exception as e:
        messages.error(request, f"Bake failed for {django_url}:\n {e}")
        return False

    
def bake(request) -> bool:
    settings.BAKE_MODE = True

    results = [
        bakeAsset(request, Asset.CSS, CSS_BLACKLIST),
        # bakeAsset(request, Asset.JS, JSS_BLACKLIST),
        bakeHTML(request)
    ]
    
    settings.BAKE_MODE = False

    return all(results)


def bake_view(request):
    if request.method == "POST":       
        bake(request)
        
        return redirect("bake_view")
    
    return render(request, "bake.html")
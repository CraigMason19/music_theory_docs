from enum import Enum
from pathlib import Path
import shutil

from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

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

        elif asset == Asset.JS:
            shutil.copytree(JS_DIR, BAKE_DIR / "JS", ignore=shutil.ignore_patterns(*ignore_list), dirs_exist_ok=True)

        else:
            raise ValueError(f"Unknown asset type: {asset}")
        
        return True
    
    except Exception as e:
        messages.error(request, f"Bake failed for {asset.name}: {e}")

        return False
    
    
def bake(request) -> bool:
    results = [
        bakeAsset(request, Asset.CSS, CSS_BLACKLIST),
        # bakeAsset(request, Asset.JS, JSS_BLACKLIST),
    ]
    
    return all(results)


def bake_view(request):
    if request.method == "POST":       
        if bake(request):
            messages.success(request, "Assets baked successfully.")
        else:
            messages.warning(request, "Some assets failed to bake.")
        
        return redirect("bake_view")
    
    return render(request, "bake.html")
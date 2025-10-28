from django.shortcuts import render
import requests


def home(request):
    books = []
    query = ""
    if request.method == "POST":
        query = request.POST.get("query", "").strip()
        if query:
            url = f"https://www.googleapis.com/books/v1/volumes?q={requests.utils.requote_uri(query)}"
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                data = r.json()
                items = data.get("items", [])
                for item in items[:8]:
                    info = item.get("volumeInfo", {})
                    books.append({
                        "title": info.get("title", "No title"),
                        "authors": ", ".join(info.get("authors", ["Unknown"])),
                        "description": (info.get("description") or "")[:300],
                        "info_link": info.get("infoLink", "#")
                    })
            except Exception:
                books = []
    return render(request, "index.html", {"books": books, "query": query})


import urllib.request
import re

def check_url(url):
    print(f"=== CHECKING {url} ===")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Check for Mejoras Académicas
        print("Contains 'Mejoras':", "Mejoras" in html)
        print("Contains 'Mejoras Académicas':", "Mejoras Académicas" in html)
        
        # Check for book details box
        print("Contains 'book-details-box':", "book-details-box" in html)
        print("Contains 'Economics: The User':", "Economics: The User" in html)
        
        # Search for all links containing "mejoras" or "etapas"
        links = re.findall(r'href="([^"]+)"', html)
        mejoras_links = [l for l in links if 'mejoras' in l.lower()]
        print("Mejoras links:", mejoras_links)
        
        # Print first few navigation items
        matches = re.findall(r'<span class="md-ellipsis">\s*([^<]+?)\s*</span>', html)
        print("First 20 nav items:", matches[:20])
    except Exception as e:
        print(f"Error checking {url}: {e}")

check_url("https://mrspagvi.github.io/Curso/")
check_url("https://mrspagvi.github.io/Curso/etapas/etapa-20-chang-economia-99/")

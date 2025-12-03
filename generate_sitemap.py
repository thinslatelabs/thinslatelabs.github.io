import os
import datetime

BASE_URL = "https://thinslatelabs.github.io"
ROOT_DIR = "/Users/vasanthsriram/Documents/thinslatelabs.github.io"

def generate_sitemap():
    pages = []
    
    # Add homepage
    pages.append({
        "loc": f"{BASE_URL}/",
        "lastmod": datetime.date.today().isoformat(),
        "priority": "1.0"
    })
    
    # Add blog pages
    blog_dir = os.path.join(ROOT_DIR, "blog")
    if os.path.exists(blog_dir):
        for filename in os.listdir(blog_dir):
            if filename.endswith(".html"):
                # Calculate priority
                priority = "0.8" if filename == "index.html" else "0.6"
                
                # Calculate URL
                if filename == "index.html":
                    url = f"{BASE_URL}/blog/"
                else:
                    url = f"{BASE_URL}/blog/{filename}"
                
                pages.append({
                    "loc": url,
                    "lastmod": datetime.date.today().isoformat(),
                    "priority": priority
                })

    # Generate XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += '  <url>\n'
        xml += f'    <loc>{page["loc"]}</loc>\n'
        xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w") as f:
        f.write(xml)
    
    print(f"Generated sitemap with {len(pages)} URLs.")

if __name__ == "__main__":
    generate_sitemap()

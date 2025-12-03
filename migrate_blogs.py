import os
import re
import shutil

SOURCE_DIR = "/Users/vasanthsriram/Documents/oktonote.github.io/blog"
DEST_DIR = "/Users/vasanthsriram/Documents/thinslatelabs.github.io/blog"
IMAGES_DEST_DIR = "/Users/vasanthsriram/Documents/thinslatelabs.github.io/images/blog"

HEADER_TEMPLATE = """
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <a href="../index.html" class="logo">Thinslate Labs</a>
            <ul class="nav-links">
                <li><a href="../index.html#about">About</a></li>
                <li><a href="../index.html#products">Products</a></li>
                <li><a href="../index.html#contact">Contact</a></li>
                <li><a href="./index.html" style="color: var(--primary-blue);">Blog</a></li>
            </ul>
        </nav>
    </header>
"""

FOOTER_TEMPLATE = """
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">Thinslate Labs, LLC</div>
                <p class="footer-description">
                    Building innovative software tools that enhance productivity and simplify digital workflows.
                </p>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Thinslate Labs, LLC. All rights reserved.</p>
            </div>
        </div>
    </footer>
"""

def migrate():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.html')]
    
    print(f"Found {len(files)} HTML files to migrate.")

    for filename in files:
        source_path = os.path.join(SOURCE_DIR, filename)
        dest_path = os.path.join(DEST_DIR, filename)
        
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Replace Handlebars partials
        content = content.replace('{{> header}}', HEADER_TEMPLATE)
        content = content.replace('{{> footer}}', FOOTER_TEMPLATE)
        
        # 2. Update CSS links
        # Remove existing css links and inject ours
        content = re.sub(r'<link rel="stylesheet" href="/assets/css/.*">', '', content)
        
        # Inject Thinslate styles + Blog styles in head
        style_injection = """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/feather-icons"></script>
    <link rel="stylesheet" href="../css/blog.css">
    <style>
        /* Critical styles from main index.html needed for header/footer */
        :root {
            --primary-blue: #2563eb;
            --secondary-purple: #7c3aed;
            --dark-gray: #1f2937;
            --light-gray: #f8fafc;
            --medium-gray: #64748b;
            --white: #ffffff;
            --success: #10b981;
            --border-color: #e2e8f0;
        }
        body { font-family: 'Inter', sans-serif; color: var(--dark-gray); }
        .header { background: white; border-bottom: 1px solid var(--border-color); padding: 1rem 0; }
        .nav { display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
        .logo { font-size: 1.5rem; font-weight: 700; color: var(--primary-blue); text-decoration: none; }
        .nav-links { display: flex; gap: 2rem; list-style: none; }
        .nav-links a { color: var(--medium-gray); text-decoration: none; font-weight: 500; }
        .nav-links a:hover { color: var(--primary-blue); }
        .footer { background: var(--dark-gray); color: white; padding: 3rem 0; text-align: center; margin-top: auto;}
        .footer-logo { font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; }
        .footer-description { color: #9ca3af; margin-bottom: 2rem; max-width: 400px; margin-left: auto; margin-right: auto; }
        .footer-bottom { border-top: 1px solid #374151; padding-top: 2rem; font-size: 0.9rem; color: #9ca3af; }
        
        @media (max-width: 768px) { .nav-links { display: none; } }
    </style>
        """
        content = content.replace('</head>', style_injection + '\n</head>')
        
        # 3. Update Image Paths
        # /assets/images/ -> ../images/blog/
        content = content.replace('/assets/images/', '../images/blog/')
        
        # 4. Update Links
        # href="/" -> href="../index.html"
        content = content.replace('href="/"', 'href="../index.html"')
        
        # href="/blog/" -> href="./index.html"
        content = content.replace('href="/blog/"', 'href="./index.html"')
        
        # href="/blog/some-post" -> href="./some-post.html" (assuming links don't have .html extension in source but files do)
        # This is tricky. Oktonote might use clean URLs.
        # Let's look at a sample link: <a href="/blog/quickest-way-capture-thoughts">
        # We need to append .html if it's missing
        
        def fix_blog_link(match):
            path = match.group(1)
            if path == "" or path == "/":
                return 'href="./index.html"'
            if not path.endswith('.html'):
                return f'href="./{path}.html"'
            return f'href="./{path}"'

        content = re.sub(r'href="/blog/([^"]*)"', fix_blog_link, content)
        
        # Fix other absolute paths
        content = content.replace('href="/features"', 'href="../index.html#products"')
        content = content.replace('href="/#download"', 'href="../index.html#products"')
        
        # 5. Remove OktoNote specific scripts/favicons if needed, or adapt them
        # For now, we leave them but might want to update favicon
        
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Migrated {filename}")

if __name__ == "__main__":
    migrate()

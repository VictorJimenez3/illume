import re

def protect_latex(text):
    """
    Temporarily replace LaTeX content with placeholders to protect it during cleaning
    Returns: (modified_text, latex_fragments)
    """
    latex_patterns = [
        r'\\\[.*?\\\]',           # Display math mode
        r'\\\(.*?\\\)',           # Inline math mode
        r'\$\$.*?\$\$',          # Double dollar display math
        r'\$.*?\$',              # Single dollar inline math
        r'\\begin\{.*?\}.*?\\end\{.*?\}' # Environment blocks
    ]
    
    protected = []
    placeholder_template = "LATEX_PLACEHOLDER_{}"
    
    for pattern in latex_patterns:
        matches = re.finditer(pattern, text, re.DOTALL)
        for i, match in enumerate(matches):
            placeholder = placeholder_template.format(len(protected))
            text = text.replace(match.group(0), placeholder)
            protected.append(match.group(0))
            
    return text, protected

def restore_latex(text, protected):
    """Restore LaTeX content from placeholders"""
    for i, latex in enumerate(protected):
        text = text.replace(f"LATEX_PLACEHOLDER_{i}", latex)
    return text

def clean_wiki_content(text):
    print("Cleaning wiki content...")

    # First protect LaTeX content
    text, protected_latex = protect_latex(text)
    
    # Remove CSS/HTML style blocks
    text = re.sub(r'@media.*?}', '', text, flags=re.DOTALL)
    text = re.sub(r'\.mw-parser-output.*?}', '', text)
    
    # Remove HTML tags more thoroughly
    text = re.sub(r'<(?!math)[^>]+>', '', text)  # Keep <math> tags
    text = re.sub(r'</.*?>', '', text)  # Remove closing tags
    
    # Remove wiki-specific formatting
    text = re.sub(r'\[\[.*?\]\]', '', text)  # Remove wiki links
    text = re.sub(r'\{\{.*?\}\}', '', text)  # Remove templates
    
    # Remove special formatting
    text = re.sub(r'\\displaystyle', '', text)
    text = re.sub(r'\\mathbb', '', text)
    
    # Clean up navigation and metadata
    text = re.sub(r'Navigation.*?Contents', '', text, flags=re.DOTALL)
    text = re.sub(r'Retrieved from.*?$', '', text, flags=re.DOTALL)
    text = re.sub(r'Categories:.*?$', '', text, flags=re.DOTALL)
    
    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple newlines to double
    text = re.sub(r' +', ' ', text)  # Multiple spaces to single
    text = re.sub(r'\t+', ' ', text)  # Tabs to space
    
    # Remove edit links and reference markers
    text = re.sub(r'\[edit\]', '', text)
    text = re.sub(r'\[(\d+)\]', r'[ref\1]', text)
    
    # Restore protected LaTeX content
    text = restore_latex(text, protected_latex)
    
    return text.strip()
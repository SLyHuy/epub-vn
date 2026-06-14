import sys
import zipfile
import re
import argparse
import os
from bs4 import BeautifulSoup, NavigableString

# Define abbreviations that should not have their inner dots touched
# e.g., Tp.HCM, PGS.TS., ThS.
SPECIAL_DOT = "«DOT»"
ABBREVIATIONS = {
    'Tp.HCM': f'Tp{SPECIAL_DOT}HCM',
    'PGS.TS.': f'PGS{SPECIAL_DOT}TS.',
    'PGS.TS': f'PGS{SPECIAL_DOT}TS',
    'GS.TS.': f'GS{SPECIAL_DOT}TS.',
    'GS.TS': f'GS{SPECIAL_DOT}TS',
    'ThS.BS.': f'ThS{SPECIAL_DOT}BS.',
    'ThS.BS': f'ThS{SPECIAL_DOT}BS',
    'Ths.Bs.': f'Ths{SPECIAL_DOT}Bs.',
    'Ths.Bs': f'Ths{SPECIAL_DOT}Bs',
    'BS.CK': f'BS{SPECIAL_DOT}CK',
    'U.S.A': f'U{SPECIAL_DOT}S{SPECIAL_DOT}A',
}

def process_text(text):
    if not text.strip():
        return text

    placeholders = {}
    
    def add_placeholder(match):
        key = f"__PH_{len(placeholders)}__"
        placeholders[key] = match.group(0)
        return key

    # 1. Protect URLs, Emails
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', add_placeholder, text)
    text = re.sub(r'(https?://|www\.)\S+', add_placeholder, text)
    text = re.sub(r'\b[a-zA-Z0-9.-]+\.(com|vn|net|org|edu|gov|io|info)\b', add_placeholder, text)
    
    # 2. Protect Decimals and hierarchical numbers (e.g., 3.14, 1.2.3, 1,000)
    text = re.sub(r'\b\d+(?:[,.]\d+)+\b', add_placeholder, text)
    
    # 3. Protect specific abbreviations (inner dots only)
    for k, v in ABBREVIATIONS.items():
        text = text.replace(k, v)
        
    # 4. Main regex for punctuation spacing
    def repl_space(match):
        before = match.group(1)
        punct = match.group(2)
        
        # Opening quotes exception
        if punct in ['"', "'", '“', '‘']:
            if not before or before.isspace() or before in ['(', '[', '{', '"', "'", '“', '‘']:
                return f"{before}{punct}"
                
        # Otherwise, add space
        return f"{before}{punct} "

    # Pattern: 
    # (^|.) -> Capture preceding char or empty if start of string
    # ([.,:;!?\)"\]\}\'”’]) -> Capture punctuation
    # (?=[^\W_]) -> Lookahead for word char (letters/numbers, supports unicode). Doesn't consume it.
    text = re.sub(r'(^|.)([.,:;!?\)"\]\}\'”’])(?=[^\W_])', repl_space, text)
    
    # 5. Restore abbreviations
    text = text.replace(SPECIAL_DOT, '.')
    
    # 6. Restore placeholders
    # We iterate in reverse order to avoid nested placeholder issues (though unlikely here)
    for key, val in reversed(placeholders.items()):
        text = text.replace(key, val)
        
    return text


def process_html(html_content):
    # Parse HTML. We must use 'xml' (lxml) to preserve XML declarations and XHTML syntax (like self-closing tags).
    soup = BeautifulSoup(html_content, 'xml')
    
    # Find all text nodes
    for text_node in soup.find_all(text=True):
        # Skip empty or whitespace-only nodes
        if not text_node.strip():
            continue
            
        # Do not modify text inside <style> or <script> tags
        if text_node.parent.name in ['style', 'script']:
            continue
            
        original_text = str(text_node)
        new_text = process_text(original_text)
        
        if new_text != original_text:
            text_node.replace_with(NavigableString(new_text))
            
    # Return as string, ensuring we keep the original encoding
    return str(soup)


def fix_epub(input_path, output_path):
    print(f"[*] Processing: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"[!] Error: File '{input_path}' not found.")
        return

    # Open the original epub
    with zipfile.ZipFile(input_path, 'r') as zin:
        # Create the new epub
        with zipfile.ZipFile(output_path, 'w') as zout:
            
            # 1. Handle mimetype first (MUST be uncompressed and first entry)
            if 'mimetype' in zin.namelist():
                print(" -> Writing mimetype (uncompressed)")
                mimetype_content = zin.read('mimetype')
                zout.writestr('mimetype', mimetype_content, compress_type=zipfile.ZIP_STORED)
            else:
                print("[!] Warning: No 'mimetype' file found in EPUB. It might not be a valid EPUB.")
                
            # 2. Process all other files
            for item in zin.infolist():
                if item.filename == 'mimetype':
                    continue
                    
                content = zin.read(item.filename)
                
                # Check if it's an HTML/XHTML file
                if item.filename.lower().endswith(('.html', '.xhtml', '.htm')):
                    print(f" -> Fixing punctuation in: {item.filename}")
                    try:
                        # Decode, process, then re-encode
                        html_str = content.decode('utf-8')
                        fixed_html_str = process_html(html_str)
                        content = fixed_html_str.encode('utf-8')
                    except Exception as e:
                        print(f"[!] Error processing {item.filename}: {e}. Copying original.")
                
                # Write to output zip (compressed)
                zout.writestr(item, content, compress_type=zipfile.ZIP_DEFLATED)
                
    print(f"[*] Success! Saved corrected EPUB to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix missing spaces after Vietnamese punctuation in EPUB files.")
    parser.add_argument("input", help="Path to the input EPUB file")
    parser.add_argument("output", help="Path to save the output EPUB file")
    
    args = parser.parse_args()
    
    fix_epub(args.input, args.output)

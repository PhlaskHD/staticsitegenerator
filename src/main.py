from textnode import *
from htmlnode import *
from markdowntohtml import *
import re, os, shutil

def main():
    static_to_public("static", "public")
    
    generate_pages_recursive("content", "template.html", "public")



def static_to_public(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    for each in os.listdir(source_dir):
        source_path = os.path.join(source_dir, each)
        dest_path = os.path.join(dest_dir, each)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            os.mkdir(dest_path)
            static_to_public(source_path, dest_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for each in lines:
        if each[0:2] == "# ":
            return each[2:].strip()
        else:
            raise Exception("No h1 header")
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown_raw = file.read()
    with open(template_path) as file:
        template_raw = file.read()
    markdown = markdown_to_html_node(markdown_raw)
    markdown_node = markdown.to_html()
    title = extract_title(markdown_raw)
    final_html = template_raw.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", markdown_node)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # List all entries in the directory
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        # Full path to the current entry
        full_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(full_path) and entry.endswith('.md'):
            # It's a markdown file - generate HTML
            
            # Calculate the relative path from dir_path_content
            relative_path = os.path.relpath(full_path, dir_path_content)
            
            # Create destination path (changing .md to .html)
            dest_path = os.path.join(dest_dir_path, relative_path.replace('.md', '.html'))
            
            # Make sure the destination directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Generate the HTML page using your existing function
            generate_page(full_path, template_path, dest_path)
            
        elif os.path.isdir(full_path):
            # It's a directory - recursively process it
            new_dest_dir = os.path.join(dest_dir_path, entry)
            
            # Create the directory if it doesn't exist
            os.makedirs(new_dest_dir, exist_ok=True)
            
            # Recursive call
            generate_pages_recursive(full_path, template_path, new_dest_dir)

main()
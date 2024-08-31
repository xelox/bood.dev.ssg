import shutil
import os

from textnode import md_to_html

def transfer_files():
    shutil.rmtree('public')
    shutil.copytree('static', 'public')

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as source_file:
        markdown_content = source_file.read()
        title, html = md_to_html(markdown_content)
        with open(template_path, 'r') as template_file:
            template = template_file.read()
            res = template.replace('{{ Title }}', title)
            res = res.replace('{{ Content }}', html)
            with open(dest_path, 'w') as dest_file:
                dest_file.write(res)

def generate_pages_recursively(src_dir, template_path, dest_dir):
    items = os.listdir(src_dir)
    for item in items:
        src_path = f'{src_dir}/{item}'
        dest_path = f'{dest_dir}/{item.replace('.md', '.html')}'
        if os.path.isfile(src_path):

            generate_page(src_path, template_path, dest_path)
        else:
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            generate_pages_recursively(src_path, template_path, dest_path)

def main():
    transfer_files()
    generate_pages_recursively('content', 'template.html', 'public')


if __name__ == "__main__":
    main()

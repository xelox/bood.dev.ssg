import shutil

from textnode import md_to_html

def transfer_files():
    shutil.rmtree('public')
    shutil.copytree('static', 'public')

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown_content = file.read()
        print(md_to_html(markdown_content))

def main():
    transfer_files()
    generate_page('content/index.md', '', '')


if __name__ == "__main__":
    main()

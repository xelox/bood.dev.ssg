import shutil

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


        

def main():
    transfer_files()
    generate_page('content/index.md', 'template.html', 'public/index.html')


if __name__ == "__main__":
    main()

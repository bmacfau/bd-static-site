import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as to_file:
        to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Walk through every entry in the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for filename in files:
            if filename.endswith('.md'):
                markdown_file_path = os.path.join(root, filename)

                # Compute the path relative to the content directory
                relative_path = os.path.relpath(markdown_file_path, dir_path_content)

                # Determine the output directory and ensure it has the correct structure
                folder_path = os.path.dirname(relative_path)

                # Create the output folder path for the HTML file
                if filename == "index.md":
                    # Output directly to index.html within the folder
                    html_file_path = os.path.join(dest_dir_path, folder_path, 'index.html')
                else:
                    # Use the stem of the markdown filename for the folder structure
                    markdown_stem = Path(filename).stem
                    html_file_path = os.path.join(dest_dir_path, folder_path, markdown_stem, 'index.html')

                # Ensure the necessary directories exist
                os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

                # Call generate_page to generate the HTML file
                generate_page(markdown_file_path, template_path, html_file_path)
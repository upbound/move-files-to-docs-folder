import os
import yaml
import argparse

# Define the mkdocs.yml file
MKDOCS_YAML_FILE = 'mkdocs.yml'

# Function to recursively get all markdown files in a directory, skipping hidden directories
def get_markdown_files(directory):
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(".md"):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                markdown_files.append(relative_path.replace('\\', '/'))
    return markdown_files

# Function to generate the navigation section for mkdocs.yml while preserving directory structure
def generate_nav(markdown_files):
    nav = {}
    for md_file in markdown_files:
        parts = md_file.split('/')
        current = nav
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = md_file

    def build_nav_dict(d):
        nav_list = []
        for key, value in d.items():
            if isinstance(value, dict):
                nav_list.append({key: build_nav_dict(value)})
            else:
                title = os.path.splitext(os.path.basename(value))[0].replace('-', ' ').title()
                nav_list.append({title: value})
        return nav_list

    return build_nav_dict(nav)

# Load existing mkdocs.yml, update nav, and save it back
def update_mkdocs_yaml(content_dir):
    # Get all markdown files
    markdown_files = get_markdown_files(content_dir)

    # Load existing mkdocs.yml
    with open(MKDOCS_YAML_FILE, 'r') as f:
        mkdocs_data = yaml.safe_load(f)

    # Update nav section
    mkdocs_data['nav'] = generate_nav(markdown_files)

    # Write the updated mkdocs.yml back
    with open(MKDOCS_YAML_FILE, 'w') as f:
        yaml.dump(mkdocs_data, f, sort_keys=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update mkdocs.yml with markdown files from a source directory.")
    parser.add_argument('source_dir', type=str, help="The source directory containing markdown files.")
    args = parser.parse_args()

    update_mkdocs_yaml(args.source_dir)
    print(f"Updated {MKDOCS_YAML_FILE} with all markdown files from {args.source_dir}")
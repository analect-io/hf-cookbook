import os
import re
import nbformat

def extract_pip_packages(notebook_path):
    pip_packages = []
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)
        for cell in nb.cells:
            if cell.cell_type == 'code':
                source = cell.source
                for line in source.split('\n'):
                    if 'pip install' in line:
                        packages = re.findall(r'pip\s+install\s+(-q\s+|-U\s+|--upgrade\s+|)([\w-]+(?:\s+[\w-]+)*)', line)
                        pip_packages.extend([pkg for _, pkgs in packages for pkg in pkgs.split()])
    return pip_packages

def main():
    notebooks_folder = 'notebooks/en'
    all_pip_packages = []
    for root, dirs, files in os.walk(notebooks_folder):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                pip_packages = extract_pip_packages(notebook_path)
                all_pip_packages.extend(pip_packages)

    unique_packages = list(set(all_pip_packages))
    unique_packages = [package for package in unique_packages if package not in ['--upgrade', '-U', '-q']]
    unique_packages.sort()

    with open('requirements.txt', 'w') as f:
        for package in unique_packages:
            f.write(f"{package}\n")

    print(f"Unique packages written to 'requirements.txt' file.")

if __name__ == '__main__':
    main()

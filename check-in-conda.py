import subprocess
from pathlib import Path

# Path to the requirements.txt file
requirements_path = Path("requirements.txt")

# List to store packages available in conda
conda_packages = []

# List to store packages not available in conda
non_conda_packages = []

# Read the packages from the requirements.txt file
with open(requirements_path, "r") as f:
    packages = [line.strip() for line in f.readlines()]

# Check each package for availability in conda
for package in packages:
    try:
        # Use the conda search command to check if the package is available
        subprocess.run(["conda", "search", "--info", package], check=True, capture_output=True)
        conda_packages.append(package)
    except subprocess.CalledProcessError:
        non_conda_packages.append(package)

# Print the packages available in conda
print("Packages available in conda:")
for package in conda_packages:
    print(f"- {package}")

# Print the packages not available in conda
print("\nPackages not available in conda:")
for package in non_conda_packages:
    print(f"- {package}")

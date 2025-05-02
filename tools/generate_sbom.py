import subprocess
import json
from datetime import datetime

def get_installed_packages():
    result = subprocess.run(
        ['dpkg-query', '-W', '-f=${binary:Package}\t${Version}\n'],
        capture_output=True,
        text=True
    )
    packages = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('\t')
            if len(parts) == 2:
                packages.append({"package": parts[0], "version": parts[1]})
    return packages

def save_sbom(packages):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"sbom-{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump({"generated_at": timestamp, "total": len(packages), "packages": packages}, f, indent=2)
    print(f"SBOM saved to {filename} with {len(packages)} packages.")

if __name__ == "__main__":
    print("Generating mini SBOM...")
    pkgs = get_installed_packages()
    save_sbom(pkgs)

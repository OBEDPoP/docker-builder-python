import os
import yaml
import subprocess
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def load_manifest():
    with open("manifest.yaml", "r") as file:
        return yaml.safe_load(file)

def list_required_files():
    required_files = []
    if os.path.exists("requirements.txt"):
        required_files.append("requirements.txt")
    if os.path.exists("package.json"):
        required_files.append("package.json")
    if os.path.exists("Pipfile"):
        required_files.append("Pipfile")
    if os.path.exists("pom.xml"):
        required_files.append("pom.xml")
    return required_files

def generate_dockerfile(manifest):
    appname = manifest.get("appname", "default_app")
    tag = manifest.get("tag", "latest")
    multistage = manifest.get("multistage", "no").lower() == "yes"
    expose = manifest.get("Expose", 8080)
    env_variables = manifest.get("Env Variables", [])
    
    dockerfile_content = """
    # Base Image
    FROM python:3.9 AS base
    WORKDIR /app
    
    """
    
    if multistage:
        dockerfile_content += """
        # Build Stage
        FROM base AS builder
        COPY . /app
        RUN pip install -r requirements.txt
        
        # Final Stage
        FROM base AS final
        COPY --from=builder /app /app
        """
    else:
        dockerfile_content += """
        COPY . /app
        RUN pip install -r requirements.txt
        """
    
    for env in env_variables:
        dockerfile_content += f"ENV {env['endpoint']}={env['pass']}\n"
    
    dockerfile_content += f"EXPOSE {expose}\n"
    dockerfile_content += "CMD [\"python\", \"app.py\"]"
    
    with open("Dockerfile", "w") as dockerfile:
        dockerfile.write(dockerfile_content)
    
    return appname, tag

def build_and_push_docker_image(appname, tag, registry_url=None, registry_username=None, registry_password=None):
    image_name = f"{registry_url}/{appname}:{tag}" if registry_url else f"{appname}:{tag}"
    subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
    
    if registry_url and registry_username and registry_password:
        subprocess.run(["docker", "login", registry_url, "-u", registry_username, "--password-stdin"], input=registry_password, text=True, check=True)
        subprocess.run(["docker", "push", image_name], check=True)
    
    return image_name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        manifest = load_manifest()
        appname, tag = generate_dockerfile(manifest)
        required_files = list_required_files()
        
        registry_url = request.form.get("registry_url")
        registry_username = request.form.get("registry_username")
        registry_password = request.form.get("registry_password")
        
        image_name = build_and_push_docker_image(appname, tag, registry_url, registry_username, registry_password)
        
        return render_template("index.html", message="Docker image built successfully", image=image_name, required_files=required_files)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

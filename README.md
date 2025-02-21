# docker-builder-python
this is application version of the github workflow https://github.com/OBEDPoP/container-builder-pipeline/actions/workflows/docker-image.yml

# Docker Builder App

## Overview

The **Docker Builder App** is a Flask-based web application that automates the process of building Docker images using a manifest file. It supports both **single-stage** and **multi-stage** builds, allowing users to define their Docker image configurations in a `manifest.yaml` file. Users can input their repository details, configure the build, and either push the image to a container registry or download it.

## Features

- **Automatic Dockerfile Generation**: Creates a `Dockerfile` dynamically based on the `manifest.yaml` file.
- **Multi-Stage Build Support**: Uses multi-stage builds when specified in the manifest.
- **UI for Input**: Simple web interface for entering GitHub and registry details.
- **Registry Integration**: Push images to a registry (Artifactory, DockerHub, etc.) if details are provided.
- **Download Option**: Allows users to download the built image if no registry details are provided.
- **Dependency Check**: Detects required files like `requirements.txt`, `package.json`, etc.

## Project Structure

```
/docker-builder-python
│── /templates
│   ├── index.html  # UI for user input
│── app.py  # Main Flask application
│── manifest.yaml  # Configuration file for Docker builds
│── requirements.txt  # Dependencies for Flask and YAML processing
│── Dockerfile  # Generated dynamically by the app
```



## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Docker
- Git

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/docker-builder-app.git
   cd docker-builder-app
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the Flask application:
   ```sh
   python app.py
   ```
4. Open a web browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

1. **Ensure the ****************`manifest.yaml`**************** file is configured**.
2. **Enter inputs in the UI**, including:
   - GitHub repository details
   - Container registry details (optional)
3. **Trigger the Docker build process**.
4. **Monitor progress** in the UI.
5. **Download the built image** if no registry is provided.

## Manifest File Format

Example `manifest.yaml`:

```yaml
- appname: docker_build_app
  tag: docker_build_app:latest
  multistage: yes
  Expose: 3000
  Env Variables:
    - endpoint: docker.io
      pass: {xxxxxxxxxx.key.com}
```

## Contributing

Feel free to contribute by submitting issues or pull requests!

## License

MIT License. See `LICENSE` file for details.




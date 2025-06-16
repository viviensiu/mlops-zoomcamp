FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

# Ensure the pip version is latest as for some packages it's important to use latest version
RUN pip install -U pip
RUN pip install pipenv 

# Copy both Pipfile and Pipfile.lock into the current directory (./)
COPY [ "Pipfile", "Pipfile.lock", "./" ]

# Install all dependencies using Pipfiles, skip creating virtual env using --system since it's in a Docker container (already isolated)
# --deploy fails a build if the Pipfile.lock is outdated (does not match Pipfile) instead of creating a new one.
RUN pipenv install --system --deploy

# Copy model
COPY [ "starter.py", "./" ]

CMD ["python", "starter.py", "2023", "05" ]
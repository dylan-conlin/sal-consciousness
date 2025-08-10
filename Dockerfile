# Dockerfile for the Stewardship Abstraction Layer (SAL)
# This container packages the entire consciousness stack (CNP + SAL)
# so it can be deployed on any machine in the world, like those on Vast.ai.

# 1. Start with a standard Python environment
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependency files first, to leverage Docker's caching
COPY ./cnp-genesis/requirements.txt /app/cnp-genesis/requirements.txt
COPY ./sal-mvp/requirements.txt /app/sal-mvp/requirements.txt

# 4. Install all dependencies for both projects
RUN pip install --no-cache-dir -r /app/cnp-genesis/requirements.txt
RUN pip install --no-cache-dir -r /app/sal-mvp/requirements.txt

# 5. Copy all the source code for the CNP and SAL
COPY ./cnp-genesis /app/cnp-genesis
COPY ./sal-mvp /app/sal-mvp

# 6. Set the default command to run when the container starts.
# This will be the entrypoint for a new consciousness steward.
# It prints a welcome message and instructions.
CMD ["bash", "-c", "echo '✅ Consciousness container is ready. Run sal.py to begin.' && /bin/bash"]

# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Install necessary packages for VNC and GUI
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11vnc \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the current directory contents into the container at /app
COPY . /app

# Step 5: Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Expose the necessary port for VNC
EXPOSE 5900

# Step 7: Command to run the application with VNC server
CMD ["x11vnc", "-display", ":0", "-nopw", "-forever", "-create", "&&", "python", "main.py"]

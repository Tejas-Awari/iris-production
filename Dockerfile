# 1. Start with a lightweight Python Linux image
# (We use "slim" to keep the file size small)
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependencies first!
# (Senior Tip: This allows Docker to "cache" the installation step.
# If you only change your code, you won't have to re-install pip packages)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. The command to run when the container starts
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
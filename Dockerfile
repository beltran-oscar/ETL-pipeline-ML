# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the poetry files
COPY pyproject.toml poetry.lock /app/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry lock
RUN poetry install

# Install Streamlit, Matplotlib, DuckDB
RUN pip install streamlit
RUN pip install matplotlib
RUN pip install duckdb

# Copy the .env file
#COPY .env /app/

# Copy the rest of the application code
COPY . .

# Copy the application code from the subfolder
COPY src/data/air_data.duckdb /app/
COPY src/app/app_ploomber.py /app/

# Extract data for app
## RUN poetry run ploomber build

# Expose the port that the app runs on
EXPOSE 8501

# Execute the script when the container starts
#CMD ["poetry", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["streamlit", "run", "app_ploomber.py", "--server.port=8501", "--server.address=0.0.0.0"]
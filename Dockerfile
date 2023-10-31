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

# Install required packages
RUN pip install streamlit
RUN pip install matplotlib
RUN pip install duckdb
RUN pip install statsmodels
RUN pip install python-dotenv

# Copy the .env file
COPY .env /app/

# Copy the rest of the application code
COPY . .

# Copy the application code from the subfolder
COPY src/app/app_ploomber.py /app/
COPY src/notebooks/ML/arima_model.pkl /app/

# Expose the port that the app runs on
EXPOSE 5000

# Execute the script when the container starts
CMD ["streamlit", "run", "app_ploomber.py", "--server.port=80", "--server.address=0.0.0.0"]
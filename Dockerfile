# Dockerfile
# Part 1: Setting up the environment variables

FROM python:3.9-slim

# Copy the configuration files to the working directory

COPY config.ini .

# Set environment variables
ENV TELEGRAM_ACCESS_TOKEN=6139479735:AAEdFqQ0Ag0Vj1yI3bamfAGBm0qxImyPQdI \
    AZURE_SQL_SERVER=mysqlserver-chatbot10.database.windows.net \
    AZURE_SQL_DATABASE=chatbot10db \
    AZURE_SQL_USER=azureuser \
    AZURE_SQL_PASSWORD=user1234! \
    AZURE_SQL_DRIVER='{ODBC Driver 17 for SQL Server}' \
    SPOTIFY_CLIENT_ID=b6d6e36d30984e708d5f614b6973adac \
    SPOTIFY_CLIENT_SECRET=2b3b7da8e54b4e76b285f6a099da41f1
    NEWS_API_KEY=128751e4fa07497b90cd74943ea543fb




# Part 2: Installing dependencies and configuring ODBC

FROM python:3.9-slim

# Install ODBC and FreeTDS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        unixodbc \
        unixodbc-dev \
        freetds-bin \
        freetds-dev \
        tdsodbc \
        && rm -rf /var/lib/apt/lists/

# Set environment variables for ODBC configuration
ENV ODBCINI /etc/odbc.ini
ENV ODBCSYSINI /etc

# Copy the configuration files to the container
#COPY config.ini .
#COPY odbcinst.ini /etc/
#COPY odbc.ini /etc/

# Copy the application code to the container
COPY chatbot.py .
COPY config.ini .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyodbc
RUN pip install configparser
#RUN pip install random
RUN pip install spotipy
RUN pip install python-telegram-bot==13.7
RUN pip install -r requirements.txt

# Start the application
CMD [ "python", "chatbot.py" ]

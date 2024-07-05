#!/bin/bash

# Define the path to the .env file
ENV_FILE=".env"

# Check the current state of USE_DATABASE
if grep -q "USE_DATABASE=True" "$ENV_FILE"; then
    # Switch to using JSON
    sed -i 's/USE_DATABASE=True/USE_DATABASE=False/' "$ENV_FILE"
    echo -e "Switched to using JSON for data persistence."
elif grep -q "USE_DATABASE=False" "$ENV_FILE"; then
    # Switch to using the database
    sed -i 's/USE_DATABASE=False/USE_DATABASE=True/' "$ENV_FILE"
    echo -e "Switched to using the database for data persistence."
else
    # Add the USE_DATABASE variable if it doesn't exist
    echo "USE_DATABASE=True" >> "$ENV_FILE"
    echo -e "Set USE_DATABASE to True."
fi

# Restart the Flask server
pkill -f "flask run"
flask run &

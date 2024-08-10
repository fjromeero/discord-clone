#!/bin/bash

# Check if the user provided a name
if [ -z "$1" ]; then
  echo "You must provide a name for the .env file."
  echo "Usage: $0 file_name"
  exit 1
fi

# Define variables
FILE_NAME="$1"
SOURCE_FILE=".env.example"
DEST_FILE="./$FILE_NAME"
SYMLINK_SOURCE="../$FILE_NAME"
SYMLINK_DEST="./frontend/$FILE_NAME"

# Copy the .env.example file with the provided name
if cp "$SOURCE_FILE" "$DEST_FILE"; then
  echo "File successfully copied: $DEST_FILE"
else
  echo "Error copying the file."
  exit 1
fi

# Create the symbolic link in the frontend directory
if ln -s "$SYMLINK_SOURCE" "$SYMLINK_DEST"; then
  echo "Symbolic link created at: $SYMLINK_DEST"
else
  echo "Error creating the symbolic link."
  exit 1
fi

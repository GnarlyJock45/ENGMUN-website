#!/bin/bash

# Install npm dependencies
npm install

# Build CSS for production
npm run build:prod

# Install Python dependencies
pip install -r requirements.txt
#!/bin/bash

echo "Setting up data directory..."
mkdir -p data/docs
mkdir -p data/json
echo "Downloading Gatsby PDF..."
curl "https://www.wsfcs.k12.nc.us/cms/lib/NC01001395/Centricity/Domain/7935/Gatsby_PDF_FullText.pdf" -s -o "data/docs/gatsby.pdf"
echo "Downloading airpot JSON data..."
curl "https://data.transportation.gov/api/views/kfcv-nyy3/rows.json?accessType=DOWNLOAD" -s -o "data/json/airports.json"
echo "All done!"

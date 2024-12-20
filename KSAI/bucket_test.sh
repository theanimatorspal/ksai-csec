#!/bin/bash

# Check if a bucket name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <bucket-name>"
    exit 1
fi

BUCKET_NAME=$1
echo "Testing public configurations of bucket: $BUCKET_NAME"

# 1. Test bucket for public listing
echo "Testing public object listing..."
LIST_RESULT=$(curl -s -I "https://$BUCKET_NAME.s3.amazonaws.com")
if echo "$LIST_RESULT" | grep -q "200 OK"; then
    echo "Bucket allows public listing!"
else
    echo "Bucket listing not accessible publicly."
fi

# 2. Attempt to access known files
echo "Testing for access to common files..."
COMMON_FILES=(
    ".aws-datasync-metadata"
    "index.html"
    "config.json"
    "backup.tar.gz"
)

for FILE in "${COMMON_FILES[@]}"; do
    URL="https://$BUCKET_NAME.s3.amazonaws.com/$FILE"
    echo "Testing URL: $URL"
    RESULT=$(curl -s -I "$URL")
    if echo "$RESULT" | grep -q "200 OK"; then
        echo "Accessible: $URL"
    else
        echo "Not accessible: $URL"
    fi
done

# 3. Bruteforce common object keys (dictionary-based)
echo "Bruteforcing object keys..."
DICTIONARY="keys.txt" # A file containing common object names
if [ ! -f "$DICTIONARY" ]; then
    echo "Dictionary file 'keys.txt' not found. Please create one with common keys."
    exit 1
fi

while IFS= read -r KEY; do
    URL="https://$BUCKET_NAME.s3.amazonaws.com/$KEY"
    echo "Testing URL: $URL"
    RESULT=$(curl -s -I "$URL")
    if echo "$RESULT" | grep -q "200 OK"; then
        echo "Accessible: $URL"
    fi
done < "$DICTIONARY"

# 4. Check for open permissions using S3 website endpoints
echo "Checking bucket permissions via website endpoint..."
WEBSITE_RESULT=$(curl -s -I "http://$BUCKET_NAME.s3-website.amazonaws.com")
if echo "$WEBSITE_RESULT" | grep -q "200 OK"; then
    echo "Bucket has an accessible website endpoint!"
else
    echo "Bucket website endpoint not accessible."
fi

echo "Finished testing bucket: $BUCKET_NAME"

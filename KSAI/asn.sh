#!/bin/bash

# Check if the correct number of arguments is passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_file> <output_file> <output_file2>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
OUTPUT_FILE2="$3"


# Verify the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' does not exist."
    exit 1
fi

# Empty the output file if it exists, or create it
> "$OUTPUT_FILE"

# Read each AS number from the input file and process it
while IFS= read -r ASN; do
    echo "Processing $ASN..."
    whois -h whois.radb.net -- "-i origin $ASN" \
        | grep -Eo "([0-9.]+){4}/[0-9]+" \
        | uniq \
        | tee "$OUTPUT_FILE2" \
        | mapcidr -silent \
        | dnsx -ptr -resp-only \
        >> "$OUTPUT_FILE"
done < "$INPUT_FILE"

echo "Processing complete. Output saved to '$OUTPUT_FILE'."

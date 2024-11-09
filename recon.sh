#!/bin/bash

domains=("example.com" "test.com" "example.org")
output_dir="./scan_results"

for domain in "${domains[@]}"
do
    mkdir -p "$output_dir/$domain"
    nmap -v -oN "$output_dir/$domain/open_ports.txt" "$domain"
    sublist3r -d "$domain" -o "$output_dir/$domain/subdomains.txt"
    gobuster dir -u "https://$domain" -w /usr/share/wordlists/dirb/common.txt -o "$output_dir/$domain/file_paths.txt" -k
done

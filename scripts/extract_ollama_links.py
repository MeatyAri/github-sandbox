#!/usr/bin/env python3
import sys
import re
import json

def extract_links(input_data):
    links = []
    for line in input_data.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('{'):
            try:
                data = json.loads(line)
                if 'url' in data:
                    links.append(data['url'])
                elif 'link' in data:
                    links.append(data['link'])
                elif 'download_url' in data:
                    links.append(data['download_url'])
            except json.JSONDecodeError:
                pass
        else:
            url_match = re.search(r'https://[^\s\'"]+', line)
            if url_match:
                links.append(url_match.group())
    return links

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            input_data = f.read()
    else:
        input_data = sys.stdin.read()
    
    links = extract_links(input_data)
    for link in links:
        print(link)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch generate Dropbox direct download links for all files in a folder.

Usage example:
    python generate_dropbox_links.py \
        -k YOUR_ACCESS_TOKEN \
        -f /CUTnTag/hs/ \
        -o hs_links.txt
"""

import dropbox
import argparse
import os

def list_files(dbx, folder):
    """Recursively list all files in the folder"""
    files = []
    try:
        res = dbx.files_list_folder(folder)
        files.extend(res.entries)
        while res.has_more:
            res = dbx.files_list_folder_continue(res.cursor)
            files.extend(res.entries)
    except Exception as e:
        print(f"Error listing folder '{folder}': {e}")
    # Only return FileMetadata entries
    return [f for f in files if isinstance(f, dropbox.files.FileMetadata)]

def create_shared_link(dbx, path):
    """Generate a direct download link for a file"""
    try:
        link = dbx.sharing_create_shared_link_with_settings(path)
        url = link.url.replace("?dl=0", "?dl=1")
        return url
    except dropbox.exceptions.ApiError:
        # If already shared, get existing link
        try:
            links = dbx.sharing_list_shared_links(path=path).links
            if links:
                return links[0].url.replace("?dl=0", "?dl=1")
        except Exception as e:
            print(f"Cannot create or retrieve link for {path}: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Batch generate Dropbox direct download links for all files in a folder."
    )
    parser.add_argument("-k", "--key", required=True, help="Dropbox API access token")
    parser.add_argument("-f", "--folder", required=True, help="Dropbox folder path (e.g. /Project/data)")
    parser.add_argument("-o", "--output", default="dropbox_links.txt", help="Output filename to save URLs")

    args = parser.parse_args()

    # Initialize Dropbox client
    dbx = dropbox.Dropbox(args.key)

    # List files
    files = list_files(dbx, args.folder)
    print(f"Found {len(files)} files in '{args.folder}'")

    records = []
    for f in files:
        url = create_shared_link(dbx, f.path_lower)
        if url:
            filename = os.path.basename(f.path_display)
            records.append((filename, url))

    # Save to output file (filename \t url)
    with open(args.output, "w") as out:
        for name, url in records:
            out.write(f"{name}\t{url}\n")

    print(f"? Saved {len(records)} links to '{args.output}'")

if __name__ == "__main__":
    main()

import os
import ndjson
import json
import requests
import re

ndjson_file = "source/prestatiedruk.ndjson"
output_folder = "profile_pictures/"
category = "prestatiedruk"
image_links = []

def extract_id_and_extension(url):
    pattern = r"/([^/]+)\.([a-zA-Z]+)(\?.*)?$"
    match = re.search(pattern, url)
    
    if match:
        image_id = match.group(1) 
        extension = match.group(2) 
        return image_id, extension
    else:
        return None, None

def download_image(img_url, save_dir, category):
    try:
        image_id, image_extension = extract_id_and_extension(img_url)
        response = requests.get(img_url)
        response.raise_for_status()
        
        filename = os.path.join(save_dir, f"{category}_{image_id}.{image_extension}")
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

with open(ndjson_file, 'r') as file:
    for item_index, item in enumerate(ndjson.reader(file)):
        data_item = item.get("data")
        if data_item is None:
            continue
        user_item = data_item.get("user")
        if user_item is None:
            continue
        profile_picture = user_item["profile_pic_url"]
        print(profile_picture)
        download_image(profile_picture, output_folder, category)
            
            
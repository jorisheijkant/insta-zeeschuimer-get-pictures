import os
import ndjson
import json
import requests
import re

ndjson_file = "source/posts.ndjson"
output_folder = "images/"
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

def download_image(img_url, save_dir):
    try:
        image_id, image_extension = extract_id_and_extension(img_url)
        response = requests.get(img_url)
        response.raise_for_status()
        
        filename = os.path.join(save_dir, f"{image_id}.{image_extension}")
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
        images_array = data_item.get("image_versions2")
        if images_array is None:
            continue
        image_candidates = images_array.get("candidates")
        if image_candidates is None:
            continue
        main_image = image_candidates[0]
        print(main_image)
        download_image(main_image["url"], output_folder)
            
            
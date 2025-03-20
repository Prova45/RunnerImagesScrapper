import re
import json
import requests

def download_readme():
    url = "https://raw.githubusercontent.com/actions/runner-images/main/README.md"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Impossibile scaricare il README.md")

def extract_json_url(badge_url):
    match = re.search(r"https://img\.shields\.io/endpoint\?url=(https%3A%2F%2Fgist\.githubusercontent\.com%2F[^\s]+)", badge_url)
    if match:
        return match.group(1).replace("%3A", ":").replace("%2F", "/").replace("%2C", ",").replace("%2B", "+")
    return None

def categorize_by_os(image_name):
    image_name = image_name.lower()
    if 'ubuntu' in image_name:
        return 'ubuntu'
    elif 'macos' in image_name:
        return 'macos'
    elif 'windows' in image_name:
        return 'windows'
    return None

def process_readme(content):
    pattern = r"\| (.*?) \| (.*?) \| \[(.*?)\] \| !\[.*?\]\((.*?)\) \|"
    matches = re.findall(pattern, content)

    data = {
        "ubuntu": [],
        "macos": [],
        "windows": []
    }

    for match in matches:
        image = match[0].strip()
        label = match[1].strip()
        included_software = match[2].strip()
        badge_url = match[3].strip()

        json_url = extract_json_url(badge_url)
        category = categorize_by_os(image)
        if category:
            data[category].append({
                "image": image,
                "label": label,
                "included_software": included_software,
                "json_url": json_url
            })
    
    with open("versions.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    try:
        readme_content = download_readme()
        process_readme(readme_content)
    except Exception as e:
        print(f"Errore durante l'elaborazione: {e}")

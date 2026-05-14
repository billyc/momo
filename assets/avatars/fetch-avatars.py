import sys,json
import yaml
import urllib.request

avatars = {
    "avatars": {}
}

with open("speakers.yaml", "r") as file:
    speakers = yaml.safe_load(file)
    for s in speakers:
        print(s["name"],s["image"])
        ext = s["image"].split(".")[-1]
        filename = f"{s['name']}.{ext}"
        print(filename)

        #urllib.request.urlretrieve(s["image"], filename)
        s["avatar"] = filename

        avatars["avatars"][s["name"]] = filename

# Write the list of dictionaries to a YAML file
with open(f"_speakers.yaml", "w") as f:
    yaml.dump(speakers, f, sort_keys=False)
with open(f"_avatars.yaml", "w") as f:
    yaml.dump(avatars, f, sort_keys=False)

import sys, json
import pandas as pd
import yaml

import re
import unicodedata

YEAR = "2025"


def make_filename_safe(name: str) -> str:
    # Normalize Unicode (e.g., é → e)
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")  # remove non-ASCII
    # Replace spaces and repeated hyphens
    name = re.sub(r"\s+", "-", name)
    # Remove anything that's not a-z, 0-9, underscore, or hyphen
    name = re.sub(r"[^a-zA-Z0-9_-]", "", name)
    # Collapse multiple hyphens and lowercase
    name = re.sub(r"-{2,}", "-", name).strip("-").lower()
    return name


# Load the Excel file and select the 'data' sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1h9T9-gtwsDiBqeEq0kxhfSD4gvLAU4tO"

gid = {"agenda": 12805781, "speakers": 1604031287}

for k, v in gid.items():
    csv_url = sheet_url + "/export?format=csv&gid=" + str(v)
    df = pd.read_csv(csv_url, keep_default_na=False, na_filter=False)
    print(df.head())

    if k == "speakers":
        # sort by last name
        df.sort_values(by="LastName", inplace=True)

        # attach headshot avatars
        with open("static/assets/avatars/_avatars.yaml", "r") as file:
            lookup = yaml.safe_load(file)
            df["avatar"] = df["Name"].map(lookup["avatars"])
            df["title"] = df["Name"]
            df["type"] = "speakers"
            df["layout"] = "speakers"

        # write individual speaker pages
        speakers = df.to_dict(orient="records")
        for i, speaker in enumerate(speakers):
            speaker["id"] = i
            yaml_string = yaml.dump(speaker, sort_keys=False)
            md = f"---\n{yaml_string}---\n"
            with open(f"./content/{YEAR}/speakers/{i}.md", "w") as f:
                f.write(md)

        # Write the list of dictionaries to a YAML file
        with open(f"./data/speakers.yaml", "w") as f:
            # sort_keys=False preserves column order
            yaml.dump(speakers, f, sort_keys=False)

        # Also create a lookup by speaker name
        speaker_lookup = {}
        for speaker in speakers:
            speaker_lookup[speaker["Name"]] = speaker
        with open(f"./data/speakerlookup.yaml", "w") as f:
            # sort_keys=False preserves column order
            yaml.dump(speaker_lookup, f, sort_keys=False)

    if k == "agenda":

        days = {
            "09/14/2025": [],
            "09/15/2025": [],
            "09/16/2025": [],
            "09/17/2025": [],
        }

        for date in days.keys():
            todays_sessions = []

            # get today's sessions
            today = df[df["Date"] == date].to_dict(orient="records")
            # attach subsessions to sessions
            current_session = None
            for event in today:
                if event["SessionOrSub"] == "Session":
                    if current_session != None:
                        todays_sessions.append(current_session)
                    current_session = event
                    current_session["subs"] = []
                else:
                    current_session["subs"].append(event)

                # split things up nicely
                speakers = []
                if len(event["Speakers"]) > 0:
                    speakers = [a.strip() for a in sorted(event["Speakers"].split(";"))]
                event["Speakers"] = speakers

                s = []
                if len(event["RoleModerator"]) > 0:
                    s = [a.strip() for a in sorted(event["RoleModerator"].split(";"))]
                event["RoleModerator"] = s

                s = []
                if len(event["RoleFacilitator"]) > 0:
                    s = [a.strip() for a in sorted(event["RoleFacilitator"].split(";"))]
                event["RoleFacilitator"] = s

                s = []
                if len(event["RoleDebater"]) > 0:
                    s = [a.strip() for a in sorted(event["RoleDebater"].split(";"))]
                event["RoleDebater"] = s

                tracks = []
                if len(event["Tracks"]) > 0:
                    tracks = [a.strip() for a in sorted(event["Tracks"].split(";"))]
                event["Tracks"] = tracks

            # all done with today's events
            todays_sessions.append(current_session)
            days[date] = todays_sessions
            print(date)
            print([session["SessionTitle"] for session in todays_sessions])

        # Write the list of dictionaries to a YAML file
        with open(f"./data/{k}.yaml", "w") as f:
            # sort_keys=False preserves column order
            # json.dump(records, f, sort_keys=False, indent=2)
            yaml.dump(days, f, sort_keys=False)

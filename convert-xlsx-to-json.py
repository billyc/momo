import sys,json
import pandas as pd
import yaml

# Load the Excel file and select the 'data' sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1h9T9-gtwsDiBqeEq0kxhfSD4gvLAU4tO"

gid = {
    "agenda": 12805781,
    "speakers": 1604031287
}

for k,v in gid.items():
    csv_url = sheet_url + "/export?format=csv&gid=" + str(v)
    df = pd.read_csv(csv_url, keep_default_na=False, na_filter=False)
    print(df.head())

    if k == "speakers":
        # sort by last name
        df.sort_values(by="LastName", inplace=True)

        # attach headshot avatars
        with open ("static/assets/avatars/_avatars.yaml", "r") as file:
            lookup = yaml.safe_load(file)
            df["avatar"] = df["Name"].map(lookup["avatars"])

    # Convert the DataFrame to a list of dictionaries (one dict per row)
    records = df.to_dict(orient="records")

    # Write the list of dictionaries to a YAML file
    with open(f"{k}.yaml", "w") as f:
        # sort_keys=False preserves column order
        #json.dump(records, f, sort_keys=False, indent=2)
        yaml.dump(records, f, sort_keys=False)

from pathlib import Path
import json

lc_names_id = "nr91028921"
lc_subjects_id = "sh85010201"

json_path = str(Path(__file__).parent / "response.json")
with open(json_path) as json_file:
    lc_subjects_response = json.load(json_file)

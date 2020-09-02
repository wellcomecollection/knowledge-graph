import json
from pathlib import Path

wikidata_id = "Q42"
lc_names_id = "nr91028921"
lc_subjects_id = "sh85010201"
mesh_id = "D019142"

data_dir = Path(__file__).parent / "data"

with open(str(data_dir / "loc_response.json")) as f:
    loc_response = json.load(f)

with open(str(data_dir / "mesh_response.json")) as f:
    mesh_response = json.load(f)

with open(str(data_dir / "wikidata_response.json")) as f:
    wikidata_response = json.load(f)

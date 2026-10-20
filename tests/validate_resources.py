"""Validate physics definitions and block tags without requiring Minecraft."""
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[1] / "src/main/resources/data"
count = 0
for path in root.rglob("*.json"):
    if "/physics_block_properties/" not in str(path) and "/tags/block/" not in str(path):
        continue
    # Minecraft accepts JSON comments; reject malformed structures and null entries.
    raw = re.sub(r"(?m)^\s*//.*$", "", path.read_text())
    data = json.loads(raw)
    assert isinstance(data, dict), path
    if "/physics_block_properties/" in str(path):
        assert isinstance(data.get("selector"), str), path
        assert isinstance(data.get("properties"), dict), path
    else:
        assert isinstance(data.get("values"), list), path
        for entry in data["values"]:
            assert isinstance(entry, str) or (
                isinstance(entry, dict) and isinstance(entry.get("id"), str)
            ), (path, entry)
    count += 1
print(f"Validated {count} physics definitions and block tags")

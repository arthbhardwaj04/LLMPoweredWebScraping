from typing import Dict, Any
import yaml

def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data = data or {}
    data.setdefault("global", {})
    data["global"].setdefault("user_agent", "Mozilla/5.0 (compatible; SimpleScraper/0.1)")
    data["global"].setdefault("timeout_sec", 15)
    data.setdefault("sites", [])
    return data

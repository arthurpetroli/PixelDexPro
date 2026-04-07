from typing import Optional, List, Dict, Any
import re
import pandas as pd
from io import StringIO
import httpx
from core.config import get_settings

settings = get_settings()


class CobblemonSheetIngestion:
    """Service for ingesting Cobblemon spawn data from Google Sheets."""

    # Column name mappings (sheet column -> our field name)
    COLUMN_MAPPING = {
        "no": "entry_number",
        "#": "entry_number",
        "pokemon": "pokemon_name",
        "entry": "entry_number",
        "bucket": "bucket",
        "weight": "weight",
        "min level": "min_level",
        "minlevel": "min_level",
        "max level": "max_level",
        "maxlevel": "max_level",
        "biomes": "biomes",
        "biome": "biomes",
        "excluded biomes": "excluded_biomes",
        "excludedbiomes": "excluded_biomes",
        "time": "time",
        "weather": "weather",
        "context": "context",
        "presets": "presets",
        "preset": "presets",
        "conditions": "conditions",
        "condition": "conditions",
        "anticonditions": "anticonditions",
        "anticondition": "anticonditions",
        "skylight min": "skylight_min",
        "skylightmin": "skylight_min",
        "skylight max": "skylight_max",
        "skylightmax": "skylight_max",
        "can see sky": "can_see_sky",
        "canseesky": "can_see_sky",
    }

    def __init__(self):
        self.sheet_url = settings.COBBLEMON_SHEET_URL
        self.sheet_id = settings.COBBLEMON_SHEET_ID

    def _normalize_column_name(self, col: str) -> str:
        """Normalize column name to our standard field name."""
        normalized = col.lower().strip()
        return self.COLUMN_MAPPING.get(normalized, normalized)

    def _parse_list_field(self, value: Any) -> List[str]:
        """Parse a field that may contain a comma-separated list."""
        if pd.isna(value) or value is None or value == "":
            return []

        if isinstance(value, list):
            return [str(v).strip() for v in value if v]

        value_str = str(value).strip()
        if not value_str:
            return []

        # Handle different separators
        if "," in value_str:
            return [v.strip() for v in value_str.split(",") if v.strip()]
        elif ";" in value_str:
            return [v.strip() for v in value_str.split(";") if v.strip()]
        else:
            return [value_str]

    def _parse_boolean(self, value: Any) -> Optional[bool]:
        """Parse a boolean field."""
        if pd.isna(value) or value is None or value == "":
            return None

        value_str = str(value).lower().strip()
        if value_str in ("true", "yes", "1", "y"):
            return True
        elif value_str in ("false", "no", "0", "n"):
            return False
        return None

    def _parse_int(self, value: Any) -> Optional[int]:
        """Parse an integer field."""
        if pd.isna(value) or value is None or value == "":
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def _parse_float(self, value: Any) -> Optional[float]:
        """Parse a float field."""
        if pd.isna(value) or value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _extract_pattern_key_values(self, row: Dict[str, Any]) -> Dict[str, str]:
        """Extract key=value pattern fields from row."""
        patterns = {}
        for key, value in row.items():
            if "=" in str(key) or (isinstance(value, str) and "=" in value):
                if "=" in str(key):
                    # Column name contains pattern
                    patterns[str(key)] = str(value) if not pd.isna(value) else ""
                elif isinstance(value, str) and "=" in value:
                    # Value contains pattern
                    for part in value.split(","):
                        if "=" in part:
                            k, v = part.split("=", 1)
                            patterns[k.strip()] = v.strip()
        return patterns

    def parse_row(
        self, row: Dict[str, Any], source_sheet: str, source_version: str
    ) -> Dict[str, Any]:
        """Parse a single row from the sheet into our spawn format."""
        # Normalize column names
        normalized_row = {}
        for col, value in row.items():
            normalized_col = self._normalize_column_name(col)
            normalized_row[normalized_col] = value

        return {
            "pokemon_name": str(normalized_row.get("pokemon_name", "")).strip().lower(),
            "entry_number": self._parse_int(normalized_row.get("entry_number")),
            "bucket": str(normalized_row.get("bucket", "")).strip() or None,
            "weight": self._parse_float(normalized_row.get("weight")),
            "min_level": self._parse_int(normalized_row.get("min_level")),
            "max_level": self._parse_int(normalized_row.get("max_level")),
            "biomes": self._parse_list_field(normalized_row.get("biomes")),
            "excluded_biomes": self._parse_list_field(
                normalized_row.get("excluded_biomes")
            ),
            "time": str(normalized_row.get("time", "")).strip().lower() or None,
            "weather": self._parse_list_field(normalized_row.get("weather")),
            "context": str(normalized_row.get("context", "")).strip().lower() or None,
            "presets": self._parse_list_field(normalized_row.get("presets")),
            "conditions": self._parse_list_field(normalized_row.get("conditions")),
            "anticonditions": self._parse_list_field(
                normalized_row.get("anticonditions")
            ),
            "skylight_min": self._parse_int(normalized_row.get("skylight_min")),
            "skylight_max": self._parse_int(normalized_row.get("skylight_max")),
            "can_see_sky": self._parse_boolean(normalized_row.get("can_see_sky")),
            "pattern_key_value": self._extract_pattern_key_values(row),
            "source_sheet": source_sheet,
            "source_version": source_version,
        }

    async def fetch_sheet_as_csv(self, sheet_url: str) -> str:
        """Fetch a Google Sheet as CSV using the export URL."""
        # Convert Google Sheet URL to CSV export URL
        if "docs.google.com/spreadsheets" in sheet_url:
            # Extract sheet ID
            match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url)
            if match:
                sheet_id = match.group(1)
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            else:
                csv_url = sheet_url
        else:
            csv_url = sheet_url

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(csv_url, follow_redirects=True)
            response.raise_for_status()
            return response.text

    async def ingest_from_url(
        self, sheet_url: str, source_version: str = "1.0"
    ) -> List[Dict[str, Any]]:
        """Ingest spawn data from a Google Sheet URL."""
        csv_content = await self.fetch_sheet_as_csv(sheet_url)
        return self.ingest_from_csv(csv_content, sheet_url, source_version)

    def ingest_from_csv(
        self, csv_content: str, source_sheet: str, source_version: str
    ) -> List[Dict[str, Any]]:
        """Parse CSV content into spawn records."""
        df = pd.read_csv(StringIO(csv_content))

        spawns = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            spawn_data = self.parse_row(row_dict, source_sheet, source_version)

            # Skip rows without a Pokémon name
            if spawn_data["pokemon_name"]:
                spawns.append(spawn_data)

        return spawns

    def ingest_from_dataframe(
        self, df: pd.DataFrame, source_sheet: str, source_version: str
    ) -> List[Dict[str, Any]]:
        """Parse a pandas DataFrame into spawn records."""
        spawns = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            spawn_data = self.parse_row(row_dict, source_sheet, source_version)

            if spawn_data["pokemon_name"]:
                spawns.append(spawn_data)

        return spawns


cobblemon_ingestion = CobblemonSheetIngestion()

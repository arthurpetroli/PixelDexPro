"""
Service for fetching and processing Cobblemon spawn data from Google Sheets.
"""

import logging
from typing import List, Dict, Any, Optional
import httpx
import csv
from io import StringIO

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Service for fetching Cobblemon spawn data from Google Sheets."""

    SHEET_ID = "1DJT7Hd0ldgVUjJbN0kYQFAyNBP6JGG_Clkipax98x-g"
    GID = "0"

    def __init__(self):
        self.csv_url = f"https://docs.google.com/spreadsheets/d/{self.SHEET_ID}/export?format=csv&gid={self.GID}"

    async def fetch_spawn_data(self) -> List[Dict[str, Any]]:
        """
        Fetch spawn data from Google Sheets as CSV and parse it.

        Returns:
            List of spawn entries with parsed data
        """
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(self.csv_url)
                response.raise_for_status()

                # Parse CSV
                csv_content = StringIO(response.text)
                reader = csv.DictReader(csv_content)

                spawn_data = []
                for row in reader:
                    # Skip empty rows
                    if not row.get("Pokémon") or not row.get("Pokémon").strip():
                        continue

                    # Parse biomes (comma-separated)
                    biomes_str = row.get("Biomes", "").strip()
                    biomes = (
                        [b.strip() for b in biomes_str.split(",") if b.strip()]
                        if biomes_str
                        else []
                    )

                    # Parse excluded biomes
                    excluded_biomes_str = row.get("Excluded Biomes", "").strip()
                    excluded_biomes = (
                        [b.strip() for b in excluded_biomes_str.split(",") if b.strip()]
                        if excluded_biomes_str
                        else []
                    )

                    # Parse numeric fields
                    try:
                        pokedex_number = (
                            int(row.get("No.", "0")) if row.get("No.") else None
                        )
                    except (ValueError, TypeError):
                        pokedex_number = None

                    try:
                        weight = (
                            float(row.get("Weight", "0")) if row.get("Weight") else None
                        )
                    except (ValueError, TypeError):
                        weight = None

                    try:
                        level_min = (
                            int(row.get("Lv. Min", "0")) if row.get("Lv. Min") else None
                        )
                    except (ValueError, TypeError):
                        level_min = None

                    try:
                        level_max = (
                            int(row.get("Lv. Max", "0")) if row.get("Lv. Max") else None
                        )
                    except (ValueError, TypeError):
                        level_max = None

                    spawn_entry = {
                        "pokedex_number": pokedex_number,
                        "pokemon_name": row.get("Pokémon", "").strip(),
                        "entry": row.get("Entry", "").strip(),
                        "bucket": row.get("Bucket", "").strip(),
                        "weight": weight,
                        "level_min": level_min,
                        "level_max": level_max,
                        "biomes": biomes,
                        "excluded_biomes": excluded_biomes,
                        "time": row.get("Time", "").strip(),
                        "weather": row.get("Weather", "").strip(),
                        "context": row.get("Context", "").strip(),
                        "can_see_sky": row.get("Can See Sky", "").strip(),
                        "min_light_level": row.get("Min Light Level", "").strip(),
                        "max_light_level": row.get("Max Light Level", "").strip(),
                        "min_y": row.get("Min Y", "").strip(),
                        "max_y": row.get("Max Y", "").strip(),
                        "needed_nearby_blocks": row.get(
                            "Needed Nearby Blocks", ""
                        ).strip(),
                        "needed_base_blocks": row.get("Needed Base Blocks", "").strip(),
                        "anti_condition": row.get("Anti Condition", "").strip(),
                    }

                    spawn_data.append(spawn_entry)

                logger.info(
                    f"Fetched {len(spawn_data)} spawn entries from Google Sheets"
                )
                return spawn_data

        except Exception as e:
            logger.error(f"Error fetching spawn data from Google Sheets: {e}")
            raise

    async def get_unique_biomes(self) -> List[str]:
        """
        Get a list of all unique biomes from the spawn data.

        Returns:
            Sorted list of unique biome names
        """
        spawn_data = await self.fetch_spawn_data()

        biomes_set = set()
        for entry in spawn_data:
            biomes_set.update(entry["biomes"])

        # Remove empty strings and sort
        biomes = sorted([b for b in biomes_set if b])

        logger.info(f"Found {len(biomes)} unique biomes")
        return biomes

    async def get_spawns_by_biome(self, biome: str) -> List[Dict[str, Any]]:
        """
        Get all spawn entries for a specific biome.

        Args:
            biome: The biome name to filter by

        Returns:
            List of spawn entries for the biome
        """
        spawn_data = await self.fetch_spawn_data()

        # Filter entries that include this biome
        filtered = [entry for entry in spawn_data if biome in entry["biomes"]]

        logger.info(f"Found {len(filtered)} spawn entries for biome '{biome}'")
        return filtered

    async def get_spawns_by_pokemon(self, pokemon_name: str) -> List[Dict[str, Any]]:
        """
        Get all spawn entries for a specific Pokémon.

        Args:
            pokemon_name: The Pokémon name to filter by

        Returns:
            List of spawn entries for the Pokémon
        """
        spawn_data = await self.fetch_spawn_data()

        # Case-insensitive search
        pokemon_name_lower = pokemon_name.lower()
        filtered = [
            entry
            for entry in spawn_data
            if entry["pokemon_name"].lower() == pokemon_name_lower
        ]

        logger.info(f"Found {len(filtered)} spawn entries for Pokémon '{pokemon_name}'")
        return filtered

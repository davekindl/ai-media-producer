"""
Visual Constitution Builder — World-Build from lyrics + genre.

Analyzes lyrics content and style to define:
  - Character Anchor (verbatim across all prompts)
  - Setting Anchor (verbatim across all prompts)
  - Art Direction Anchor (palette, camera, rendering)

Then generates 5 keyframe prompts (A-E) at different energy tiers.
"""

import json
from pathlib import Path


# Tier definitions: what changes per energy level
TIERS = {
    "A": {
        "name": "Stillness",
        "energy": 1,
        "pose": "Eyes closed, head down, motionless",
        "lighting": "single dim light source, cold blue undertones",
        "atmosphere": "heavy fog, near-darkness, oppressive silence",
        "fire": "a single dying ember",
        "camera": "wide shot, low angle, still",
    },
    "B": {
        "name": "Awakening",
        "energy": 2,
        "pose": "Eyes opening, chin lifting slowly, first sign of life",
        "lighting": "warm amber light entering from one side, rim light on shoulders",
        "atmosphere": "fog thinning, embers glowing brighter, first heat shimmer",
        "fire": "scattered embers on the ground beginning to glow",
        "camera": "medium-wide shot, slight low angle",
    },
    "C": {
        "name": "Building",
        "energy": 3,
        "pose": "Active stance, fists clenching, muscles tensing, leaning forward",
        "lighting": "multiple fire sources, strong rim lighting, dramatic shadows",
        "atmosphere": "sparks rising, dust particles catching light, tension building",
        "fire": "flames licking up from below, multiple fire sources",
        "camera": "medium shot, slight upward angle, subtle push in",
    },
    "D": {
        "name": "Eruption",
        "energy": 4,
        "pose": "Full exertion, mouth open in a roar, veins visible, explosive power",
        "lighting": "blinding backlight, harsh contrast, fire reflecting off skin",
        "atmosphere": "chaos, sparks flying everywhere, smoke billowing, debris",
        "fire": "raging inferno behind, flames engulfing the scene",
        "camera": "close-up, low angle looking up, dynamic",
    },
    "E": {
        "name": "Transcendence",
        "energy": 5,
        "pose": "Arms spread wide, consumed by energy, near-abstract silhouette",
        "lighting": "pure white/gold backlighting, figure becoming silhouette",
        "atmosphere": "near-abstract, light consuming everything, borders dissolving",
        "fire": "figure and fire merging, everything burning white-gold",
        "camera": "extreme low angle, wide, epic scale",
    },
}


# Default image model: OpenAI GPT-Image-2 via kie.ai unified jobs API.
DEFAULT_IMAGE_MODEL = "gpt-image-2-text-to-image"


def select_model(genre: str, has_character: bool) -> str:
    """Select image generation model based on genre and content.

    Defaults to GPT-Image-2 (the current kie.ai default). Photorealistic
    portraits route to Flux, which tends to render faces more naturally.
    """
    photoreal_genres = [
        "pop", "clean", "bright", "acoustic", "folk", "indie",
        "r&b", "soul", "jazz",
    ]

    genre_lower = genre.lower() if genre else ""

    if has_character and any(g in genre_lower for g in photoreal_genres):
        return "flux"

    return DEFAULT_IMAGE_MODEL


def build_constitution(
    lyrics_text: str,
    genre: str = "",
    character_description: str = "",
    setting_description: str = "",
    art_style: str = "",
    color_palette: str = "",
) -> dict:
    """
    Build a Visual Constitution from lyrics context.

    If character/setting/art descriptions aren't provided, the caller
    (Claude) should derive them from lyrics analysis before calling this.

    Returns a constitution dict with anchors and keyframe prompts.
    """
    has_character = bool(character_description)
    model = select_model(genre, has_character)

    # Default art direction if not provided
    if not art_style:
        art_style = "cinematic digital painting, hyper-detailed, dramatic lighting"
    if not color_palette:
        color_palette = "deep black, molten orange, cold steel blue, ember gold"

    # Art direction anchor (appears in ALL prompts)
    art_anchor = (
        f"16:9 aspect ratio, {art_style}, "
        f"color palette: {color_palette}, "
        f"volumetric lighting, film grain, no text, no watermark, no UI elements"
    )

    # Negative prompt (applied to all)
    negative = (
        "text, watermark, logo, signature, UI, HUD, blurry, low quality, "
        "deformed, cartoon, anime, illustration, clipart, stock photo"
    )

    # Build 5 keyframe prompts
    keyframes = {}
    for tier_key, tier in TIERS.items():
        parts = []

        # Character anchor (verbatim)
        if character_description:
            parts.append(character_description)
            parts.append(f"{tier['pose']}")

        # Setting anchor (verbatim)
        if setting_description:
            parts.append(setting_description)

        # Tier-specific variations
        parts.append(f"{tier['lighting']}")
        parts.append(f"{tier['atmosphere']}")
        parts.append(f"{tier['fire']}")
        parts.append(f"Camera: {tier['camera']}")

        # Art direction anchor (verbatim)
        parts.append(art_anchor)

        keyframes[tier_key] = {
            "tier": tier_key,
            "name": tier["name"],
            "energy": tier["energy"],
            "prompt": ". ".join(parts),
            "negative": negative,
        }

    constitution = {
        "model": model,
        "character_anchor": character_description or None,
        "setting_anchor": setting_description or None,
        "art_direction_anchor": art_anchor,
        "negative_prompt": negative,
        "color_palette": color_palette,
        "genre": genre,
        "keyframes": keyframes,
    }

    return constitution


def reduce_keyframes(constitution: dict, structure_map: list[dict]) -> dict:
    """
    If the song doesn't use all 5 energy tiers, reduce keyframes.

    Maps structure_map energy levels to the minimum set of keyframes needed.
    """
    # Find unique energy levels used in the song
    energies_used = set()
    for section in structure_map:
        energies_used.add(section["energy"])

    # Map energies to keyframe tiers
    energy_to_tier = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}
    tiers_needed = set()
    for e in energies_used:
        tiers_needed.add(energy_to_tier.get(e, "C"))

    # Always include at least A and E for contrast
    if len(tiers_needed) >= 2:
        tiers_needed.add("A")
        tiers_needed.add("E")

    # Filter keyframes
    reduced = {k: v for k, v in constitution["keyframes"].items() if k in tiers_needed}
    constitution["keyframes"] = reduced
    constitution["tiers_used"] = sorted(tiers_needed)

    return constitution


def save_constitution(constitution: dict, output_path: str):
    """Save constitution to JSON."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(
        json.dumps(constitution, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"  Visual constitution: {output_path}")
    print(f"  Model: {constitution['model']}")
    print(f"  Keyframes: {list(constitution['keyframes'].keys())}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build visual constitution from lyrics context")
    parser.add_argument("--genre", default="", help="Song genre/style")
    parser.add_argument("--character", default="", help="Character anchor description")
    parser.add_argument("--setting", default="", help="Setting anchor description")
    parser.add_argument("--art-style", default="", help="Art style description")
    parser.add_argument("--colors", default="", help="Color palette")
    parser.add_argument("--structure-map", help="Path to structure_map.json (for tier reduction)")
    parser.add_argument("--output", default="./output/constitution.json")
    args = parser.parse_args()

    constitution = build_constitution(
        lyrics_text="",
        genre=args.genre,
        character_description=args.character,
        setting_description=args.setting,
        art_style=args.art_style,
        color_palette=args.colors,
    )

    if args.structure_map:
        sm = json.loads(Path(args.structure_map).read_text())
        constitution = reduce_keyframes(constitution, sm)

    save_constitution(constitution, args.output)

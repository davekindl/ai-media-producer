"""
Video Loop Planner — Maps structure_map sections to keyframe transitions
and generates kie.ai video prompts for each transition.

Takes:
  - structure_map.json (sections with energy levels)
  - constitution.json (keyframes A-E with prompts)
  - aligned_lyrics.json (section timing)

Produces:
  - loop_plan.json (clip sequence with video model + motion prompts)
"""

import json
import math
from pathlib import Path


# Energy level → keyframe tier mapping
ENERGY_TO_TIER = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}

# Video model selection per transition type
VIDEO_MODELS = {
    "same": "kling_3.0",        # Same-frame loops (subtle motion)
    "adjacent": "veo_3_fast",   # Smooth energy shifts
    "skip": "sora_2_pro_hd",    # Dramatic jumps
    "reverse": "veo_3_fast",    # Energy drops (gradual)
    "reverse_sudden": "sora_2_pro_hd",  # Sudden drops
}

# Default clip duration for video generation
DEFAULT_CLIP_DURATION = 5  # seconds


def classify_transition(start_tier: str, end_tier: str) -> str:
    """Classify the transition type between two keyframe tiers."""
    tier_order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
    start_idx = tier_order[start_tier]
    end_idx = tier_order[end_tier]

    diff = end_idx - start_idx

    if diff == 0:
        return "same"
    elif diff == 1:
        return "adjacent"
    elif diff > 1:
        return "skip"
    elif diff == -1:
        return "reverse"
    else:  # diff < -1
        return "reverse_sudden"


def select_transition_effect(transition_type: str, start_tier: str, end_tier: str) -> str:
    """Select the FFmpeg transition effect for this clip boundary."""
    if transition_type == "same":
        return "hard_cut"
    elif transition_type in ("adjacent", "reverse"):
        return "crossfade_500ms"
    elif transition_type == "skip":
        # E→A or similar dramatic drops get flash
        if start_tier in ("D", "E") and end_tier in ("A", "B"):
            return "flash_to_black_200ms"
        return "crossfade_500ms"
    elif transition_type == "reverse_sudden":
        return "flash_to_black_200ms"
    return "crossfade_500ms"


def build_motion_prompt(
    constitution: dict,
    start_tier: str,
    end_tier: str,
    section_name: str,
) -> str:
    """
    Build a motion prompt for video generation.

    Uses character/setting anchors from constitution + tier-specific motion.
    """
    from world_build import TIERS

    parts = []

    # Character anchor with motion
    if constitution.get("character_anchor"):
        parts.append(constitution["character_anchor"])

    # Setting anchor
    if constitution.get("setting_anchor"):
        parts.append(constitution["setting_anchor"])

    # Transition-specific motion
    if start_tier == end_tier:
        tier = TIERS[start_tier]
        parts.append(f"Subtle breathing motion, {tier['atmosphere']}")
        parts.append(f"{tier['lighting']}")
        parts.append("minimal camera movement, 5 seconds")
    else:
        start = TIERS[start_tier]
        end = TIERS[end_tier]
        parts.append(f"Transitioning from {start['name'].lower()} to {end['name'].lower()}")
        parts.append(f"Lighting shifts from {start['lighting']} to {end['lighting']}")
        parts.append(f"Atmosphere: {end['atmosphere']}")
        parts.append("smooth transition, 5 seconds")

    return ". ".join(parts)


def plan_loops(
    structure_map: list[dict],
    aligned_lyrics: dict,
    constitution: dict,
) -> dict:
    """
    Generate the complete loop plan from structure, timing, and constitution.

    Returns loop_plan dict with clips, models, prompts, and assembly notes.
    """
    available_tiers = list(constitution.get("keyframes", {}).keys())
    if not available_tiers:
        available_tiers = ["A", "B", "C", "D", "E"]

    # Build section timing from aligned_lyrics
    section_timings = {}
    for section in aligned_lyrics.get("sections", []):
        tag = section["tag"]
        section_timings[tag] = {
            "start": section.get("start", 0),
            "end": section.get("end", 0),
        }

    clips = []
    clip_id = 1
    prev_tier = None

    for i, section in enumerate(structure_map):
        section_name = section["section"]
        energy = section["energy"]

        # Map energy to tier, snap to available tiers
        ideal_tier = ENERGY_TO_TIER.get(energy, "C")
        if ideal_tier not in available_tiers:
            # Find closest available tier
            tier_order = ["A", "B", "C", "D", "E"]
            ideal_idx = tier_order.index(ideal_tier)
            closest = min(available_tiers, key=lambda t: abs(tier_order.index(t) - ideal_idx))
            ideal_tier = closest

        # Determine start/end tiers for this section
        start_tier = prev_tier or ideal_tier
        end_tier = ideal_tier

        # Look ahead: if next section has very different energy, we might
        # transition within this section
        if i + 1 < len(structure_map):
            next_energy = structure_map[i + 1]["energy"]
            next_tier = ENERGY_TO_TIER.get(next_energy, "C")
            if next_tier in available_tiers:
                end_tier = ideal_tier  # Stay at current tier
            # But for the last beat of a building section, aim toward next
        else:
            end_tier = ideal_tier

        # Get timing
        timing = section_timings.get(section_name, {})
        time_start = timing.get("start", 0)
        time_end = timing.get("end", 0)

        # If no timing from alignment (instrumental sections), estimate
        if time_start == 0 and time_end == 0 and i > 0:
            prev_timing = section_timings.get(structure_map[i-1]["section"], {})
            time_start = prev_timing.get("end", 0)
            # Estimate duration based on position
            time_end = time_start + 15  # Default 15s for unmatched sections

        section_duration = max(time_end - time_start, 1)

        # Determine clip duration and loop count
        clip_duration = DEFAULT_CLIP_DURATION
        loop_count = max(1, math.ceil(section_duration / clip_duration))

        # Classify transition
        transition_type = classify_transition(start_tier, end_tier)
        video_model = VIDEO_MODELS.get(transition_type, "veo_3_fast")
        transition_effect = select_transition_effect(transition_type, start_tier, end_tier)

        # Build motion prompt
        motion_prompt = build_motion_prompt(
            constitution, start_tier, end_tier, section_name
        )

        clips.append({
            "clip_id": clip_id,
            "start_frame": start_tier,
            "end_frame": end_tier,
            "section": section_name,
            "energy": energy,
            "time_start": round(time_start, 2),
            "time_end": round(time_end, 2),
            "video_model": video_model,
            "motion_prompt": motion_prompt,
            "clip_duration_seconds": clip_duration,
            "loop_count": loop_count,
            "transition_type": transition_effect,
        })

        clip_id += 1
        prev_tier = end_tier

    # Assembly notes
    assembly_notes = {
        "crossfade_between_different_pairs": "0.5s",
        "hard_cut_within_same_keyframe_loops": True,
        "flash_to_black_on_dramatic_drops": "E->A transitions, 0.2s white flash",
        "total_clips": len(clips),
        "unique_transitions": len(set(c["start_frame"] + c["end_frame"] for c in clips)),
    }

    return {
        "keyframes_used": sorted(available_tiers),
        "clips": clips,
        "assembly_notes": assembly_notes,
    }


def save_loop_plan(loop_plan: dict, output_path: str):
    """Save loop plan to JSON."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(
        json.dumps(loop_plan, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"  Loop plan: {output_path}")
    print(f"  Keyframes used: {loop_plan['keyframes_used']}")
    print(f"  Total clips: {len(loop_plan['clips'])}")

    # Summary
    for clip in loop_plan["clips"]:
        arrow = f"{clip['start_frame']}->{clip['end_frame']}"
        model = clip["video_model"]
        print(f"    Clip {clip['clip_id']}: [{clip['section']}] {arrow} ({model}) {clip['time_start']:.1f}s-{clip['time_end']:.1f}s")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate video loop plan")
    parser.add_argument("--structure-map", required=True, help="Path to structure_map.json")
    parser.add_argument("--aligned", required=True, help="Path to aligned_lyrics.json")
    parser.add_argument("--constitution", required=True, help="Path to constitution.json")
    parser.add_argument("--output", default="./output/loop_plan.json")
    args = parser.parse_args()

    sm = json.loads(Path(args.structure_map).read_text())
    aligned = json.loads(Path(args.aligned).read_text())
    const = json.loads(Path(args.constitution).read_text())

    plan = plan_loops(sm, aligned, const)
    save_loop_plan(plan, args.output)

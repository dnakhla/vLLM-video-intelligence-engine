#!/usr/bin/env python3
"""Add video durations to data.json from all_takes.json"""
import json
from pathlib import Path

def format_duration(seconds):
    """Format duration as MM:SS."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

def main():
    # Load data.json
    data_file = Path(__file__).parent / 'data.json'
    with open(data_file) as f:
        data = json.load(f)

    # Load all_takes.json which has the duration data
    all_takes_file = Path(__file__).parent.parent / 'results_100_shared' / 'all_takes.json'
    with open(all_takes_file) as f:
        all_takes = json.load(f)

    # Build a lookup map
    duration_map = {}
    for result in all_takes['results']:
        video_id = result['video_id']
        if 'metadata' in result and 'duration_seconds' in result['metadata']:
            duration_map[video_id] = result['metadata']['duration_seconds']

    print(f"Adding durations for {len(data['videos'])} videos...")

    # Add duration to each video
    for video in data['videos']:
        video_id = video['id']
        if video_id in duration_map:
            duration = duration_map[video_id]
            video['duration_seconds'] = duration
            video['duration_formatted'] = format_duration(duration)
            print(f"  ✓ {video_id}: {video['duration_formatted']}")
        else:
            print(f"  ✗ {video_id}: Duration not found")

    # Save updated data
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✅ Updated {data_file}")

if __name__ == "__main__":
    main()

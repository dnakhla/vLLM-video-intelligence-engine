#!/usr/bin/env python3
"""Analyze data to find real insights about topic agreement patterns."""
import json

with open('data.json') as f:
    data = json.load(f)

# Analyze topic agreement across models and videos
topic_stats = {}

for video in data['videos']:
    # Get tags that all 4 models agree on (intersection)
    all_models = ['GPT+Whisper', 'Gemma+Whisper', 'GPT Vision', 'GPT Transcript']

    # Get tags from each model
    model_tags = {}
    for model in all_models:
        if model in video['models'] and 'tags' in video['models'][model]:
            model_tags[model] = set(video['models'][model]['tags'])

    # Skip if any model is missing
    if len(model_tags) != 4:
        continue

    # Find intersection of tags (topics all models agree on)
    agreed_tags = set.intersection(*model_tags.values())

    # For each agreed tag, check host agreement across models
    for tag in agreed_tags:
        if tag not in topic_stats:
            topic_stats[tag] = {
                'total_videos': 0,
                'host_agrees_all_models': 0,
                'host_disagrees_all_models': 0,
                'host_mixed': 0
            }

        topic_stats[tag]['total_videos'] += 1

        # Check if host agrees/disagrees across all models
        host_responses = []
        for model in all_models:
            if 'host_agrees' in video['models'][model]:
                host_responses.append(video['models'][model]['host_agrees'])

        if len(host_responses) == 4:
            if all(host_responses):
                topic_stats[tag]['host_agrees_all_models'] += 1
            elif not any(host_responses):
                topic_stats[tag]['host_disagrees_all_models'] += 1
            else:
                topic_stats[tag]['host_mixed'] += 1

# Find topics with 100% agreement
print('Topics with 100% Host Agreement Across All Models:')
print('='*70)
perfect_agree = []
for tag, stats in topic_stats.items():
    if stats['total_videos'] >= 3:  # At least 3 videos
        agree_rate = (stats['host_agrees_all_models'] / stats['total_videos']) * 100
        if agree_rate == 100:
            perfect_agree.append((tag, stats))

perfect_agree.sort(key=lambda x: x[1]['total_videos'], reverse=True)
for tag, stats in perfect_agree:
    print(f'{tag}: {stats["total_videos"]} videos, 100% host agreement')

print('\nTopics with 100% Host Disagreement Across All Models:')
print('='*70)
perfect_disagree = []
for tag, stats in topic_stats.items():
    if stats['total_videos'] >= 3:
        disagree_rate = (stats['host_disagrees_all_models'] / stats['total_videos']) * 100
        if disagree_rate == 100:
            perfect_disagree.append((tag, stats))

perfect_disagree.sort(key=lambda x: x[1]['total_videos'], reverse=True)
for tag, stats in perfect_disagree:
    print(f'{tag}: {stats["total_videos"]} videos, 100% host disagreement')

print('\nMost Polarizing Topics (Mixed Host Response):')
print('='*70)
mixed = []
for tag, stats in topic_stats.items():
    if stats['total_videos'] >= 3:
        mixed_rate = (stats['host_mixed'] / stats['total_videos']) * 100
        if mixed_rate >= 50:
            mixed.append((tag, stats, mixed_rate))

mixed.sort(key=lambda x: x[2], reverse=True)
for tag, stats, rate in mixed[:10]:
    print(f'{tag}: {stats["total_videos"]} videos, {rate:.0f}% mixed responses')

# Additional insights
print('\n\nModel Agreement Statistics:')
print('='*70)
model_perfect_agreement = 0
for video in data['videos']:
    all_models = ['GPT+Whisper', 'Gemma+Whisper', 'GPT Vision', 'GPT Transcript']
    host_agrees = []
    for model in all_models:
        if model in video['models'] and 'host_agrees' in video['models'][model]:
            host_agrees.append(video['models'][model]['host_agrees'])

    if len(host_agrees) == 4 and (all(host_agrees) or not any(host_agrees)):
        model_perfect_agreement += 1

print(f'Videos where all 4 models perfectly agree on host response: {model_perfect_agreement}/{len(data["videos"])} ({model_perfect_agreement/len(data["videos"])*100:.1f}%)')

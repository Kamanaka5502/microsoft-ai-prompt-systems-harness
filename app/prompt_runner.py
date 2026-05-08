from __future__ import annotations

CONTENT_FORMATS = {
    'quest': 'Give the player a clear objective, motivation, and success condition.',
    'dialogue': 'Create a short exchange with voice, intent, and emotional clarity.',
    'character': 'Introduce a memorable character with role, tone, and player relevance.',
    'event': 'Announce a timed experience with stakes, reward, and urgency.',
    'tutorial': 'Teach one mechanic with clarity, sequence, and low friction.',
}


def generate_content_packet(format_name: str, topic: str, audience: str, tone: str) -> dict:
    if format_name not in CONTENT_FORMATS:
        format_name = 'quest'

    format_rule = CONTENT_FORMATS[format_name]
    content = (
        f'{topic} is presented as a {format_name} content packet for {audience}. '
        f'The tone is {tone}. {format_rule} The output should remain clear, engaging, '
        'and repeatable across related content variations while preserving structure, player value, '
        'and production-readiness.'
    )

    return {
        'format': format_name,
        'title': f'{topic.title()} — {format_name.title()} Packet',
        'audience': audience,
        'tone': tone,
        'content': content,
        'constraints_satisfied': [
            'format declared',
            'audience declared',
            'tone declared',
            'production structure preserved',
            'repeatable packet contract followed',
        ],
        'failure_risks': [
            'may require stronger franchise-specific voice',
        ],
        'revision_notes': [
            'increase game flavor if target IP voice is supplied',
        ],
    }

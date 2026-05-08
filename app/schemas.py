from __future__ import annotations

REQUIRED_FIELDS = {
    'format': str,
    'title': str,
    'audience': str,
    'tone': str,
    'content': str,
    'constraints_satisfied': list,
    'failure_risks': list,
    'revision_notes': list,
}

SUPPORTED_FORMATS = {'quest', 'dialogue', 'character', 'event', 'tutorial'}


def validate_content_packet(packet: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in packet:
            errors.append(f'missing:{field}')
        elif not isinstance(packet[field], expected_type):
            errors.append(f'type_error:{field}')

    if packet.get('format') not in SUPPORTED_FORMATS:
        errors.append('unsupported_format')

    content = packet.get('content')
    if isinstance(content, str) and len(content.strip()) < 80:
        errors.append('content_too_short')

    if packet.get('constraints_satisfied') == []:
        errors.append('no_constraints_satisfied')

    return len(errors) == 0, errors

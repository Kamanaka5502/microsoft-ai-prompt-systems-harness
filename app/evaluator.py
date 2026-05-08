from __future__ import annotations

from app.schemas import validate_content_packet


def evaluate_packet(packet: dict) -> dict:
    valid, errors = validate_content_packet(packet)

    content = packet.get('content', '')
    clarity = 1.0 if isinstance(content, str) and len(content) >= 120 else 0.55
    structure = 1.0 if valid else 0.25
    engagement = 0.85 if packet.get('tone') and packet.get('audience') else 0.4
    repeatability = 1.0 if len(packet.get('constraints_satisfied', [])) >= 4 else 0.45
    production_readiness = 0.9 if packet.get('revision_notes') else 0.65
    risk_penalty = min(len(packet.get('failure_risks', [])) * 0.06, 0.30)

    score = round(
        (0.25 * clarity)
        + (0.25 * structure)
        + (0.20 * engagement)
        + (0.20 * repeatability)
        + (0.10 * production_readiness)
        - risk_penalty,
        4,
    )

    if not valid:
        decision = 'REVISE'
    elif score >= 0.82:
        decision = 'ACCEPT'
    elif score >= 0.64:
        decision = 'REVISE'
    else:
        decision = 'REJECT'

    return {
        'valid': valid,
        'errors': errors,
        'quality_score': score,
        'decision': decision,
        'dimensions': {
            'clarity': clarity,
            'structure': structure,
            'engagement': engagement,
            'repeatability': repeatability,
            'production_readiness': production_readiness,
            'risk_penalty': risk_penalty,
        },
    }

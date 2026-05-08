from __future__ import annotations

from hashlib import sha256
import json

from app.prompt_runner import CONTENT_FORMATS, generate_content_packet
from app.evaluator import evaluate_packet
from app.failure_modes import detect_failure_modes, revision_path

CASES = [
    ('quest', 'daily reward loop', 'casual players', 'playful'),
    ('dialogue', 'new companion greeting', 'new players', 'warm'),
    ('character', 'puzzle mentor', 'returning players', 'curious'),
    ('event', 'weekend challenge', 'live-ops players', 'exciting'),
    ('tutorial', 'match-three power-up', 'first-time players', 'clear'),
]

FAILURE_PROBE = {
    'format': 'quest',
    'title': 'Broken Packet',
    'audience': 'casual players',
    'tone': 'playful',
    'content': 'Too short.',
    'constraints_satisfied': [],
    'failure_risks': ['missing structure', 'low clarity', 'not production ready'],
    'revision_notes': [],
}


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def build_proof_pack() -> dict:
    receipts = []

    for format_name, topic, audience, tone in CASES:
        packet = generate_content_packet(format_name, topic, audience, tone)
        evaluation = evaluate_packet(packet)
        failures = detect_failure_modes(packet, evaluation)
        repairs = revision_path(failures)

        receipt_material = {
            'packet': packet,
            'evaluation': evaluation,
            'failure_modes': failures,
            'revision_path': repairs,
        }
        receipts.append({
            'format': format_name,
            'topic': topic,
            'evaluation': evaluation,
            'failure_modes': failures,
            'revision_path_available': bool(repairs),
            'receipt_hash': sha256(canonical(receipt_material).encode()).hexdigest(),
        })

    probe_evaluation = evaluate_packet(FAILURE_PROBE)
    probe_failures = detect_failure_modes(FAILURE_PROBE, probe_evaluation)
    probe_repairs = revision_path(probe_failures)
    failure_probe = {
        'probe': 'intentionally_broken_packet',
        'evaluation': probe_evaluation,
        'failure_modes': probe_failures,
        'revision_path': probe_repairs,
        'probe_hash': sha256(canonical({
            'packet': FAILURE_PROBE,
            'evaluation': probe_evaluation,
            'failure_modes': probe_failures,
            'revision_path': probe_repairs,
        }).encode()).hexdigest(),
    }

    format_coverage = sorted({r['format'] for r in receipts})
    all_schema_valid = all(r['evaluation']['valid'] for r in receipts)
    quality_threshold_met = all(r['evaluation']['quality_score'] >= 0.64 for r in receipts)
    repeatability_threshold_met = all(
        r['evaluation']['dimensions']['repeatability'] >= 0.8 for r in receipts
    )
    revision_path_available = all(r['revision_path_available'] for r in receipts)
    production_ready_formats = [
        r['format'] for r in receipts if r['evaluation']['decision'] in {'ACCEPT', 'REVISE'}
    ]
    failure_modes_detected = bool(failure_probe['failure_modes'])
    failure_probe_repaired = bool(failure_probe['revision_path'])

    proof_material = {
        'law': 'generative.content.prompt.harness.v1',
        'case_count': len(receipts),
        'format_coverage': format_coverage,
        'all_schema_valid': all_schema_valid,
        'quality_threshold_met': quality_threshold_met,
        'repeatability_threshold_met': repeatability_threshold_met,
        'revision_path_available': revision_path_available,
        'production_ready_formats': production_ready_formats,
        'failure_probe_hash': failure_probe['probe_hash'],
        'failure_modes_detected': failure_modes_detected,
        'failure_probe_repaired': failure_probe_repaired,
        'receipt_hashes': [r['receipt_hash'] for r in receipts],
    }
    proof_hash = sha256(canonical(proof_material).encode()).hexdigest()

    proof_holds = all([
        all_schema_valid,
        quality_threshold_met,
        repeatability_threshold_met,
        revision_path_available,
        failure_modes_detected,
        failure_probe_repaired,
        set(format_coverage) == set(CONTENT_FORMATS),
    ])

    return {
        'status': 'GENERATIVE_CONTENT_PROMPT_HARNESS_HOLDS' if proof_holds else 'GENERATIVE_CONTENT_PROMPT_HARNESS_FAILS',
        'case_count': len(receipts),
        'format_coverage': format_coverage,
        'schema_valid': all_schema_valid,
        'quality_threshold_met': quality_threshold_met,
        'repeatability_threshold_met': repeatability_threshold_met,
        'failure_modes_detected': failure_modes_detected,
        'failure_probe_repaired': failure_probe_repaired,
        'revision_path_available': revision_path_available,
        'production_ready_formats': production_ready_formats,
        'proof_hash': proof_hash,
        'failure_probe': failure_probe,
        'receipts': receipts,
    }


def main() -> None:
    proof = build_proof_pack()
    print(canonical(proof))
    print(proof['status'])


if __name__ == '__main__':
    main()

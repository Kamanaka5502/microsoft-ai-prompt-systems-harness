from __future__ import annotations


def detect_failure_modes(packet: dict, evaluation: dict) -> list[str]:
    failures: list[str] = []

    if not evaluation['valid']:
        failures.extend(evaluation['errors'])

    dims = evaluation['dimensions']
    if dims['clarity'] < 0.8:
        failures.append('weak_clarity')
    if dims['engagement'] < 0.8:
        failures.append('weak_engagement_signal')
    if dims['repeatability'] < 0.8:
        failures.append('low_repeatability')
    if dims['production_readiness'] < 0.8:
        failures.append('not_production_ready')

    if len(packet.get('failure_risks', [])) > 2:
        failures.append('too_many_open_risks')

    return failures


def revision_path(failures: list[str]) -> list[str]:
    if not failures:
        return ['ready_for_use_or_format_expansion']

    repairs = []
    for failure in failures:
        repairs.append(f'repair:{failure}')
    return repairs

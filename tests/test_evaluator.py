from app.prompt_runner import generate_content_packet
from app.evaluator import evaluate_packet
from app.failure_modes import detect_failure_modes, revision_path


def test_evaluator_scores_structured_packet():
    packet = generate_content_packet('event', 'weekend challenge', 'live-ops players', 'exciting')
    result = evaluate_packet(packet)

    assert result['valid'] is True
    assert result['quality_score'] >= 0.64
    assert result['decision'] in {'ACCEPT', 'REVISE'}


def test_failure_modes_have_revision_paths():
    packet = generate_content_packet('quest', 'daily reward loop', 'casual players', 'playful')
    result = evaluate_packet(packet)
    failures = detect_failure_modes(packet, result)
    repairs = revision_path(failures)

    assert repairs

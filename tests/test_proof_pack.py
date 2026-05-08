from app.proof_pack import build_proof_pack


def test_proof_pack_holds():
    proof = build_proof_pack()

    assert proof['status'] == 'GENERATIVE_CONTENT_PROMPT_HARNESS_HOLDS'
    assert proof['case_count'] == 5
    assert proof['schema_valid'] is True
    assert proof['quality_threshold_met'] is True
    assert proof['repeatability_threshold_met'] is True
    assert proof['revision_path_available'] is True
    assert set(proof['format_coverage']) == {'quest', 'dialogue', 'character', 'event', 'tutorial'}
    assert len(proof['proof_hash']) == 64


def test_proof_pack_replays_deterministically():
    first = build_proof_pack()
    second = build_proof_pack()

    assert first['proof_hash'] == second['proof_hash']
    assert first['status'] == second['status']

from app.prompt_runner import CONTENT_FORMATS, generate_content_packet
from app.schemas import validate_content_packet


def test_all_supported_formats_generate_valid_packets():
    for format_name in CONTENT_FORMATS:
        packet = generate_content_packet(format_name, 'sample topic', 'casual players', 'playful')
        valid, errors = validate_content_packet(packet)
        assert valid is True
        assert errors == []

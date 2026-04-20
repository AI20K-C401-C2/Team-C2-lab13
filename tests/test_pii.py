from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_phone_vn() -> None:
    out = scrub_text("Gọi cho tôi số 0987654321 nhé")
    assert "0987654321" not in out
    assert "REDACTED_PHONE_VN" in out


def test_scrub_cccd() -> None:
    out = scrub_text("CCCD của tôi là 123456789012")
    assert "123456789012" not in out
    assert "REDACTED_CCCD" in out


def test_scrub_credit_card() -> None:
    out = scrub_text("Thẻ số 4111 1111 1111 1111 hết hạn")
    assert "4111 1111 1111 1111" not in out
    assert "REDACTED_CREDIT_CARD" in out


def test_scrub_passport() -> None:
    out = scrub_text("Hộ chiếu B12345678 còn hạn")
    assert "B12345678" not in out
    assert "REDACTED_PASSPORT" in out


def test_scrub_multiple_pii() -> None:
    out = scrub_text("Liên hệ user@example.com hoặc 0912345678")
    assert "user@example.com" not in out
    assert "0912345678" not in out
    assert "REDACTED_EMAIL" in out
    assert "REDACTED_PHONE_VN" in out

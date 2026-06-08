import pytest
from unittest.mock import AsyncMock, patch
from src.analyzer import LogAnalyzer

def test_process_line_detects_failure():
    analyzer = LogAnalyzer()
    log = "2026-06-08 12:00:00 [ERROR] 192.168.1.50 - Failed password for admin"
    assert analyzer.process_line(log) == "192.168.1.50"

@pytest.mark.asyncio
@patch("src.analyzer.send_alert", new_callable=AsyncMock)
async def test_alert_triggers_on_threshold(mock_send_alert):
    analyzer = LogAnalyzer()
    ip = "185.220.101.1"
    assert await analyzer.check_alerts(ip) is False
    assert await analyzer.check_alerts(ip) is False
    assert await analyzer.check_alerts(ip) is True
    mock_send_alert.assert_called_once()
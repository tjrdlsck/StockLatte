import sys

def test_python_version():
    """파이썬 버전이 3.8 이상인지 검증하는 테스트입니다."""
    assert sys.version_info >= (3, 8)

def test_imports():
    """필수 라이브러리들이 정상적으로 로드되는지 검증하는 테스트입니다."""
    try:
        import yfinance
        import pandas
        import numpy
        import requests
        import dotenv
        import pytest
    except ImportError as e:
        assert False, f"필수 패키지 임포트(import) 실패: {e}"

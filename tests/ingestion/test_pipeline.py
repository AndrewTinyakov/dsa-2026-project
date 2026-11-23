from datetime import date
from unittest.mock import Mock

import pytest
import requests

from food_inflation.ingestion import download_sources, fao, pipeline


def test_download_reuses_all_three_cached_files(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    names = ["fao_food_prices.csv", "turkish_food_cpi.csv", "usd_try_daily.csv"]
    for name in names:
        (raw_dir / name).write_text("existing snapshot\n")
    get = Mock(side_effect=AssertionError("Cached inputs should work offline"))
    monkeypatch.setattr(requests, "get", get)
    monkeypatch.delenv("EVDS_API_KEY", raising=False)

    download_sources(tmp_path)

    get.assert_not_called()
    assert all((raw_dir / name).read_text() == "existing snapshot\n" for name in names)


def test_download_only_replaces_missing_fao_snapshot(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    (raw_dir / "turkish_food_cpi.csv").touch()
    (raw_dir / "usd_try_daily.csv").touch()
    response = Mock()
    response.content = (
        b"Title\nUnits\nDate,Food Price Index,Meat,Dairy,Cereals,Oils,Sugar\n"
        b"2025-01,100,101,102,103,104,105\n"
    )
    get = Mock(return_value=response)
    monkeypatch.setattr(requests, "get", get)

    download_sources(tmp_path)

    get.assert_called_once_with(fao.FAO_URL, timeout=90)
    assert (raw_dir / "fao_food_prices.csv").read_text() == (
        "Date,Food Price Index,Meat,Dairy,Cereals,Oils,Sugar\n2025-01,100,101,102,103,104,105\n"
    )


def test_unexpected_fao_response_does_not_create_a_snapshot(tmp_path, monkeypatch):
    response = Mock()
    response.content = b"Title\nUnits\nDate,A,B,C,D,E,F\n2025-01,1,2,3,4,5,6\n"
    monkeypatch.setattr(requests, "get", Mock(return_value=response))

    with pytest.raises(ValueError, match="fao_food_prices.csv is missing source columns"):
        download_sources(tmp_path)

    assert list((tmp_path / "data" / "raw").iterdir()) == []


def test_missing_evds_file_uses_project_key_and_downloads_complete_months(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    (raw_dir / "fao_food_prices.csv").touch()
    (raw_dir / "turkish_food_cpi.csv").touch()
    (tmp_path / ".env").write_text("EVDS_API_KEY=test-key\n")
    monkeypatch.delenv("EVDS_API_KEY", raising=False)

    class FixedDate(date):
        @classmethod
        def today(cls):
            return cls(2006, 2, 12)

    monkeypatch.setattr(pipeline, "date", FixedDate)
    responses = []
    for year in (2005, 2006):
        response = Mock()
        response.content = f"Tarih,TP_DK_USD_A_YTL,UNIXTIME\n03-01-{year},1.35,0\n".encode()
        responses.append(response)
    get = Mock(side_effect=responses)
    monkeypatch.setattr(requests, "get", get)

    download_sources(tmp_path)

    assert [call.args[0].split("&endDate=")[1] for call in get.call_args_list] == [
        "31-12-2005&type=csv",
        "31-01-2006&type=csv",
    ]
    assert all(call.kwargs["headers"] == {"key": "test-key"} for call in get.call_args_list)
    assert (raw_dir / "usd_try_daily.csv").read_text() == (
        "Tarih,TP_DK_USD_A_YTL,UNIXTIME\n03-01-2005,1.35,0\n03-01-2006,1.35,0\n"
    )

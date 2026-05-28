"""Unit tests for the scoring service (§8, §15.1)."""

from __future__ import annotations

from datetime import date

from app.models.smartphone import Smartphone
from app.models.soc import SoC
from app.services import scoring


def _soc(**overrides: object) -> SoC:
    base = dict(
        slug="test-soc",
        name="Test SoC",
        manufacturer_id=1,
        release_date=date(2024, 1, 1),
        process_nm=3.0,
        gpu_name="Test GPU",
        geekbench_single=3000,
        geekbench_multi=9000,
        antutu_score=2_500_000,
    )
    base.update(overrides)
    return SoC(**base)


def _phone(**overrides: object) -> Smartphone:
    base = dict(
        slug="test-phone",
        name="Test Phone",
        brand_id=1,
        soc_id=1,
        release_date=date(2024, 1, 1),
        msrp_usd=999,
        ram_gb=12,
        battery_mah=5000,
        charging_wired_w=45,
        charging_wireless_w=15,
        weight_g=180.0,
        os="Android",
        display={"refresh_hz": 120, "brightness_nits": 2600, "ppi": 460},
        cameras=[
            {"type": "main", "mp": 50, "ois": True},
            {"type": "ultrawide", "mp": 12},
            {"type": "selfie", "mp": 12},
        ],
    )
    base.update(overrides)
    return Smartphone(**base)


def test_scores_are_within_0_100() -> None:
    scores = scoring.compute_scores(_phone(), _soc())
    for value in (
        scores.overall,
        scores.performance,
        scores.camera,
        scores.battery,
        scores.display,
        scores.value,
    ):
        assert value is not None
        assert 0.0 <= value <= 100.0


def test_algorithm_version_is_attached() -> None:
    scores = scoring.compute_scores(_phone(), _soc())
    assert scores.algorithm_version == scoring.ALGORITHM_VERSION


def test_missing_benchmarks_yield_null_performance_not_zero() -> None:
    scores = scoring.compute_scores(_phone(), _soc(geekbench_single=None, geekbench_multi=None))
    assert scores.performance is None  # §8.2: null, never 0


def test_missing_camera_yields_null() -> None:
    scores = scoring.compute_scores(_phone(cameras=[]), _soc())
    assert scores.camera is None


def test_value_requires_msrp() -> None:
    scores = scoring.compute_scores(_phone(msrp_usd=None), _soc())
    assert scores.value is None


def test_normalize_clamps_to_bounds() -> None:
    bounds = scoring.Bounds(0, 100)
    assert scoring._normalize(-50, bounds) == 0.0
    assert scoring._normalize(150, bounds) == 100.0
    assert scoring._normalize(50, bounds) == 50.0


def test_normalize_invert() -> None:
    bounds = scoring.Bounds(2.0, 7.0)
    # smaller process_nm should score higher when inverted
    high = scoring._normalize(2.0, bounds, invert=True)
    low = scoring._normalize(7.0, bounds, invert=True)
    assert high > low

from __future__ import annotations

import os

os.environ["ARROW_DEFAULT_MEMORY_POOL"] = "system"

import hashlib
import html
import json
import math
import traceback
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

import aegisultra_enginev2 as aegis


# ============================================================
# AEGIS ULTRA — STREAMLIT COMMAND CENTER
# ============================================================

APP_NAME = "AEGIS ULTRA"
APP_VERSION = "2.1.0"

ENGINE_NAME = getattr(
    aegis,
    "ENGINE_NAME",
    "AEGIS ULTRA ENGINE",
)

ENGINE_VERSION = getattr(
    aegis,
    "ENGINE_VERSION",
    "Unknown",
)


# ============================================================
# 1. Streamlit configuration
# ============================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. Styling
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --ultra-bg: #080a11;
        --ultra-surface: rgba(255, 255, 255, 0.045);
        --ultra-surface-strong: rgba(255, 255, 255, 0.065);
        --ultra-border: rgba(255, 255, 255, 0.09);
        --ultra-text: rgba(255, 255, 255, 0.94);
        --ultra-muted: rgba(255, 255, 255, 0.58);
        --ultra-blue: #7388ff;
        --ultra-purple: #ae72ff;
        --ultra-green: #32d9a1;
        --ultra-amber: #ffbd59;
        --ultra-red: #ff6577;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(81, 102, 255, 0.15),
                transparent 29%
            ),
            radial-gradient(
                circle at 90% 2%,
                rgba(172, 81, 255, 0.12),
                transparent 26%
            ),
            radial-gradient(
                circle at 65% 75%,
                rgba(0, 211, 164, 0.06),
                transparent 30%
            ),
            linear-gradient(
                180deg,
                #090b13 0%,
                #0d1019 48%,
                #080a11 100%
            );
    }

    .block-container {
        max-width: 1520px;
        padding-top: 1.25rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(16, 19, 31, 0.99),
                rgba(8, 10, 17, 0.99)
            );
        border-right: 1px solid var(--ultra-border);
    }

    .ultra-hero {
        padding: 2rem 2.15rem;
        margin-bottom: 1.25rem;
        border-radius: 24px;
        background:
            linear-gradient(
                120deg,
                rgba(76, 95, 255, 0.23),
                rgba(150, 68, 255, 0.16),
                rgba(0, 214, 170, 0.09)
            );
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow:
            0 18px 60px rgba(0, 0, 0, 0.36),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(18px);
    }

    .ultra-badge {
        display: inline-block;
        padding: 0.37rem 0.75rem;
        margin-bottom: 0.9rem;
        border-radius: 999px;
        color: #c6ffee;
        background: rgba(0, 214, 163, 0.12);
        border: 1px solid rgba(0, 214, 163, 0.27);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .ultra-title {
        margin: 0;
        color: white;
        font-size: 3rem;
        font-weight: 850;
        letter-spacing: -0.055em;
        line-height: 1.05;
    }

    .ultra-subtitle {
        max-width: 950px;
        margin-top: 0.72rem;
        margin-bottom: 0;
        color: rgba(255, 255, 255, 0.70);
        font-size: 1.02rem;
        line-height: 1.6;
    }

    .section-label {
        margin-top: 1.2rem;
        margin-bottom: 0.75rem;
        color: rgba(255, 255, 255, 0.50);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .info-panel {
        padding: 0.9rem 1.05rem;
        margin-bottom: 1rem;
        border-radius: 14px;
        color: rgba(255, 255, 255, 0.76);
        background: rgba(115, 136, 255, 0.08);
        border: 1px solid rgba(115, 136, 255, 0.20);
        line-height: 1.55;
    }

    .format-panel {
        padding: 0.85rem 1rem;
        margin-bottom: 0.8rem;
        border-radius: 14px;
        color: rgba(255, 255, 255, 0.69);
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.075);
        font-size: 0.88rem;
        line-height: 1.55;
    }

    .summary-card {
        min-height: 126px;
        padding: 1.05rem 1.15rem;
        border-radius: 17px;
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.085);
        box-shadow: 0 10px 32px rgba(0, 0, 0, 0.20);
    }

    .summary-label {
        color: rgba(255, 255, 255, 0.50);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .summary-value {
        margin-top: 0.42rem;
        color: white;
        font-size: 1.55rem;
        font-weight: 850;
        letter-spacing: -0.035em;
    }

    .summary-note {
        margin-top: 0.35rem;
        color: rgba(255, 255, 255, 0.48);
        font-size: 0.8rem;
        line-height: 1.35;
    }

    .status-pass {
        color: var(--ultra-green);
    }

    .status-caution {
        color: var(--ultra-amber);
    }

    .status-fail {
        color: var(--ultra-red);
    }

    .recommendation-card {
        padding: 1.25rem 1.35rem;
        margin-bottom: 0.9rem;
        border-radius: 18px;
        background:
            linear-gradient(
                120deg,
                rgba(0, 214, 163, 0.10),
                rgba(255, 255, 255, 0.035)
            );
        border: 1px solid rgba(0, 214, 163, 0.22);
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.23);
    }

    .recommendation-rank {
        color: #7fffd3;
        font-size: 0.77rem;
        font-weight: 850;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .recommendation-name {
        margin-top: 0.32rem;
        color: white;
        font-size: 1.35rem;
        font-weight: 850;
        letter-spacing: -0.025em;
    }

    .recommendation-stats {
        margin-top: 0.55rem;
        color: rgba(255, 255, 255, 0.66);
        font-size: 0.91rem;
        line-height: 1.6;
    }

    .price-good {
        display: inline-block;
        margin-top: 0.65rem;
        padding: 0.3rem 0.65rem;
        border-radius: 999px;
        color: #bffff0;
        background: rgba(0, 214, 163, 0.11);
        border: 1px solid rgba(0, 214, 163, 0.22);
        font-size: 0.76rem;
        font-weight: 800;
    }

    .price-warning {
        display: inline-block;
        margin-top: 0.65rem;
        padding: 0.3rem 0.65rem;
        border-radius: 999px;
        color: #ffe3a8;
        background: rgba(255, 189, 89, 0.10);
        border: 1px solid rgba(255, 189, 89, 0.22);
        font-size: 0.76rem;
        font-weight: 800;
    }

    .score-card {
        text-align: center;
        min-height: 145px;
        padding: 1.35rem 0.85rem;
        border-radius: 19px;
        background:
            linear-gradient(
                145deg,
                rgba(130, 91, 255, 0.16),
                rgba(255, 255, 255, 0.035)
            );
        border: 1px solid rgba(151, 120, 255, 0.22);
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.23);
    }

    .score-value {
        color: white;
        font-size: 2.1rem;
        font-weight: 850;
        letter-spacing: -0.04em;
    }

    .score-probability {
        margin-top: 0.35rem;
        color: #d7ceff;
        font-size: 0.92rem;
        font-weight: 750;
    }

    [data-testid="stMetric"] {
        padding: 0.95rem 1rem;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.042);
        border: 1px solid rgba(255, 255, 255, 0.075);
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.16);
    }

    [data-testid="stMetricValue"] {
        font-weight: 820;
        letter-spacing: -0.03em;
    }

    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div,
    [data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.043);
        border-color: rgba(255, 255, 255, 0.10);
    }

    textarea {
        font-family:
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            monospace !important;
        font-size: 0.88rem !important;
        line-height: 1.5 !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        min-height: 3rem;
        border-radius: 13px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        font-weight: 760;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        padding: 0.34rem;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.035);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding-left: 1rem;
        padding-right: 1rem;
        font-weight: 720;
    }

    [data-testid="stDataFrame"] {
        overflow: hidden;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.075);
    }

    div[data-testid="stExpander"] {
        border-radius: 15px;
        border-color: rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.018);
    }

    hr {
        border-color: rgba(255, 255, 255, 0.075);
    }

    @media (max-width: 700px) {
        .ultra-title {
            font-size: 2.15rem;
        }

        .ultra-hero {
            padding: 1.4rem 1.3rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. Generic helpers
# ============================================================

def tokenize(value: Any) -> List[str]:
    return (
        str(value)
        .replace(",", " ")
        .replace("\t", " ")
        .split()
    )


def is_skip_token(value: Any) -> bool:
    return str(value).strip().lower() in {
        "",
        "-",
        "x",
        "na",
        "n/a",
        "none",
        "null",
    }


def optional_text(value: Any) -> str:
    return str(value or "").strip()


def validate_float(
    value: Any,
    label: str,
) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"{label} 必須是有效數值。"
        )

    if not math.isfinite(result):
        raise ValueError(
            f"{label} 不可為 NaN 或無限大。"
        )

    return result


def validate_odds(
    value: Any,
    label: str,
) -> float:
    result = validate_float(
        value,
        label,
    )

    if result <= 1.0:
        raise ValueError(
            f"{label} 必須大於 1.00。"
        )

    return result


def validate_quarter_line(
    value: Any,
    label: str,
) -> float:
    result = validate_float(
        value,
        label,
    )

    if not math.isclose(
        result * 4.0,
        round(result * 4.0),
        abs_tol=1e-8,
    ):
        raise ValueError(
            f"{label} 必須以 0.25 為單位。"
        )

    return result


def validate_integer_line(
    value: Any,
    label: str,
) -> float:
    result = validate_float(
        value,
        label,
    )

    if not math.isclose(
        result,
        round(result),
        abs_tol=1e-8,
    ):
        raise ValueError(
            f"{label} 必須是整數讓球。"
        )

    return result


def safe_float(
    value: Any,
) -> Optional[float]:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None

    if not math.isfinite(result):
        return None

    return result


def format_probability(
    value: Any,
    digits: int = 1,
) -> str:
    number = safe_float(value)

    if number is None:
        return "—"

    return f"{number * 100:.{digits}f}%"


def format_odds(
    value: Any,
    digits: int = 3,
) -> str:
    number = safe_float(value)

    if number is None:
        return "—"

    return f"{number:.{digits}f}"


def format_ev(
    value: Any,
    digits: int = 2,
) -> str:
    number = safe_float(value)

    if number is None:
        return "—"

    return f"{number * 100:+.{digits}f}%"


def probability_value(
    record: Dict[str, Any],
    metric: str,
    statistic: str = "minimum",
) -> Any:
    return (
        record
        .get("probability", {})
        .get(metric, {})
        .get(statistic)
    )


def summary_value(
    record: Dict[str, Any],
    field: str,
    statistic: str = "minimum",
) -> Any:
    return (
        record
        .get(field, {})
        .get(statistic)
    )


def html_escape(value: Any) -> str:
    return html.escape(
        str(value if value is not None else "—")
    )


def json_default(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()

    if hasattr(value, "tolist"):
        return value.tolist()

    if isinstance(value, set):
        return list(value)

    return str(value)


def json_text(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        default=json_default,
    )


def download_name(prefix: str) -> str:
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    return f"{prefix}_{timestamp}.json"


def status_chinese(status: Any) -> str:
    translations = {
        "PASS": "通過",
        "CAUTION": "注意",
        "FAIL": "失敗",
        "COMPLETED": "已完成",
        "NOT_AVAILABLE": "不適用",
        "NOT_TESTABLE": "無法測試",
        "DISABLED": "已停用",
        "ROBUST": "穩健",
        "FRAGILE": "脆弱",
        "OFFICIAL": "正式推薦",
        "REFERENCE_ONLY": "僅供參考",
        "FAIR_OR_BETTER": "價格合理或更佳",
        "MIXED_PRICE": "價格訊號混合",
        "SLIGHTLY_UNDERPAID": "輕微回報不足",
        "POOR_PRICE": "價格偏差",
        "SEVERELY_UNDERPAID": "嚴重回報不足",
        "UNKNOWN": "未知",
    }

    text = str(status or "UNKNOWN")
    return translations.get(
        text,
        text.replace("_", " "),
    )


def status_css_class(status: Any) -> str:
    status = str(status or "").upper()

    if status in {
        "PASS",
        "COMPLETED",
        "ROBUST",
        "OFFICIAL",
        "FAIR_OR_BETTER",
    }:
        return "status-pass"

    if status in {
        "CAUTION",
        "FRAGILE",
        "MIXED_PRICE",
        "SLIGHTLY_UNDERPAID",
        "NOT_AVAILABLE",
        "NOT_TESTABLE",
        "DISABLED",
    }:
        return "status-caution"

    return "status-fail"


def translate_reason(reason: Any) -> str:
    translations = {
        "BELOW_MINIMUM_ODDS": "賠率低於最低限制",
        "ABOVE_MAXIMUM_ODDS": "賠率高於最高限制",
        "NO_VALID_RECONSTRUCTION": "沒有有效市場重建情境",
        "PRIMARY_SOURCE_SCENARIOS_INCOMPLETE": "主要尖銳來源情境不完整",
        "MODEL_QUALITY_GATE_FAILED": "模型品質閘門未通過",
        "HT_UNDERIDENTIFIED_REFERENCE_ONLY": "半場市場辨識不足，只供參考",
        "HT_FT_COHERENCE_FAILED": "半場與全場一致性測試失敗",
        "BELOW_OPTIONAL_EV_FLOOR": "低於自訂期望值下限",
        "PERIOD_MODEL_UNAVAILABLE": "該時段模型不可用",
        "BASE_CANDIDATE_INELIGIBLE": "候選盤本身不合資格",
        "NO_CONSERVATIVE_HIT_PROBABILITY": "沒有保守命中概率",
        "BELOW_MINIMUM_OFFICIAL_HIT_PROBABILITY": "低於正式推薦最低命中率",
        "CONFLICTS_WITH_HIGHER_RANKED_OFFICIAL_PICK": "與較高排名推薦衝突",
        "MAXIMUM_RECOMMENDATIONS_REACHED": "已達正式推薦數目上限",
    }

    text = str(reason or "")

    return translations.get(
        text,
        text.replace("_", " "),
    )


# ============================================================
# 4. Bulk odds parsers
# ============================================================

def parse_triplet(
    text: str,
    label: str,
    *,
    required: bool,
    allow_skips: bool,
) -> Optional[Dict[str, Optional[float]]]:
    if not str(text).strip():
        if required:
            raise ValueError(
                f"{label} 不可留空。"
            )

        return None

    tokens = tokenize(text)

    if len(tokens) != 3:
        raise ValueError(
            f"{label} 必須輸入三個賠率："
            "主／和／客。"
        )

    values = []

    for index, token in enumerate(tokens):
        position = ["主", "和", "客"][index]

        if is_skip_token(token):
            if not allow_skips:
                raise ValueError(
                    f"{label} 的{position}賠率不可留空。"
                )

            values.append(None)
            continue

        values.append(
            validate_odds(
                token,
                f"{label} {position}",
            )
        )

    if all(value is None for value in values):
        return None

    return {
        "home": values[0],
        "draw": values[1],
        "away": values[2],
    }


def parse_two_way_ladder(
    text: str,
    label: str,
    *,
    market: str,
    allow_skips: bool,
) -> List[Dict[str, Any]]:
    rows = []
    seen_lines = set()

    for row_number, raw_row in enumerate(
        str(text).splitlines(),
        start=1,
    ):
        raw_row = raw_row.strip()

        if not raw_row:
            continue

        tokens = tokenize(raw_row)

        if len(tokens) != 3:
            raise ValueError(
                f"{label} 第 {row_number} 行格式錯誤。"
                "每行必須有：盤口 賠率1 賠率2。"
            )

        line = validate_quarter_line(
            tokens[0],
            f"{label} 第 {row_number} 行盤口",
        )

        if line in seen_lines:
            raise ValueError(
                f"{label} 出現重複盤口 {line:g}。"
            )

        seen_lines.add(line)

        prices: List[Optional[float]] = []

        for index, token in enumerate(tokens[1:]):
            if is_skip_token(token):
                if not allow_skips:
                    raise ValueError(
                        f"{label} 第 {row_number} 行"
                        "的兩邊賠率都必須提供。"
                    )

                prices.append(None)
            else:
                prices.append(
                    validate_odds(
                        token,
                        (
                            f"{label} 第 {row_number} 行"
                            f"賠率 {index + 1}"
                        ),
                    )
                )

        if all(price is None for price in prices):
            raise ValueError(
                f"{label} 第 {row_number} 行"
                "最少需要一個賠率。"
            )

        if market == "AH":
            rows.append(
                {
                    "line": line,
                    "home": prices[0],
                    "away": prices[1],
                }
            )
        else:
            rows.append(
                {
                    "line": line,
                    "over": prices[0],
                    "under": prices[1],
                }
            )

    return rows


def parse_hhad_ladder(
    text: str,
    label: str,
    *,
    allow_skips: bool,
) -> List[Dict[str, Any]]:
    rows = []
    seen_lines = set()

    for row_number, raw_row in enumerate(
        str(text).splitlines(),
        start=1,
    ):
        raw_row = raw_row.strip()

        if not raw_row:
            continue

        tokens = tokenize(raw_row)

        if len(tokens) != 4:
            raise ValueError(
                f"{label} 第 {row_number} 行格式錯誤。"
                "每行必須有：讓球 主勝 和 客勝。"
            )

        line = validate_integer_line(
            tokens[0],
            f"{label} 第 {row_number} 行讓球",
        )

        if line in seen_lines:
            raise ValueError(
                f"{label} 出現重複讓球 {line:g}。"
            )

        seen_lines.add(line)
        prices = []

        for index, token in enumerate(tokens[1:]):
            if is_skip_token(token):
                if not allow_skips:
                    raise ValueError(
                        f"{label} 第 {row_number} 行"
                        "的三個賠率都必須提供。"
                    )

                prices.append(None)
            else:
                prices.append(
                    validate_odds(
                        token,
                        (
                            f"{label} 第 {row_number} 行"
                            f"賠率 {index + 1}"
                        ),
                    )
                )

        if all(price is None for price in prices):
            raise ValueError(
                f"{label} 第 {row_number} 行"
                "最少需要一個賠率。"
            )

        rows.append(
            {
                "line": line,
                "home": prices[0],
                "draw": prices[1],
                "away": prices[2],
            }
        )

    return rows


def parse_team_ou_ladder(
    text: str,
    label: str,
    *,
    allow_skips: bool,
) -> List[Dict[str, Any]]:
    rows = []
    seen_keys = set()

    for row_number, raw_row in enumerate(
        str(text).splitlines(),
        start=1,
    ):
        raw_row = raw_row.strip()

        if not raw_row:
            continue

        tokens = tokenize(raw_row)

        if len(tokens) != 4:
            raise ValueError(
                f"{label} 第 {row_number} 行格式錯誤。"
                "每行必須有：HOME/ AWAY 盤口 大賠率 細賠率。"
            )

        team = tokens[0].strip().upper()

        if team not in {"HOME", "AWAY"}:
            raise ValueError(
                f"{label} 第 {row_number} 行球隊"
                "必須是 HOME 或 AWAY。"
            )

        line = validate_quarter_line(
            tokens[1],
            f"{label} 第 {row_number} 行盤口",
        )

        row_key = (team, line)

        if row_key in seen_keys:
            raise ValueError(
                f"{label} 出現重複盤口："
                f"{team} {line:g}。"
            )

        seen_keys.add(row_key)
        prices = []

        for index, token in enumerate(tokens[2:]):
            if is_skip_token(token):
                if not allow_skips:
                    raise ValueError(
                        f"{label} 第 {row_number} 行"
                        "的大細賠率都必須提供。"
                    )

                prices.append(None)
            else:
                prices.append(
                    validate_odds(
                        token,
                        (
                            f"{label} 第 {row_number} 行"
                            f"賠率 {index + 1}"
                        ),
                    )
                )

        if all(price is None for price in prices):
            raise ValueError(
                f"{label} 第 {row_number} 行"
                "最少需要一個賠率。"
            )

        rows.append(
            {
                "team": team,
                "line": line,
                "over": prices[0],
                "under": prices[1],
            }
        )

    return rows


# ============================================================
# 5. Default JSON example
# ============================================================

def example_json_input() -> Dict[str, Any]:
    return {
        "match": {
            "name": "主隊 vs 客隊",
            "home": "主隊",
            "away": "客隊",
            "competition": "賽事名稱",
            "kickoff": "",
            "snapshot_time": "",
        },
        "sharp_books": [
            {
                "key": "pinnacle",
                "title": "Pinnacle",
                "markets": {
                    "FT": {
                        "1X2": {
                            "home": 2.12,
                            "draw": 3.35,
                            "away": 3.55,
                        },
                        "AH": [
                            {
                                "line": -0.25,
                                "home": 1.95,
                                "away": 1.95,
                            },
                            {
                                "line": 0.0,
                                "home": 1.72,
                                "away": 2.18,
                            },
                        ],
                        "OU": [
                            {
                                "line": 2.25,
                                "over": 1.92,
                                "under": 1.98,
                            },
                            {
                                "line": 2.5,
                                "over": 2.12,
                                "under": 1.78,
                            },
                        ],
                        "HHAD": [],
                        "TEAM_OU": [],
                    }
                },
            }
        ],
        "hkjc_markets": [
            {
                "id": "M001",
                "period": "FT",
                "market": "1X2",
                "selection": "HOME",
                "odds": 2.15,
            },
            {
                "id": "M002",
                "period": "FT",
                "market": "AH",
                "selection": "HOME",
                "line": -0.25,
                "odds": 1.95,
            },
            {
                "id": "M003",
                "period": "FT",
                "market": "OU",
                "selection": "UNDER",
                "line": 2.5,
                "odds": 1.82,
            },
        ],
        "settings": {
            "minimum_odds": 1.5,
            "maximum_odds": None,
            "max_recommendations": 3,
            "minimum_official_hit_probability": 0.5,
            "correct_score_count": 2,
            "devig_methods": [
                "MULTIPLICATIVE",
                "POWER",
            ],
            "primary_source": "pinnacle",
            "ev_rejection_floor": None,
            "features": {
                "quality_gate": True,
                "stress_audit": True,
                "family_out_audit": True,
                "adaptive_grids": True,
                "ht_ft_coherence": True,
            },
        },
    }


# ============================================================
# 6. Session state
# ============================================================

SESSION_DEFAULTS = {
    "ultra_result": None,
    "ultra_input": None,
    "ultra_analysis_hash": None,
    "ultra_error": None,
    "ultra_traceback": None,
    "ultra_json_text": json_text(
        example_json_input()
    ),
}

for state_key, state_value in SESSION_DEFAULTS.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = state_value


# ============================================================
# 7. Cached engine execution
# ============================================================

@st.cache_data(
    show_spinner=False,
    max_entries=32,
)
def cached_engine_run(
    canonical_json: str,
    engine_fingerprint: str,
) -> Dict[str, Any]:
    del engine_fingerprint

    return aegis.run_engine(
        json.loads(canonical_json)
    )


def execute_engine(
    input_data: Dict[str, Any],
) -> Dict[str, Any]:
    canonical_json = json.dumps(
        input_data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=json_default,
    )

    try:
        with open(
            aegis.__file__,
            "rb",
        ) as engine_file:
            engine_fingerprint = hashlib.sha256(
                engine_file.read()
            ).hexdigest()
    except OSError:
        engine_fingerprint = str(
            ENGINE_VERSION
        )

    analysis_hash = hashlib.sha256(
        (
            canonical_json
            + engine_fingerprint
        ).encode("utf-8")
    ).hexdigest()

    if (
        st.session_state.ultra_analysis_hash
        == analysis_hash
        and st.session_state.ultra_result
        is not None
    ):
        return st.session_state.ultra_result

    result = cached_engine_run(
        canonical_json,
        engine_fingerprint,
    )

    st.session_state.ultra_analysis_hash = (
        analysis_hash
    )
    st.session_state.ultra_result = result
    st.session_state.ultra_input = result.get(
        "input_snapshot",
        deepcopy(input_data),
    )

    return result


# ============================================================
# 8. Header
# ============================================================

st.markdown(
    f"""
    <div class="ultra-hero">
        <div class="ultra-badge">
            Bulk odds command center · App V{APP_VERSION}
        </div>
        <h1 class="ultra-title">
            🛡️ AEGIS ULTRA
        </h1>
        <p class="ultra-subtitle">
            保留原版快速工作流程：直接從 Gemini、ChatGPT
            或其他來源複製整批賠率，貼入文字框後一次分析。
            支援 FT、HT、多個尖銳來源、1X2、AH、O/U、
            HHAD 及球隊入球大細。
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 9. Sidebar
# ============================================================

with st.sidebar:
    st.markdown("## 🛡️ AEGIS ULTRA")

    st.caption(
        f"App V{APP_VERSION} · Engine V{ENGINE_VERSION}"
    )

    st.success(
        "批量貼上賠率\n\n"
        "不需要逐個欄位輸入"
    )

    st.divider()

    input_mode = st.radio(
        "輸入模式",
        options=[
            "🎛️ 批量貼上",
            "📋 貼上 JSON",
            "📁 上載 JSON",
        ],
        index=0,
    )

    st.divider()

    st.markdown("### 分析原則")

    st.write("• Target-line-out 重建")
    st.write("• 保守命中率優先")
    st.write("• 正式推薦衝突過濾")
    st.write("• EV 只作價格審核")
    st.write("• 所有輸入盤口保留顯示")

    st.divider()

    if st.button(
        "🗑️ 清除目前分析",
        use_container_width=True,
    ):
        st.session_state.ultra_result = None
        st.session_state.ultra_input = None
        st.session_state.ultra_analysis_hash = None
        st.session_state.ultra_error = None
        st.session_state.ultra_traceback = None
        st.rerun()


# ============================================================
# 10. Bulk input rendering
# ============================================================

def render_sharp_period(
    source_index: int,
    period: str,
    *,
    enabled_default: bool,
) -> Optional[Dict[str, str]]:
    period_name = (
        "全場 FT"
        if period == "FT"
        else "半場 HT"
    )

    enabled = st.checkbox(
        f"啟用{period_name}市場",
        value=enabled_default,
        key=f"sharp_enable_{source_index}_{period}",
    )

    if not enabled:
        st.info(
            f"此來源未啟用{period_name}。"
        )
        return None

    one_x_two = st.text_input(
        f"{period} 1X2 — 主勝／和／客勝",
        placeholder="2.20 3.60 3.40",
        key=f"sharp_1x2_{source_index}_{period}",
    )

    first, second = st.columns(2)

    with first:
        ah = st.text_area(
            f"{period} 亞洲讓球 AH",
            placeholder=(
                "主隊讓球線 主隊賠率 客隊賠率\n"
                "0.00 1.65 2.30\n"
                "-0.25 1.98 1.92\n"
                "-0.50 2.20 1.72"
            ),
            height=220,
            key=f"sharp_ah_{source_index}_{period}",
            help=(
                "第一個數字永遠是套用於主隊的讓球線。"
            ),
        )

    with second:
        ou = st.text_area(
            f"{period} 入球大細 O/U",
            placeholder=(
                "入球線 大盤賠率 細盤賠率\n"
                "2.00 1.75 2.15\n"
                "2.25 2.02 1.88\n"
                "2.50 2.35 1.68"
            ),
            height=220,
            key=f"sharp_ou_{source_index}_{period}",
        )

    third, fourth = st.columns(2)

    with third:
        if period == "FT":
            hhad = st.text_area(
                "FT 讓球主客和 HHAD",
                placeholder=(
                    "主隊讓球 主勝 和 客勝\n"
                    "-1 3.60 3.75 1.72\n"
                    "+1 1.45 4.20 5.80"
                ),
                height=170,
                key=f"sharp_hhad_{source_index}_{period}",
            )
        else:
            hhad = ""

    with fourth:
        team_ou = st.text_area(
            f"{period} 球隊入球大細",
            placeholder=(
                "球隊 入球線 大盤賠率 細盤賠率\n"
                "HOME 1.50 2.05 1.78\n"
                "AWAY 1.00 1.85 2.00"
            ),
            height=170,
            key=f"sharp_team_ou_{source_index}_{period}",
        )

    return {
        "1X2": one_x_two,
        "AH": ah,
        "OU": ou,
        "HHAD": hhad,
        "TEAM_OU": team_ou,
    }


def render_hkjc_period(
    period: str,
) -> Dict[str, str]:
    period_name = (
        "全場 FT"
        if period == "FT"
        else "半場 HT"
    )

    st.markdown(
        f"### {period_name}"
    )

    st.caption(
        "沒有提供的賠率可輸入 X 或 -。"
        "所有有效盤口會自動轉換成候選盤。"
    )

    one_x_two = st.text_input(
        f"HKJC {period} 1X2 — 主勝／和／客勝",
        placeholder="2.25 3.45 3.25",
        key=f"hkjc_1x2_{period}",
    )

    first, second = st.columns(2)

    with first:
        ah = st.text_area(
            f"HKJC {period} AH",
            placeholder=(
                "主隊讓球線 主隊賠率 客隊賠率\n"
                "+0.25 1.86 2.02\n"
                "0.00 1.65 2.30\n"
                "-0.25 2.05 1.85"
            ),
            height=225,
            key=f"hkjc_ah_{period}",
        )

    with second:
        ou = st.text_area(
            f"HKJC {period} O/U",
            placeholder=(
                "入球線 大盤賠率 細盤賠率\n"
                "2.25 1.95 1.85\n"
                "2.50 2.18 1.70\n"
                "2.75 X 1.55"
            ),
            height=225,
            key=f"hkjc_ou_{period}",
        )

    third, fourth = st.columns(2)

    with third:
        if period == "FT":
            hhad = st.text_area(
                "HKJC FT 讓球主客和 HHAD",
                placeholder=(
                    "主隊讓球 主勝 和 客勝\n"
                    "-1 3.60 3.75 1.72\n"
                    "+1 1.45 X 5.80"
                ),
                height=180,
                key=f"hkjc_hhad_{period}",
            )
        else:
            hhad = ""

    with fourth:
        team_ou = st.text_area(
            f"HKJC {period} 球隊入球大細",
            placeholder=(
                "球隊 入球線 大盤賠率 細盤賠率\n"
                "HOME 1.50 2.05 1.78\n"
                "AWAY 1.00 X 2.00"
            ),
            height=180,
            key=f"hkjc_team_ou_{period}",
        )

    return {
        "1X2": one_x_two,
        "AH": ah,
        "OU": ou,
        "HHAD": hhad,
        "TEAM_OU": team_ou,
    }


# ============================================================
# 11. Input construction
# ============================================================

def build_sharp_period(
    raw: Dict[str, str],
    source_title: str,
    period: str,
) -> Dict[str, Any]:
    return {
        "1X2": parse_triplet(
            raw["1X2"],
            f"{source_title} {period} 1X2",
            required=False,
            allow_skips=False,
        ),
        "AH": parse_two_way_ladder(
            raw["AH"],
            f"{source_title} {period} AH",
            market="AH",
            allow_skips=False,
        ),
        "OU": parse_two_way_ladder(
            raw["OU"],
            f"{source_title} {period} O/U",
            market="OU",
            allow_skips=False,
        ),
        "HHAD": (
            parse_hhad_ladder(
                raw["HHAD"],
                f"{source_title} {period} HHAD",
                allow_skips=False,
            )
            if period == "FT"
            else []
        ),
        "TEAM_OU": parse_team_ou_ladder(
            raw["TEAM_OU"],
            f"{source_title} {period} 球隊入球大細",
            allow_skips=False,
        ),
    }


def period_has_market(
    markets: Dict[str, Any],
) -> bool:
    return any(
        bool(markets.get(market))
        for market in [
            "1X2",
            "AH",
            "OU",
            "HHAD",
            "TEAM_OU",
        ]
    )


def build_hkjc_candidates(
    *,
    home_name: str,
    away_name: str,
    raw_periods: Dict[str, Dict[str, str]],
) -> List[Dict[str, Any]]:
    candidates = []
    counter = 1

    def add_candidate(
        *,
        period: str,
        market: str,
        selection: str,
        odds: float,
        label: str,
        line: Optional[float] = None,
        team: Optional[str] = None,
    ) -> None:
        nonlocal counter

        candidate = {
            "id": f"M{counter:03d}",
            "label": label,
            "period": period,
            "market": market,
            "selection": selection,
            "odds": odds,
        }

        if line is not None:
            candidate["line"] = line

        if team is not None:
            candidate["team"] = team

        candidates.append(candidate)
        counter += 1

    for period in ["FT", "HT"]:
        raw = raw_periods[period]
        period_label = "全場" if period == "FT" else "半場"

        one_x_two = parse_triplet(
            raw["1X2"],
            f"HKJC {period} 1X2",
            required=False,
            allow_skips=True,
        )

        if one_x_two:
            specs = [
                (
                    "home",
                    "HOME",
                    f"{home_name} {period_label}勝",
                ),
                (
                    "draw",
                    "DRAW",
                    f"{period_label}和",
                ),
                (
                    "away",
                    "AWAY",
                    f"{away_name} {period_label}勝",
                ),
            ]

            for key, selection, label in specs:
                odds = one_x_two.get(key)

                if odds is not None:
                    add_candidate(
                        period=period,
                        market="1X2",
                        selection=selection,
                        odds=odds,
                        label=label,
                    )

        ah_rows = parse_two_way_ladder(
            raw["AH"],
            f"HKJC {period} AH",
            market="AH",
            allow_skips=True,
        )

        for row in ah_rows:
            if row["home"] is not None:
                add_candidate(
                    period=period,
                    market="AH",
                    selection="HOME",
                    line=row["line"],
                    odds=row["home"],
                    label=(
                        f"{home_name} "
                        f"{period_label} AH "
                        f"{row['line']:+g}"
                    ),
                )

            if row["away"] is not None:
                add_candidate(
                    period=period,
                    market="AH",
                    selection="AWAY",
                    line=row["line"],
                    odds=row["away"],
                    label=(
                        f"{away_name} "
                        f"{period_label} AH "
                        f"{-row['line']:+g}"
                    ),
                )

        ou_rows = parse_two_way_ladder(
            raw["OU"],
            f"HKJC {period} O/U",
            market="OU",
            allow_skips=True,
        )

        for row in ou_rows:
            if row["over"] is not None:
                add_candidate(
                    period=period,
                    market="OU",
                    selection="OVER",
                    line=row["line"],
                    odds=row["over"],
                    label=(
                        f"{period_label}入球大 "
                        f"{row['line']:g}"
                    ),
                )

            if row["under"] is not None:
                add_candidate(
                    period=period,
                    market="OU",
                    selection="UNDER",
                    line=row["line"],
                    odds=row["under"],
                    label=(
                        f"{period_label}入球細 "
                        f"{row['line']:g}"
                    ),
                )

        if period == "FT":
            hhad_rows = parse_hhad_ladder(
                raw["HHAD"],
                "HKJC FT HHAD",
                allow_skips=True,
            )

            for row in hhad_rows:
                hhad_specs = [
                    (
                        "home",
                        "HOME",
                        f"{home_name} 讓球主勝 {row['line']:+g}",
                    ),
                    (
                        "draw",
                        "DRAW",
                        f"讓球和 {row['line']:+g}",
                    ),
                    (
                        "away",
                        "AWAY",
                        f"{away_name} 讓球客勝 {row['line']:+g}",
                    ),
                ]

                for key, selection, label in hhad_specs:
                    odds = row.get(key)

                    if odds is not None:
                        add_candidate(
                            period="FT",
                            market="HHAD",
                            selection=selection,
                            line=row["line"],
                            odds=odds,
                            label=label,
                        )

        team_rows = parse_team_ou_ladder(
            raw["TEAM_OU"],
            f"HKJC {period} 球隊入球大細",
            allow_skips=True,
        )

        for row in team_rows:
            team_name = (
                home_name
                if row["team"] == "HOME"
                else away_name
            )

            if row["over"] is not None:
                add_candidate(
                    period=period,
                    market="TEAM_OU",
                    selection="OVER",
                    team=row["team"],
                    line=row["line"],
                    odds=row["over"],
                    label=(
                        f"{team_name} {period_label}"
                        f"入球大 {row['line']:g}"
                    ),
                )

            if row["under"] is not None:
                add_candidate(
                    period=period,
                    market="TEAM_OU",
                    selection="UNDER",
                    team=row["team"],
                    line=row["line"],
                    odds=row["under"],
                    label=(
                        f"{team_name} {period_label}"
                        f"入球細 {row['line']:g}"
                    ),
                )

    if not candidates:
        raise ValueError(
            "最少需要輸入一個 HKJC 候選盤。"
        )

    return candidates


# ============================================================
# 12. Main input interface
# ============================================================

input_to_run = None
input_preview = None


if input_mode == "🎛️ 批量貼上":
    st.markdown(
        '<div class="section-label">Bulk input workflow</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-panel">
            <b>你可以直接貼上整批賠率。</b><br>
            每個盤口一行，空白或逗號均可分隔。
            不需要逐格輸入，也不需要手動新增表格列。
        </div>
        """,
        unsafe_allow_html=True,
    )

    match_tab, sharp_tab, hkjc_tab, policy_tab = st.tabs(
        [
            "① 賽事資料",
            "② 尖銳市場",
            "③ HKJC 候選盤",
            "④ 推薦設定",
        ]
    )

    with match_tab:
        st.subheader("賽事資料")

        first, second = st.columns(2)

        with first:
            home_name = st.text_input(
                "主隊",
                key="ultra_home_name",
            )

            competition = st.text_input(
                "賽事",
                placeholder="例如：英格蘭超級聯賽",
                key="ultra_competition",
            )

            kickoff = st.text_input(
                "開賽時間",
                placeholder="例如：2026-08-15 22:00 HKT",
                key="ultra_kickoff",
            )

        with second:
            away_name = st.text_input(
                "客隊",
                key="ultra_away_name",
            )

            custom_match_name = st.text_input(
                "自訂賽事名稱",
                placeholder="留空時自動使用「主隊 vs 客隊」",
                key="ultra_match_name",
            )

            snapshot_time = st.text_input(
                "市場快照時間",
                value=(
                    datetime.now()
                    .astimezone()
                    .isoformat(timespec="minutes")
                ),
                key="ultra_snapshot_time",
            )

    sharp_sources_raw = []

    with sharp_tab:
        st.subheader("尖銳市場來源")

        st.markdown(
            """
            <div class="format-panel">
                <b>AH 格式：</b>
                主隊讓球線　主隊賠率　客隊賠率<br>
                <b>O/U 格式：</b>
                入球線　大盤賠率　細盤賠率<br>
                <b>HHAD 格式：</b>
                主隊整數讓球　主勝　和　客勝<br>
                <b>球隊 O/U 格式：</b>
                HOME/AWAY　入球線　大盤賠率　細盤賠率
            </div>
            """,
            unsafe_allow_html=True,
        )

        source_count = st.number_input(
            "尖銳來源數目",
            min_value=1,
            max_value=5,
            value=1,
            step=1,
            key="ultra_source_count",
        )

        for source_index in range(
            int(source_count)
        ):
            default_key = (
                "pinnacle"
                if source_index == 0
                else f"source_{source_index + 1}"
            )

            default_title = (
                "Pinnacle"
                if source_index == 0
                else f"Sharp Source {source_index + 1}"
            )

            with st.container(border=True):
                st.markdown(
                    f"### ⚡ 尖銳來源 {source_index + 1}"
                )

                first, second = st.columns(2)

                with first:
                    source_key = st.text_input(
                        "來源識別碼",
                        value=default_key,
                        key=f"source_key_{source_index}",
                    )

                with second:
                    source_title = st.text_input(
                        "來源名稱",
                        value=default_title,
                        key=f"source_title_{source_index}",
                    )

                ft_source_tab, ht_source_tab = st.tabs(
                    [
                        "全場 FT",
                        "半場 HT",
                    ]
                )

                with ft_source_tab:
                    ft_raw = render_sharp_period(
                        source_index,
                        "FT",
                        enabled_default=True,
                    )

                with ht_source_tab:
                    ht_raw = render_sharp_period(
                        source_index,
                        "HT",
                        enabled_default=False,
                    )

                sharp_sources_raw.append(
                    {
                        "key": source_key,
                        "title": source_title,
                        "FT": ft_raw,
                        "HT": ht_raw,
                    }
                )

        available_source_keys = [
            optional_text(source["key"]).lower()
            for source in sharp_sources_raw
            if optional_text(source["key"])
        ]

        primary_source = st.selectbox(
            "主要尖銳來源",
            options=(
                available_source_keys
                or ["pinnacle"]
            ),
            index=0,
            key="ultra_primary_source",
        )

    with hkjc_tab:
        st.subheader("HKJC 候選盤")

        st.markdown(
            """
            <div class="format-panel">
                可直接貼上 AI 整理好的完整賠率列表。
                使用 <b>X</b> 或 <b>-</b> 表示該邊沒有賠率。
                系統會自動建立每一個候選盤及 ID。
            </div>
            """,
            unsafe_allow_html=True,
        )

        ft_hkjc_tab, ht_hkjc_tab = st.tabs(
            [
                "全場 FT",
                "半場 HT",
            ]
        )

        with ft_hkjc_tab:
            hkjc_ft_raw = render_hkjc_period(
                "FT"
            )

        with ht_hkjc_tab:
            hkjc_ht_raw = render_hkjc_period(
                "HT"
            )

    with policy_tab:
        st.subheader("正式推薦設定")

        first, second, third = st.columns(3)

        with first:
            minimum_odds = st.number_input(
                "最低 HKJC 賠率",
                min_value=1.01,
                max_value=1000.0,
                value=1.50,
                step=0.05,
                format="%.2f",
                key="ultra_minimum_odds",
            )

        with second:
            maximum_recommendations = st.selectbox(
                "正式推薦數目上限",
                options=[
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                ],
                index=2,
                key="ultra_max_recommendations",
            )

        with third:
            minimum_hit_probability_pct = (
                st.number_input(
                    "最低保守命中率 (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=50.0,
                    step=1.0,
                    format="%.1f",
                    key="ultra_minimum_hit_pct",
                )
            )

        first, second = st.columns(2)

        with first:
            use_maximum_odds = st.checkbox(
                "設定最高 HKJC 賠率",
                value=False,
                key="ultra_use_maximum_odds",
            )

            if use_maximum_odds:
                maximum_odds = st.number_input(
                    "最高 HKJC 賠率",
                    min_value=1.01,
                    max_value=1000.0,
                    value=10.00,
                    step=0.10,
                    format="%.2f",
                    key="ultra_maximum_odds",
                )
            else:
                maximum_odds = None

        with second:
            correct_score_count = st.selectbox(
                "波膽參考數目",
                options=[0, 1, 2, 3, 4, 5],
                index=2,
                key="ultra_correct_score_count",
            )

        devig_methods = st.multiselect(
            "去水情境",
            options=[
                "MULTIPLICATIVE",
                "POWER",
            ],
            default=[
                "MULTIPLICATIVE",
                "POWER",
            ],
            key="ultra_devig_methods",
        )

        use_ev_floor = st.checkbox(
            "拒絕嚴重回報不足的價格",
            value=False,
            key="ultra_use_ev_floor",
        )

        if use_ev_floor:
            ev_floor_pct = st.number_input(
                "最低容許 EV (%)",
                min_value=-100.0,
                max_value=500.0,
                value=-10.0,
                step=1.0,
                format="%.1f",
                key="ultra_ev_floor_pct",
            )
        else:
            ev_floor_pct = -10.0

        with st.expander(
            "進階引擎功能",
            expanded=True,
        ):
            quality_gate = st.checkbox(
                "模型品質閘門",
                value=True,
                key="ultra_quality_gate",
            )

            stress_audit = st.checkbox(
                "輕／中／重壓力測試",
                value=True,
                key="ultra_stress_audit",
            )

            family_out_audit = st.checkbox(
                "整個市場族群移除測試",
                value=True,
                key="ultra_family_out_audit",
            )

            adaptive_grids = st.checkbox(
                "自適應入球網格",
                value=True,
                key="ultra_adaptive_grids",
            )

            ht_ft_coherence = st.checkbox(
                "半場－全場一致性測試",
                value=True,
                key="ultra_ht_ft_coherence",
            )

    st.divider()

    run_manual = st.button(
        "🚀 開始 AEGIS ULTRA 分析",
        type="primary",
        use_container_width=True,
        key="ultra_manual_run",
    )

    if run_manual:
        try:
            clean_home = optional_text(
                home_name
            )
            clean_away = optional_text(
                away_name
            )

            if not clean_home or not clean_away:
                raise ValueError(
                    "主隊及客隊不可留空。"
                )

            if (
                clean_home.casefold()
                == clean_away.casefold()
            ):
                raise ValueError(
                    "主隊及客隊不可相同。"
                )

            if not devig_methods:
                raise ValueError(
                    "最少需要選擇一種去水方法。"
                )

            sharp_books = []
            seen_source_keys = set()

            for source_index, source in enumerate(
                sharp_sources_raw,
                start=1,
            ):
                source_key = optional_text(
                    source["key"]
                ).lower()

                source_title = (
                    optional_text(source["title"])
                    or source_key
                )

                if not source_key:
                    raise ValueError(
                        f"尖銳來源 {source_index} "
                        "缺少識別碼。"
                    )

                if source_key in seen_source_keys:
                    raise ValueError(
                        f"尖銳來源識別碼重複："
                        f"{source_key}。"
                    )

                seen_source_keys.add(
                    source_key
                )

                markets = {}

                for period in ["FT", "HT"]:
                    raw_period = source.get(
                        period
                    )

                    if raw_period is None:
                        continue

                    parsed_markets = build_sharp_period(
                        raw_period,
                        source_title,
                        period,
                    )

                    if not period_has_market(
                        parsed_markets
                    ):
                        raise ValueError(
                            f"{source_title} {period} "
                            "已啟用，但沒有輸入任何市場。"
                        )

                    markets[period] = (
                        parsed_markets
                    )

                if not markets:
                    raise ValueError(
                        f"{source_title} 沒有啟用"
                        "任何 FT 或 HT 市場。"
                    )

                sharp_books.append(
                    {
                        "key": source_key,
                        "title": source_title,
                        "timestamp": optional_text(
                            snapshot_time
                        ),
                        "markets": markets,
                    }
                )

            if primary_source not in {
                source["key"]
                for source in sharp_books
            }:
                raise ValueError(
                    "主要尖銳來源不在已建立的來源中。"
                )

            hkjc_markets = build_hkjc_candidates(
                home_name=clean_home,
                away_name=clean_away,
                raw_periods={
                    "FT": hkjc_ft_raw,
                    "HT": hkjc_ht_raw,
                },
            )

            match_name = (
                optional_text(custom_match_name)
                or f"{clean_home} vs {clean_away}"
            )

            input_to_run = {
                "match": {
                    "name": match_name,
                    "home": clean_home,
                    "away": clean_away,
                    "competition": optional_text(
                        competition
                    ),
                    "kickoff": optional_text(
                        kickoff
                    ),
                    "snapshot_time": optional_text(
                        snapshot_time
                    ),
                },
                "sharp_books": sharp_books,
                "hkjc_markets": hkjc_markets,
                "settings": {
                    "primary_source": primary_source,
                    "minimum_odds": float(
                        minimum_odds
                    ),
                    "maximum_odds": (
                        float(maximum_odds)
                        if maximum_odds is not None
                        else None
                    ),
                    "max_recommendations": int(
                        maximum_recommendations
                    ),
                    "minimum_official_hit_probability": (
                        float(
                            minimum_hit_probability_pct
                        )
                        / 100.0
                    ),
                    "correct_score_count": int(
                        correct_score_count
                    ),
                    "devig_methods": list(
                        devig_methods
                    ),
                    "ev_rejection_floor": (
                        float(ev_floor_pct) / 100.0
                        if use_ev_floor
                        else None
                    ),
                    "features": {
                        "quality_gate": bool(
                            quality_gate
                        ),
                        "stress_audit": bool(
                            stress_audit
                        ),
                        "family_out_audit": bool(
                            family_out_audit
                        ),
                        "adaptive_grids": bool(
                            adaptive_grids
                        ),
                        "ht_ft_coherence": bool(
                            ht_ft_coherence
                        ),
                    },
                },
            }

            input_preview = deepcopy(
                input_to_run
            )

        except Exception as input_error:
            st.session_state.ultra_error = str(
                input_error
            )
            st.session_state.ultra_traceback = (
                traceback.format_exc()
            )

            st.error(
                f"輸入錯誤：{input_error}"
            )


# ============================================================
# 13. Pasted JSON input
# ============================================================

elif input_mode == "📋 貼上 JSON":
    st.markdown(
        '<div class="section-label">Direct JSON input</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-panel">
            直接貼上完整的 AEGIS ULTRA 引擎輸入 JSON。
            此模式不會改寫 JSON 內的設定。
        </div>
        """,
        unsafe_allow_html=True,
    )

    json_input_value = st.text_area(
        "AEGIS ULTRA 輸入 JSON",
        key="ultra_json_text",
        height=650,
    )

    run_json = st.button(
        "🚀 執行貼上的 JSON",
        type="primary",
        use_container_width=True,
        key="ultra_json_run",
    )

    if run_json:
        try:
            parsed_json = json.loads(
                json_input_value
            )

            if not isinstance(
                parsed_json,
                dict,
            ):
                raise ValueError(
                    "JSON 最外層必須是物件。"
                )

            input_to_run = parsed_json
            input_preview = deepcopy(
                parsed_json
            )

        except Exception as json_error:
            st.session_state.ultra_error = str(
                json_error
            )
            st.session_state.ultra_traceback = (
                traceback.format_exc()
            )

            st.error(
                f"JSON 錯誤：{json_error}"
            )


# ============================================================
# 14. Uploaded JSON input
# ============================================================

else:
    st.markdown(
        '<div class="section-label">JSON file input</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "上載 AEGIS ULTRA JSON",
        type=["json"],
    )

    if uploaded_file is not None:
        try:
            uploaded_text = (
                uploaded_file
                .getvalue()
                .decode("utf-8-sig")
            )

            uploaded_preview = json.loads(
                uploaded_text
            )

            st.success(
                f"已讀取：{uploaded_file.name}"
            )

            with st.expander(
                "檢查上載內容",
                expanded=False,
            ):
                st.json(uploaded_preview)

        except Exception as preview_error:
            uploaded_preview = None

            st.error(
                f"無法讀取 JSON：{preview_error}"
            )
    else:
        uploaded_preview = None

    run_uploaded = st.button(
        "🚀 執行上載的 JSON",
        type="primary",
        use_container_width=True,
        key="ultra_upload_run",
    )

    if run_uploaded:
        try:
            if uploaded_preview is None:
                raise ValueError(
                    "請先上載有效的 JSON 檔案。"
                )

            if not isinstance(
                uploaded_preview,
                dict,
            ):
                raise ValueError(
                    "JSON 最外層必須是物件。"
                )

            input_to_run = uploaded_preview
            input_preview = deepcopy(
                uploaded_preview
            )

        except Exception as upload_error:
            st.session_state.ultra_error = str(
                upload_error
            )
            st.session_state.ultra_traceback = (
                traceback.format_exc()
            )

            st.error(
                f"JSON 錯誤：{upload_error}"
            )


# ============================================================
# 15. Execute engine
# ============================================================

if input_preview is not None:
    with st.expander(
        "檢查提交給引擎的完整資料",
        expanded=False,
    ):
        st.json(input_preview)

    st.download_button(
        "⬇️ 下載本次輸入 JSON",
        data=json_text(input_preview),
        file_name=download_name(
            "aegis_ultra_input"
        ),
        mime="application/json",
        use_container_width=True,
    )


if input_to_run is not None:
    st.session_state.ultra_error = None
    st.session_state.ultra_traceback = None

    try:
        with st.spinner(
            "正在重建尖銳市場、移除目標盤、"
            "執行壓力測試及正式推薦衝突檢查……"
        ):
            output = execute_engine(
                deepcopy(input_to_run)
            )

        st.success(
            "AEGIS ULTRA 分析已完成。"
        )

    except Exception as engine_error:
        st.session_state.ultra_error = str(
            engine_error
        )
        st.session_state.ultra_traceback = (
            traceback.format_exc()
        )

        st.error(
            f"引擎執行失敗：{engine_error}"
        )


# ============================================================
# 16. Error display
# ============================================================

if st.session_state.ultra_error:
    with st.expander(
        "顯示技術錯誤詳情",
        expanded=False,
    ):
        st.code(
            st.session_state.ultra_traceback
            or st.session_state.ultra_error,
            language="text",
        )


# ============================================================
# 17. Result helpers
# ============================================================

def result_summary_card(
    label: str,
    value: str,
    note: str,
    css_class: str = "",
) -> None:
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">
                {html_escape(label)}
            </div>
            <div class="summary-value {css_class}">
                {html_escape(value)}
            </div>
            <div class="summary-note">
                {html_escape(note)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def recommendation_card(
    recommendation: Dict[str, Any],
) -> None:
    rank = recommendation.get(
        "rank",
        recommendation.get(
            "official_rank",
            "—",
        ),
    )

    label = recommendation.get(
        "label",
        recommendation.get("id", "—"),
    )

    hit_min = probability_value(
        recommendation,
        "hit",
        "minimum",
    )

    hit_median = probability_value(
        recommendation,
        "hit",
        "median",
    )

    nonloss_min = probability_value(
        recommendation,
        "nonloss",
        "minimum",
    )

    full_loss_max = probability_value(
        recommendation,
        "full_loss",
        "maximum",
    )

    ev_min = summary_value(
        recommendation,
        "expected_return",
        "minimum",
    )

    price_status = recommendation.get(
        "price_status",
        "UNKNOWN",
    )

    price_class = (
        "price-good"
        if price_status == "FAIR_OR_BETTER"
        else "price-warning"
    )

    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-rank">
                OFFICIAL PICK #{html_escape(rank)}
            </div>
            <div class="recommendation-name">
                {html_escape(label)}
            </div>
            <div class="recommendation-stats">
                HKJC 賠率：
                <b>{format_odds(recommendation.get("hkjc_odds"))}</b>
                &nbsp;｜&nbsp;
                保守命中率：
                <b>{format_probability(hit_min)}</b>
                &nbsp;｜&nbsp;
                中位命中率：
                <b>{format_probability(hit_median)}</b>
                &nbsp;｜&nbsp;
                保守不輸率：
                <b>{format_probability(nonloss_min)}</b>
                <br>
                最大全輸率：
                <b>{format_probability(full_loss_max)}</b>
                &nbsp;｜&nbsp;
                保守 EV：
                <b>{format_ev(ev_min)}</b>
            </div>
            <div class="{price_class}">
                價格審核：{html_escape(status_chinese(price_status))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def candidate_dataframe(
    candidates: List[Dict[str, Any]],
) -> pd.DataFrame:
    rows = []

    for candidate in candidates:
        reasons = (
            candidate.get(
                "official_exclusion_reasons",
                [],
            )
            + candidate.get(
                "exclusion_reasons",
                [],
            )
        )

        conflicts = []

        for conflict in candidate.get(
            "conflicts_with",
            [],
        ):
            label = conflict.get(
                "selected_label"
            )

            if label:
                conflicts.append(str(label))

        rows.append(
            {
                "狀態": (
                    "✅ 正式推薦"
                    if candidate.get("official")
                    else "參考"
                ),
                "排名": candidate.get(
                    "official_rank"
                ),
                "ID": candidate.get("id"),
                "候選盤": candidate.get(
                    "label"
                ),
                "時段": candidate.get(
                    "period"
                ),
                "市場": candidate.get(
                    "market"
                ),
                "HKJC 賠率": candidate.get(
                    "hkjc_odds"
                ),
                "保守命中率": format_probability(
                    probability_value(
                        candidate,
                        "hit",
                        "minimum",
                    )
                ),
                "中位命中率": format_probability(
                    probability_value(
                        candidate,
                        "hit",
                        "median",
                    )
                ),
                "保守不輸率": format_probability(
                    probability_value(
                        candidate,
                        "nonloss",
                        "minimum",
                    )
                ),
                "最大全輸率": format_probability(
                    probability_value(
                        candidate,
                        "full_loss",
                        "maximum",
                    )
                ),
                "保守公平賠率": format_odds(
                    summary_value(
                        candidate,
                        "fair_odds",
                        "maximum",
                    )
                ),
                "保守 EV": format_ev(
                    summary_value(
                        candidate,
                        "expected_return",
                        "minimum",
                    )
                ),
                "價格": status_chinese(
                    candidate.get(
                        "price_status"
                    )
                ),
                "衝突項目": "、".join(
                    conflicts
                ),
                "排除原因": "；".join(
                    translate_reason(reason)
                    for reason in reasons
                ),
            }
        )

    return pd.DataFrame(rows)


def stress_dataframe(
    candidate: Dict[str, Any],
) -> pd.DataFrame:
    stress = candidate.get(
        "stress_audit",
        {},
    )

    rows = []

    for key, label in [
        ("light", "輕度"),
        ("medium", "中度"),
        ("heavy", "重度"),
    ]:
        record = stress.get(
            key,
            {},
        )

        rows.append(
            {
                "壓力程度": label,
                "最低命中率": format_probability(
                    record.get(
                        "minimum_hit_probability"
                    )
                ),
                "中位命中率": format_probability(
                    record.get(
                        "median_hit_probability"
                    )
                ),
                "有效情境數": record.get(
                    "scenario_count"
                ),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# 18. Results
# ============================================================

result = st.session_state.ultra_result

if result:
    st.divider()

    st.markdown(
        '<div class="section-label">Analysis result</div>',
        unsafe_allow_html=True,
    )

    match = result.get(
        "match",
        {},
    )

    match_name = match.get(
        "name",
        "賽事分析",
    )

    st.header(
        f"📡 {match_name}"
    )

    caption_parts = [
        match.get("competition"),
        match.get("kickoff"),
        match.get("snapshot_time"),
    ]

    caption = " ｜ ".join(
        str(value)
        for value in caption_parts
        if value
    )

    if caption:
        st.caption(caption)

    recommendations = result.get(
        "recommendations",
        [],
    )

    candidates = result.get(
        "candidate_markets",
        [],
    )

    quality_status = (
        result
        .get("model_quality", {})
        .get("status", "UNKNOWN")
    )

    coherence_status = (
        result
        .get("ht_ft_coherence", {})
        .get("status", "NOT_AVAILABLE")
    )

    runtime_seconds = (
        result
        .get("runtime", {})
        .get("total_seconds")
    )

    first, second, third, fourth = st.columns(4)

    with first:
        result_summary_card(
            "模型品質",
            status_chinese(
                quality_status
            ),
            "市場重建及網格品質",
            status_css_class(
                quality_status
            ),
        )

    with second:
        result_summary_card(
            "正式推薦",
            str(len(recommendations)),
            f"共分析 {len(candidates)} 個候選盤",
        )

    with third:
        result_summary_card(
            "HT–FT 一致性",
            status_chinese(
                coherence_status
            ),
            "半場與全場模型一致性",
            status_css_class(
                coherence_status
            ),
        )

    with fourth:
        result_summary_card(
            "執行時間",
            (
                f"{float(runtime_seconds):.2f} 秒"
                if runtime_seconds is not None
                else "—"
            ),
            f"Engine V{ENGINE_VERSION}",
        )

    result_tabs = st.tabs(
        [
            "正式推薦",
            "所有候選盤",
            "穩健性分析",
            "推薦組合",
            "波膽參考",
            "模型診斷",
            "完整 JSON",
        ]
    )

    # --------------------------------------------------------
    # Official recommendations
    # --------------------------------------------------------

    with result_tabs[0]:
        st.subheader("正式推薦")

        if recommendations:
            for recommendation in recommendations:
                recommendation_card(
                    recommendation
                )
        else:
            st.warning(
                "沒有候選盤通過所有正式推薦條件。"
                "所有輸入盤口仍可在「所有候選盤」查看。"
            )

        official_selection = result.get(
            "official_selection",
            {},
        )

        st.caption(
            "最低正式推薦命中率："
            + format_probability(
                official_selection.get(
                    "minimum_hit_probability"
                )
            )
            + " ｜ 推薦數目上限："
            + str(
                official_selection.get(
                    "maximum_recommendations",
                    "—",
                )
            )
        )

    # --------------------------------------------------------
    # All candidates
    # --------------------------------------------------------

    with result_tabs[1]:
        st.subheader("所有候選盤")

        candidate_table = candidate_dataframe(
            candidates
        )

        if candidate_table.empty:
            st.info("沒有候選盤結果。")
        else:
            st.dataframe(
                candidate_table,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "HKJC 賠率": st.column_config.NumberColumn(
                        "HKJC 賠率",
                        format="%.3f",
                    ),
                },
            )

        with st.expander(
            "逐項排除及衝突詳情",
            expanded=False,
        ):
            reference_candidates = [
                candidate
                for candidate in candidates
                if not candidate.get("official")
            ]

            if not reference_candidates:
                st.success(
                    "沒有被排除的參考盤。"
                )

            for candidate in reference_candidates:
                st.markdown(
                    f"**{candidate.get('id', '—')}｜"
                    f"{candidate.get('label', '—')}**"
                )

                reasons = (
                    candidate.get(
                        "official_exclusion_reasons",
                        [],
                    )
                    + candidate.get(
                        "exclusion_reasons",
                        [],
                    )
                )

                if reasons:
                    st.write(
                        "排除原因："
                        + "；".join(
                            translate_reason(reason)
                            for reason in reasons
                        )
                    )

                conflicts = candidate.get(
                    "conflicts_with",
                    [],
                )

                if conflicts:
                    st.json(conflicts)

                st.divider()

    # --------------------------------------------------------
    # Robustness
    # --------------------------------------------------------

    with result_tabs[2]:
        st.subheader("穩健性分析")

        if not candidates:
            st.info("沒有候選盤可分析。")

        selected_candidate_label = st.selectbox(
            "選擇候選盤",
            options=[
                (
                    f"{candidate.get('id', '—')}｜"
                    f"{candidate.get('label', '—')}"
                )
                for candidate in candidates
            ],
            key="ultra_robustness_candidate",
        ) if candidates else None

        if selected_candidate_label:
            selected_index = [
                (
                    f"{candidate.get('id', '—')}｜"
                    f"{candidate.get('label', '—')}"
                )
                for candidate in candidates
            ].index(selected_candidate_label)

            selected_candidate = candidates[
                selected_index
            ]

            family_audit = selected_candidate.get(
                "family_out_audit",
                {},
            )

            family_status = family_audit.get(
                "status",
                "NOT_TESTABLE",
            )

            first, second, third, fourth = st.columns(4)

            first.metric(
                "整族移除狀態",
                status_chinese(
                    family_status
                ),
            )

            family_hit = (
                family_audit
                .get("probability", {})
                .get("hit", {})
            )

            second.metric(
                "整族移除最低命中率",
                format_probability(
                    family_hit.get("minimum")
                ),
            )

            third.metric(
                "整族移除中位命中率",
                format_probability(
                    family_hit.get("median")
                ),
            )

            fourth.metric(
                "整族移除最高命中率",
                format_probability(
                    family_hit.get("maximum")
                ),
            )

            st.markdown("### 結構壓力測試")

            stress_status = (
                selected_candidate
                .get("stress_audit", {})
                .get("status")
            )

            if stress_status in {
                "DISABLED",
                "NOT_TESTABLE",
            }:
                st.info(
                    "壓力測試："
                    + status_chinese(
                        stress_status
                    )
                )
            else:
                st.dataframe(
                    stress_dataframe(
                        selected_candidate
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

    # --------------------------------------------------------
    # Recommendation set
    # --------------------------------------------------------

    with result_tabs[3]:
        st.subheader("推薦組合分析")

        recommendation_set = result.get(
            "recommendation_set",
            {},
        )

        first, second, third = st.columns(3)

        first.metric(
            "全部命中最低概率",
            format_probability(
                recommendation_set
                .get(
                    "all_hit_probability",
                    {},
                )
                .get("minimum")
            ),
        )

        second.metric(
            "最少一項命中最低概率",
            format_probability(
                recommendation_set
                .get(
                    "at_least_one_hit_probability",
                    {},
                )
                .get("minimum")
            ),
        )

        third.metric(
            "全部不命中最高概率",
            format_probability(
                recommendation_set
                .get(
                    "all_miss_probability",
                    {},
                )
                .get("maximum")
            ),
        )

        set_status = recommendation_set.get(
            "status",
            "NOT_AVAILABLE",
        )

        st.info(
            "組合分析狀態："
            + status_chinese(set_status)
        )

        if recommendation_set.get("reason"):
            st.write(
                recommendation_set["reason"]
            )

        pair_records = recommendation_set.get(
            "pair_compatibility",
            [],
        )

        if pair_records:
            pair_rows = []

            for pair in pair_records:
                joint_hit = pair.get(
                    "joint_hit_probability",
                    {},
                )

                pair_rows.append(
                    {
                        "第一項": pair.get(
                            "first_label"
                        ),
                        "第二項": pair.get(
                            "second_label"
                        ),
                        "可同時命中": (
                            "是"
                            if pair.get(
                                "can_both_hit"
                            )
                            else "否"
                        ),
                        "最低聯合命中率": (
                            format_probability(
                                joint_hit.get(
                                    "minimum"
                                )
                            )
                        ),
                        "中位聯合命中率": (
                            format_probability(
                                joint_hit.get(
                                    "median"
                                )
                            )
                        ),
                    }
                )

            st.dataframe(
                pd.DataFrame(pair_rows),
                use_container_width=True,
                hide_index=True,
            )

    # --------------------------------------------------------
    # Correct scores
    # --------------------------------------------------------

    with result_tabs[4]:
        st.subheader("🎯 高風險波膽參考")

        correct_scores = result.get(
            "correct_scores",
            {},
        )

        st.warning(
            correct_scores.get(
                "warning",
                "波膽屬高風險及低命中率市場。",
            )
        )

        score_records = correct_scores.get(
            "recommendations",
            [],
        )

        if score_records:
            score_columns = st.columns(
                len(score_records)
            )

            for column, score in zip(
                score_columns,
                score_records,
            ):
                probability = score.get(
                    "probability",
                    {},
                )

                with column:
                    st.markdown(
                        f"""
                        <div class="score-card">
                            <div class="score-value">
                                {html_escape(score.get("score", "—"))}
                            </div>
                            <div class="score-probability">
                                保守概率
                                {format_probability(
                                    probability.get("minimum"),
                                    2
                                )}
                            </div>
                            <div style="
                                color: rgba(255,255,255,0.52);
                                margin-top: 0.4rem;
                                font-size: 0.82rem;
                            ">
                                中位
                                {format_probability(
                                    probability.get("median"),
                                    2
                                )}
                                · 公平賠率
                                {format_odds(
                                    score.get("central_fair_odds"),
                                    2
                                )}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            combined = correct_scores.get(
                "combined_probability",
                {},
            )

            st.info(
                "所列波膽合計保守概率："
                + format_probability(
                    combined.get("minimum"),
                    2,
                )
                + " ｜ 中位概率："
                + format_probability(
                    combined.get("median"),
                    2,
                )
            )
        else:
            st.info("沒有波膽參考。")

    # --------------------------------------------------------
    # Model diagnostics
    # --------------------------------------------------------

    with result_tabs[5]:
        st.subheader("模型診斷")

        model = result.get(
            "model",
            {},
        )

        periods = model.get(
            "periods",
            {},
        )

        if periods:
            for period, section in periods.items():
                period_name = (
                    "全場 FT"
                    if period == "FT"
                    else "半場 HT"
                )

                st.markdown(
                    f"### {period_name}"
                )

                first, second, third, fourth = (
                    st.columns(4)
                )

                first.metric(
                    "每隊最高入球",
                    section.get(
                        "max_goals_per_team",
                        "—",
                    ),
                )

                second.metric(
                    "狀態數",
                    section.get(
                        "state_count",
                        "—",
                    ),
                )

                third.metric(
                    "完整情境數",
                    section.get(
                        "full_scenario_count",
                        "—",
                    ),
                )

                fourth.metric(
                    "網格完整",
                    (
                        "是"
                        if section.get(
                            "grid_complete"
                        )
                        else "否"
                    ),
                )

                full_scenarios = section.get(
                    "full_scenarios",
                    [],
                )

                if full_scenarios:
                    scenario_rows = []

                    for scenario in full_scenarios:
                        scenario_rows.append(
                            {
                                "情境": scenario.get(
                                    "id"
                                ),
                                "來源": scenario.get(
                                    "source_title"
                                ),
                                "去水方法": scenario.get(
                                    "devig_method"
                                ),
                                "品質": status_chinese(
                                    scenario.get(
                                        "quality_status"
                                    )
                                ),
                                "主隊 λ": scenario.get(
                                    "lambda_home"
                                ),
                                "客隊 λ": scenario.get(
                                    "lambda_away"
                                ),
                                "ρ": scenario.get(
                                    "rho"
                                ),
                                "最低鬆弛": scenario.get(
                                    "minimum_slack"
                                ),
                                "最大有效殘差": scenario.get(
                                    "maximum_effective_residual"
                                ),
                                "邊界概率": scenario.get(
                                    "boundary_mass"
                                ),
                                "投影方法": scenario.get(
                                    "projection_method"
                                ),
                            }
                        )

                    st.dataframe(
                        pd.DataFrame(
                            scenario_rows
                        ),
                        use_container_width=True,
                        hide_index=True,
                    )

                errors = section.get(
                    "full_scenario_errors",
                    [],
                )

                if errors:
                    st.warning(
                        f"{period_name} 有 "
                        f"{len(errors)} 個情境失敗。"
                    )
                    st.json(errors)

                st.divider()
        else:
            first, second = st.columns(2)

            first.metric(
                "狀態數",
                model.get(
                    "state_count",
                    "—",
                ),
            )

            second.metric(
                "完整情境數",
                model.get(
                    "full_scenario_count",
                    "—",
                ),
            )

        with st.expander(
            "半場－全場一致性詳情",
            expanded=False,
        ):
            st.json(
                result.get(
                    "ht_ft_coherence",
                    {},
                )
            )

        with st.expander(
            "方法說明",
            expanded=False,
        ):
            st.json(
                result.get(
                    "methodology",
                    {},
                )
            )

    # --------------------------------------------------------
    # Full JSON
    # --------------------------------------------------------

    with result_tabs[6]:
        st.subheader("完整引擎輸出")

        result_json = json_text(result)
        input_json = json_text(
            st.session_state.ultra_input
            or {}
        )

        first, second = st.columns(2)

        first.download_button(
            "⬇️ 下載完整分析結果",
            data=result_json,
            file_name=download_name(
                "aegis_ultra_result"
            ),
            mime="application/json",
            use_container_width=True,
        )

        second.download_button(
            "⬇️ 下載完整分析輸入",
            data=input_json,
            file_name=download_name(
                "aegis_ultra_input"
            ),
            mime="application/json",
            use_container_width=True,
        )

        st.json(result)

else:
    st.info(
        "選擇輸入模式，貼上整批賠率，然後開始分析。"
    )


# ============================================================
# 19. Footer
# ============================================================

st.divider()

st.caption(
    f"{ENGINE_NAME} · Engine V{ENGINE_VERSION} · "
    "AEGIS ULTRA 只提供市場重建、概率分析及風險參考，"
    "不保證任何投注結果。"
)

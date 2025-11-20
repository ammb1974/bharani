# mcal.py
# Version: translated from JavaScript (20170826) to Python
# Myanmar Calendrical Calculations - core functions
# License: same as original (Creative Commons Attribution 4.0)

from datetime import datetime, timedelta
import math
from typing import List, Tuple, Dict, Any, Optional

# ---------- Numeral conversion ----------
def myanmar_numbers(s: str, to_language: str = "en"):
    """
    Convert numeric strings between Myanmar/Shan and Western numerals.
    If input is a date string, attempts to parse rearranged formats and returns datetime/date accordingly.
    Mirrors logic from original JS myNumbers function but returns either int, datetime, or string.
    """
    s = str(s)
    to_language = (to_language or "en").lower()

    numbers = {
        "๐": 0,  # Thai zero
        "ဝ": 0,  # Myanmar letter "wa" sometimes used as zero
        "၀": 0,
        "၁": 1,
        "၂": 2,
        "၃": 3,
        "၄": 4,
        "၅": 5,
        "၆": 6,
        "၇": 7,
        "၈": 8,
        "၉": 9,
        # Shan numerals (used in original code)
        "႐": 0,
        "႑": 1,
        "႒": 2,
        "႓": 3,
        "႔": 4,
        "႕": 5,
        "႖": 6,
        "႗": 7,
        "႘": 8,
        "႙": 9
    }

    keys = list(numbers.keys())

    def replace_numbers(txt: str):
        txt = str(txt)
        if to_language == "my":
            # Replace western digits with Myanmar digits
            for n in range(2, 12):  # indices 2..11 map to Myanmar digits in keys
                digit = str(numbers[keys[n]])
                txt = txt.replace(digit, keys[n])
            return txt
        elif to_language == "shan":
            # First convert any Myanmar numbers to international then map to Shan
            txt = myanmar_numbers(txt, "en")
            txt = str(txt)
            for n in range(12, len(keys)):
                digit = str(numbers[keys[n]])
                txt = txt.replace(digit, keys[n])
            return txt
        else:
            # convert Myanmar/Shan digits to western digits
            # special handling for Myanmar character "၀" placed around digits in original code
            # replicate behaviour: run through keys, replace with their numeric char
            out = txt
            # special-case handling similar to JS: handle patterns where '၀' mixes with Myanmar digits
            # but simpler: globally replace mapped characters
            for k in keys:
                out = out.replace(k, str(numbers[k]))
            # handle Myanmar 'ဝ' adjacency patterns that were specially normalized in original JS
            # convert occurrences of '0' as leading/trailing fill if any leftover
            return out

    def get_date_divider(txt: str):
        dividers = [".", "/", "-"]
        for d in dividers:
            parts = txt.split(d)
            if len(parts) == 3:
                try:
                    day = int(parts[0])
                    month = int(parts[1])
                    year = int(parts[2])
                    if 0 < day < 32 and 0 < month < 13 and year < 4000:
                        return d
                except Exception:
                    continue
        return None

    numerals = replace_numbers(s)

    # if numerals is numeric
    try:
        val = int(numerals)
        return val
    except Exception:
        pass

    # try date parsing behavior similar to JS function
    if to_language in ("my", "shan") and not numerals.isdigit():
        # try parsing with datetime
        try:
            d = datetime.fromisoformat(s)
            return replace_numbers(f"{d.day}.{d.month}.{d.year}")
        except Exception:
            return numerals

    date_div = get_date_divider(numerals)
    if date_div:
        parts = numerals.split(date_div)
        # JS rearranged [split[1], split[0], split[2]] to attempt month/day swap
        rearranged = f"{parts[1]}{date_div}{parts[0]}{date_div}{parts[2]}"
        try:
            d = datetime.strptime(rearranged, f"%m{date_div}%d{date_div}%Y")
            return d
        except Exception:
            # fallback to trying original order
            try:
                d = datetime.strptime(numerals, f"%d{date_div}%m{date_div}%Y")
                return d
            except Exception:
                return numerals
    # fallback
    return numerals

# ---------- Constants & data ----------
monthsEN = ['', 'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']
weekDay = ["စနေနေ့", "တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ကြာသာပတေး", "သောကြာ"]
mpDefinations = ["လဆန်း", "လပြည့်", "လပြည့်ကျော်", "လကွယ်"]
months = ["LeapWaso", "Tagu", "Kason", "Nayon", "Waso", "Wagaung",
          "Tawthalin", "Thadingyut", "Tazaungmon", "Nadaw", "Pyatho", "Tabodwe", "Tabaung"]
monthsMM = ["ပဝါဆို", "တန်ခူး", "ကဆုန်", "နယုန်", "ဝါဆို", "ဝါခေါင်",
            "တော်သလင်း", "သီတင်းကျွတ်", "တန်ဆောင်မုန်း", "နတ်တော်", "ပြာသို", "တပို့တွဲ", "တပေါင်း"]

# Era definitions (translated from JS array g_eras)
g_eras = [
    {
        "eid": 1.1,
        "begin": -999,
        "end": 797,
        "WO": -1.1,
        "NM": -1,
        "fme": [[205, 1], [246, 1], [471, 1], [572, -1], [651, 1], [653, 2], [656, 1], [672, 1],
                [729, 1], [767, -1]],
        "wte": []
    },
    {
        "eid": 1.2,
        "begin": 798,
        "end": 1099,
        "WO": -1.1,
        "NM": -1,
        "fme": [[813, -1], [849, -1], [851, -1], [854, -1], [927, -1], [933, -1], [936, -1],
                [938, -1], [949, -1], [952, -1], [963, -1], [968, -1], [1039, -1]],
        "wte": []
    },
    {
        "eid": 1.3,
        "begin": 1100,
        "end": 1216,
        "WO": -0.85,
        "NM": -1,
        "fme": [[1120, 1], [1126, -1], [1150, 1], [1172, -1], [1207, 1]],
        "wte": [[1201, 1], [1202, 0]]
    },
    {
        "eid": 2,
        "begin": 1217,
        "end": 1311,
        "WO": -1,
        "NM": 4,
        "fme": [[1234, 1], [1261, -1]],
        "wte": [[1263, 1], [1264, 0]]
    },
    {
        "eid": 3,
        "begin": 1312,
        "end": 9999,
        "WO": -0.5,
        "NM": 8,
        "fme": [[1377, 1]],
        "wte": [[1344, 1], [1345, 0]]
    }
]

# ---------- Helper: binary search for 2D arrays ----------
def b_search(k: int, A: List[List[int]]) -> int:
    """Binary search first-column in 2D array. Returns index or -1."""
    l = 0
    u = len(A) - 1
    while u >= l:
        i = (l + u) // 2
        if A[i][0] > k:
            u = i - 1
        elif A[i][0] < k:
            l = i + 1
        else:
            return i
    return -1

# ---------- Watat (intercalary) check ----------
def chk_watat(my: int) -> Dict[str, int]:
    # find era for year
    era = None
    for i in range(len(g_eras) - 1, -1, -1):
        if my >= g_eras[i]['begin']:
            era = g_eras[i]
            break
    if era is None:
        era = g_eras[0]

    NM = era['NM']
    WO = era['WO']
    SY = 1577917828 / 4320000  # solar year (365.2587565)
    LM = 1577917828 / 53433336  # lunar month (29.53058795)
    MO = 1954168.050623  # beginning of 0 ME

    TA = (SY / 12 - LM) * (12 - (NM if NM is not None else 0))
    ed = (SY * (my + 3739)) % LM
    if ed < TA:
        ed += LM
    fm = round(SY * my + MO - ed + 4.5 * LM + WO)
    TW = 0
    watat = 0
    if era['eid'] >= 2:
        TW = LM - (SY / 12 - LM) * NM
        if ed >= TW:
            watat = 1
    else:
        # 19-year cycle: remainder 2,5,7,10,13,15,18
        watat = (my * 7 + 2) % 19
        if watat < 0:
            watat += 19
        watat = watat // 12

    i = b_search(my, era['wte'])
    if i >= 0:
        watat = era['wte'][i][1]
    if watat:
        i = b_search(my, era['fme'])
        if i >= 0:
            fm += era['fme'][i][1]
    return {"fm": fm, "watat": watat}

# ---------- Myanmar year check ----------
def chk_my(my: int) -> Dict[str, int]:
    yd = 0
    y1 = None
    nd = 0
    werr = 0
    fm = 0
    y2 = chk_watat(my)
    myt = y2['watat']
    # find earlier watat year up to 3 years back
    while True:
        yd += 1
        y1 = chk_watat(my - yd)
        if y1['watat'] != 0 or yd >= 3:
            break
    if myt:
        nd = (y2['fm'] - y1['fm']) % 354
        myt = nd // 31 + 1
        fm = y2['fm']
        if nd != 30 and nd != 31:
            werr = 1
    else:
        fm = y1['fm'] + 354 * yd
    tg1 = y1['fm'] + 354 * yd - 102
    return {"myt": myt, "tg1": tg1, "fm": fm, "werr": werr}

# ---------- j2m: Julian date (jd) to Myanmar date ----------
def j2m(jd: float) -> Dict[str, Any]:
    SY = 1577917828 / 4320000  # solar year
    MO = 1954168.050623
    jdn = round(jd)
    my = math.floor((jdn - 0.5 - MO) / SY)
    yo = chk_my(my)
    dd = jdn - yo['tg1'] + 1
    b = math.floor(yo['myt'] / 2)
    c = math.floor(1 / (yo['myt'] + 1))  # yields 1 if myt==0, else 0
    myl = 354 + (1 - c) * 30 + b
    mmt = math.floor((dd - 1) / myl)
    dd = dd - mmt * myl
    a = math.floor((dd + 423) / 512)
    mm = math.floor((dd - b * a + c * a * 30 + 29.26) / 29.544)
    e = math.floor((mm + 12) / 16)
    f = math.floor((mm + 11) / 16)
    md = dd - math.floor(29.544 * mm - 29.26) - b * e + c * f * 30
    mm = mm + f * 3 - e * 4
    mml = 30 - mm % 2
    if mm == 3:
        mml += b
    mp = math.floor((md + 1) / 16) + math.floor(md / 16) + math.floor(md / mml)
    fd = md - 15 * math.floor(md / 16)
    wd = (jdn + 2) % 7
    return {
        "my": my,
        "myt": yo['myt'],
        "myl": myl,
        "mm": mm,
        "mmt": mmt,
        "mml": mml,
        "md": md,
        "mp": mp,
        "fd": fd,
        "wd": wd
    }

# ---------- m2j: Myanmar date to Julian day number ----------
def m2j(my: int, mm: int, mmt: int, mp: int, fd: int) -> int:
    yo = chk_my(my)
    b = math.floor(yo['myt'] / 2)
    c = (yo['myt'] == 0)
    mml = 30 - mm % 2
    if mm == 3:
        mml += b
    m1 = mp % 2
    m2 = math.floor(mp / 2)
    md = m1 * (15 + m2 * (mml - 15)) + (1 - m1) * (fd + 15 * m2)
    # adjust month value like the JS implementation
    mm = mm + 4 - math.floor((mm + 15) / 16) * 4 + math.floor((mm + 12) / 16)
    dd = md + math.floor(29.544 * mm - 29.26) - (1 if c else 0) * math.floor((mm + 11) / 16) * 30 + b * math.floor((mm + 12) / 16)
    myl = 354 + (1 - (1 if c else 0)) * 30 + b
    dd = dd + mmt * myl
    return int(dd + yo['tg1'] - 1)

# ---------- j2w: Julian date to Western (Gregorian/Julian) date ----------
def j2w(jd: float, ct: int = 0, SG: int = 2361222) -> Dict[str, int]:
    # ct: 0=english (default), 1=Gregorian, 2=Julian
    j = math.floor(jd + 0.5)
    jf = jd + 0.5 - j
    if ct == 2 or (ct == 0 and (jd < SG)):
        b = j + 1524
        c = math.floor((b - 122.1) / 365.25)
        f = math.floor(365.25 * c)
        e = math.floor((b - f) / 30.6001)
        m = e - 13 if e > 13 else e - 1
        d = b - f - math.floor(30.6001 * e)
        y = c - 4715 if m < 3 else c - 4716
    else:
        j2 = j - 1721119
        y = math.floor((4 * j2 - 1) / 146097)
        j2 = 4 * j2 - 1 - 146097 * y
        d = math.floor(j2 / 4)
        j3 = math.floor((4 * d + 3) / 1461)
        d = 4 * d + 3 - 1461 * j3
        d = math.floor((d + 4) / 4)
        m = math.floor((5 * d - 3) / 153)
        d = 5 * d - 3 - 153 * m
        d = math.floor((d + 5) / 5)
        y = 100 * y + j3
        if m < 10:
            m = m + 3
        else:
            m = m - 9
            y = y + 1
    jf *= 24
    h = math.floor(jf)
    jf = (jf - h) * 60
    n = math.floor(jf)
    s = (jf - n) * 60
    return {"y": int(y), "m": int(m), "d": int(d), "h": int(h), "n": int(n), "s": float(s)}

# ---------- w2j: Western date to Julian day number ----------
def w2j(y: int, m: int, d: int, ct: int = 0, SG: int = 2361222) -> int:
    # ct: 0=english (default), 1=Gregorian, 2=Julian
    a = math.floor((14 - m) / 12)
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    jd = d + math.floor((153 * m2 + 2) / 5) + 365 * y2 + math.floor(y2 / 4)
    if ct == 1:
        jd = jd - math.floor(y2 / 100) + math.floor(y2 / 400) - 32045
    elif ct == 2:
        jd = jd - 32083
    else:
        jd = jd - math.floor(y2 / 100) + math.floor(y2 / 400) - 32045
        if jd < SG:
            jd = d + math.floor((153 * m2 + 2) / 5) + 365 * y2 + math.floor(y2 / 4) - 32083
            if jd > SG:
                jd = SG
    return int(jd)

# ---------- High-level helpers ----------
def to_myanmar(dt: datetime, lang: str = "mm") -> str:
    """
    Convert a Python datetime to Myanmar date string.
    lang: "mm" returns Burmese month names; otherwise returns English transliteration.
    """
    dy = w2j(dt.year, dt.month, dt.day)
    jsondat = j2m(dy)
    if lang == "mm":
        return f"{jsondat['md']} {monthsMM[jsondat['mm']]} {jsondat['my']}"
    else:
        return f"{jsondat['md']} {months[jsondat['mm']]}, {jsondat['my']}"

def to_gregorian(txt: str) -> datetime:
    """
    Convert a Myanmar date string like "10 Tagu 1370" or Burmese names to a Python datetime (at noon).
    This function mimics the toGregorian JS helper.
    """
    parsed_raw = myanmar_numbers(txt)
    if isinstance(parsed_raw, datetime):
        return parsed_raw
    parsed_str = str(parsed_raw).lower().replace(",", "").split()
    # handle possible US date order confusion (same as JS)
    if len(parsed_str) >= 3 and not parsed_str[0].isdigit() and parsed_str[1].isdigit():
        # swap
        parsed_str[0], parsed_str[1] = parsed_str[1], parsed_str[0]
    pick_month = -1
    for i in range(1, len(months)):
        if len(parsed_str) > 1 and (parsed_str[1] == months[i].lower() or parsed_str[1] == monthsMM[i]):
            pick_month = i
            break
    if pick_month == -1:
        raise ValueError("Month not recognized in input string.")
    myear = int(parsed_str[2])
    md = int(parsed_str[0])
    # mmt=1 (hnaung) mp=0(fd?? set full moon?) fd = day as provided
    # Map to JDN then to Gregorian midday
    jdn = m2j(myear, pick_month, 1, 0, md)
    w = j2w(jdn)
    return datetime(w['y'], w['m'], w['d'], 12, 0, 0)

# ---------- Example usage ----------
if __name__ == "__main__":
    # sample conversions
    dt = datetime(2025, 11, 17)
    print("Gregorian -> Myanmar:", to_myanmar(dt, lang="en"))
    print("Gregorian -> Myanmar (MM):", to_myanmar(dt, lang="mm"))

    # parse a Myanmar date (English month)
    try:
        g = to_gregorian("10 Tagu 1387")
        print("Parsed Gregorian:", g.date())
    except Exception as e:
        print("Could not parse:", e)

    # conversions using numeral function
    print("Myanmar number conversion:", myanmar_numbers("၁၂၃၄", to_language="en"))
    print("Myanmar->my digits:", myanmar_numbers("1234", to_language="my"))

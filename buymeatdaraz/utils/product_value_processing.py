def convert_to_int(s: str) -> int:
    s = s.strip().upper()
    if "K" in s:
        return int(float(s.replace("K", "")) * 1000)
    elif "M" in s:
        return int(float(s.replace("M", "")) * 1000000)
    return int(s)

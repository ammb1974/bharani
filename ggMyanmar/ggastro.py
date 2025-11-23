def moon_phase_fraction(jdn: int) -> float:
    """Returns moon phase fraction [0.0=new, 0.5=full, 1.0=new]"""
    synodic_month = 29.53058867
    new_moon_ref = 2451550.1  # Reference JDN
    days_since_new = jdn - new_moon_ref
    phase = (days_since_new % synodic_month) / synodic_month
    return phase

def get_moon_phase(jdn: int) -> str:
    phase = moon_phase_fraction(jdn)
    if phase < 0.03 or phase > 0.97:
        return "New"
    elif phase < 0.47:
        return "Waxing"
    elif phase < 0.53:
        return "Full"
    else:
        return "Waning"

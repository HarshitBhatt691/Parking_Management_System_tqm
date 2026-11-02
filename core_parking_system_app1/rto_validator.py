import re

# Comprehensive Indian State / Union Territory RTO District Code Registry
VALID_RTO_RANGES = {
    "UK": {"name": "Uttarakhand", "min": 1, "max": 20},
    "DL": {"name": "Delhi", "min": 1, "max": 14},
    "UP": {"name": "Uttar Pradesh", "min": 1, "max": 96},
    "HR": {"name": "Haryana", "min": 1, "max": 99},
    "MH": {"name": "Maharashtra", "min": 1, "max": 50},
    "PB": {"name": "Punjab", "min": 1, "max": 75},
    "KA": {"name": "Karnataka", "min": 1, "max": 71},
    "RJ": {"name": "Rajasthan", "min": 1, "max": 55},
    "CH": {"name": "Chandigarh", "min": 1, "max": 4},
    "HP": {"name": "Himachal Pradesh", "min": 1, "max": 95},
    "MP": {"name": "Madhya Pradesh", "min": 1, "max": 70},
    "GJ": {"name": "Gujarat", "min": 1, "max": 38},
    "TN": {"name": "Tamil Nadu", "min": 1, "max": 99},
    "WB": {"name": "West Bengal", "min": 1, "max": 99},
}

RTO_DISTRICT_NAMES_UK = {
    1: "Almora", 2: "Bageshwar", 3: "Champawat", 4: "Nainital / Haldwani",
    5: "Pithoragarh", 6: "Udham Singh Nagar", 7: "Dehradun", 8: "Haridwar",
    9: "Tehri Garhwal", 10: "Uttarkashi", 11: "Chamoli", 12: "Pauri Garhwal",
    13: "Rudraprayag", 14: "Rishikesh", 15: "Kotdwar", 16: "Vikasnagar",
    17: "Roorkee", 18: "Kashipur", 19: "Ramnagar", 20: "Ranikhet"
}


def validate_and_normalize_plate(raw_plate: str):
    """
    Validates Indian vehicle license plate syntax and verifies official RTO district codes.
    Returns: (is_valid: bool, normalized_plate_or_error_message: str, details_dict: dict)
    
    Example:
      Input: 'uk04ak1234' -> (True, 'UK-04-AK-1234', {...})
      Input: 'UK-87-AK-1234' -> (False, "Invalid RTO Code 'UK-87'...", {...})
    """
    if not raw_plate or not raw_plate.strip():
        return False, "License plate number cannot be empty.", {}

    # Clean characters: uppercase and remove spaces/dashes for regex testing
    clean = re.sub(r'[^A-Za-z0-9]', '', raw_plate.strip()).upper()

    # Standard Indian Plate Regex: 2 Letters (State) + 1-2 Digits (RTO) + 1-3 Letters (Series) + 1-4 Digits (Number)
    pattern = r'^([A-Z]{2})(\d{1,2})([A-Z]{0,3})(\d{1,4})$'
    match = re.match(pattern, clean)

    if not match:
        return (
            False,
            f"Invalid license plate syntax '{raw_plate}'. Expected standard Indian format (e.g., UK-04-AK-1234).",
            {}
        )

    state_code, rto_str, series, number = match.groups()
    rto_num = int(rto_str)

    # 1. State Code Verification
    if state_code not in VALID_RTO_RANGES:
        valid_states = ", ".join(sorted(VALID_RTO_RANGES.keys()))
        return (
            False,
            f"Invalid State Code '{state_code}'. Registered states include: {valid_states}.",
            {"state_code": state_code}
        )

    state_info = VALID_RTO_RANGES[state_code]
    min_rto = state_info["min"]
    max_rto = state_info["max"]

    # 2. State-Specific RTO District Range Verification (Poka-Yoke)
    if rto_num < min_rto or rto_num > max_rto:
        rto_formatted = f"{state_code}-{rto_num:02d}"
        if state_code == "UK":
            return (
                False,
                f"Poka-Yoke Error Prevention: '{rto_formatted}' is an invalid RTO registration. "
                f"Uttarakhand RTO district codes strictly range from UK-01 to UK-20 (UK-87 does not exist).",
                {"state": state_info["name"], "entered_rto": rto_num, "max_valid_rto": max_rto}
            )
        else:
            return (
                False,
                f"Poka-Yoke Error Prevention: '{rto_formatted}' is invalid. "
                f"Valid RTO codes for {state_info['name']} ({state_code}) range from {min_rto:02d} to {max_rto:02d}.",
                {"state": state_info["name"], "entered_rto": rto_num, "max_valid_rto": max_rto}
            )

    # 3. Format Normalized Plate (e.g. UK-04-AK-1234)
    rto_display = f"{rto_num:02d}"
    number_display = f"{int(number):04d}" if len(number) <= 4 else number
    series_display = f"-{series}" if series else ""
    normalized_plate = f"{state_code}-{rto_display}{series_display}-{number_display}"

    district_name = RTO_DISTRICT_NAMES_UK.get(rto_num, "Valid Regional Transport Office") if state_code == "UK" else "Valid Regional Transport Office"

    return True, normalized_plate, {
        "state_code": state_code,
        "state_name": state_info["name"],
        "rto_number": rto_num,
        "district_name": district_name,
        "series": series,
        "vehicle_number": number_display
    }

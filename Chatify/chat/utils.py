def set_contact_number(data):
    get_mboile_number = data.get("mobile_number")
    if len(get_mboile_number) > 10 and get_mboile_number[:2] == "91":
        data["mobile_number"] = "+" + get_mboile_number
    elif get_mboile_number[:3] != "+91":
        data["mobile_number"] = "+91" + get_mboile_number
    return data

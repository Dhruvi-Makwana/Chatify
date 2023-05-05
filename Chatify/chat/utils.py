def set_contact_number(data):
    get_mboile_number = data.get("mobile_number")
    if get_mboile_number[:3] != "+91":
        data["mobile_number"] = "+91" + get_mboile_number
    return data

def find_spn_delta(json_response):
    organization = json_response["features"][0]
    dx = organization["properties"]["boundedBy"][1][0] - organization["properties"]["boundedBy"][0][0]
    dy = organization["properties"]["boundedBy"][1][1] - organization["properties"]["boundedBy"][0][1]
    return [dx, dy]
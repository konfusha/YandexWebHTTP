def find_spn_delta(json_response):
    envelope = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]
    dx = float(envelope["upperCorner"].split()[0]) - float(envelope["lowerCorner"].split()[0])
    dy = float(envelope["upperCorner"].split()[1]) - float(envelope["lowerCorner"].split()[1])
    return [dx, dy]
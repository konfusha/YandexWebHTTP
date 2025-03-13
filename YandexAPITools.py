def find_spn_delta(json_response, *points_responses):
    envelope = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]
    x = [float(envelope["upperCorner"].split()[0]), float(envelope["lowerCorner"].split()[0])]
    y = [float(envelope["upperCorner"].split()[1]), float(envelope["lowerCorner"].split()[1])]
    for point_response in points_responses:
        place = point_response["features"][0]
        x += [place["properties"]["boundedBy"][1][0], place["properties"]["boundedBy"][0][0]]
        y += [place["properties"]["boundedBy"][1][1], place["properties"]["boundedBy"][0][1]]
    return [max(x) - min(x), max(y) - min(y)]

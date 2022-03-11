def toponym_sizes(toponym):
    lower_corner = list(map(float, toponym["boundedBy"]["Envelope"][
        "lowerCorner"].split()))
    upper_corner = list(map(float, toponym["boundedBy"]["Envelope"][
        "upperCorner"].split()))

    delta1 = str(upper_corner[0] - lower_corner[0])
    delta2 = str(upper_corner[1] - lower_corner[1])
    return delta1, delta2

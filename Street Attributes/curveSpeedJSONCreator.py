import json

"""
This script creates a json file with the allowed speed range for curvature values. Curvature Values can go up to
key is the curvature. Value the allowed speed range.

curvature data see https://roadcurvature.com/
Curvature values are a weighted measure of length of curves in the roadway (expressed as meters). Based on my experience looking at the data and riding the roads, I’ve found that the curvature values regularly correlate to how much fun I have riding the road — assuming a good road-surface, low traffic and not too many stop-signs.
curvature: < 300
There might be a few fun corners on these, but these roads are predominantly straight or have long distances between each significant curve.
curvature: 300-1,000
These roads have several significant corners close together. They aren’t likely touring destinations unless you’re stuck with otherwise straight roads in the region, but if you are looking to spice up your commute with a few corners, these might be more fun than the most direct route.
curvature: 1,000-3,000
This range has a lot of fun roads. They’ll usually have a few dozen corners and generally feel more winding than straight.
curvature: 3,000-10,000
For much of the world, this range includes the destinations roads that people may ride for hours in order to visit. These roads will usually have long sections of tight turns often for miles on end. In the northeastern US, the best roads are all in this range.
curvature: 10,000+
will not be implemented in this project
These are truly epic roads with mile upon mile of twists and turns.
"""

def custom_speed_limit():
    """
    This function creates a custom speed limit dict for each curvature value
    maximum curvature is 10000[ce]/100[km/h] = 100[ce / km/h]
    :return:
    """
    speedlimit_to_curvature = {
        50: [0, 28],
        70: [28, 66]
        50: [1500]
        1000 : [1200]
    }
    for i in range(0, 9999):
        curvature_speed_limit[i] =


def save_attr_dict(mydict):
    """
    saves the speedlimit_to_curvature as a json file
    The json file containes the prefered speed range given the curvature
    :return:
    """
    with open('./curve_speed_preference.json', 'w') as f:
        json.dump(mydict, f)

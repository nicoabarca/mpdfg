import re


def get_dimensions_min_and_max(activities, connections):
    min_cost_in_activities = min(activity["cost"] for activity in activities.values())
    max_cost_in_activities = max(activity["cost"] for activity in activities.values())

    min_time_in_activities = min(activity["time"] for activity in activities.values())
    max_time_in_activities = max(activity["time"] for activity in activities.values())

    min_freq_in_activities = min(
        activity["frequency"] for activity in activities.values()
    )
    max_freq_in_activities = max(
        activity["frequency"] for activity in activities.values()
    )

    min_freq_in_connections = min(
        connection["frequency"] for connection in connections.values()
    )
    max_freq_in_connections = max(
        connection["frequency"] for connection in connections.values()
    )

    min_time_in_connections = min(
        connection["time"] for connection in connections.values()
    )
    max_time_in_connections = max(
        connection["time"] for connection in connections.values()
    )

    min_cost, max_cost = min_cost_in_activities, max_cost_in_activities
    min_time, max_time = min(min_time_in_activities, min_time_in_connections), max(
        max_time_in_activities, max_time_in_connections
    )
    min_freq, max_freq = min(min_freq_in_activities, min_freq_in_connections), max(
        max_freq_in_activities, max_freq_in_connections
    )

    return {
        "frequency": (min_freq, max_freq),
        "time": (min_time, max_time),
        "cost": (min_cost, max_cost),
    }


def hsl_color(val, dimension, dimension_scale):
    hue = 0
    saturation = 0
    lightness_scale = (75, 35)
    if dimension == "frequency":  # blue
        hue = 225
        saturation = 100
    elif dimension == "time":  # red
        hue = 0
        saturation = 100
    elif dimension == "cost":  # green
        hue = 120
        saturation = 60

    lightness = interpolated_value(val, dimension_scale, lightness_scale)

    return f"hsl({hue},{saturation}%,{lightness}%)"


def link_width(val, dimension_scale):
    width_scale = (0.1, 8)
    link_width = interpolated_value(val, dimension_scale, width_scale)
    return link_width


def text_color(background_color):
    background_lightness = (
        re.search(r"hsl\(\d+,\d+%,(\d+\.?\d*%?)\)", background_color)
        .group(1)
        .replace("%", "")
    )

    blue_threshold = 55
    red_threshold = 0
    green_threshold = 0
    if float(background_lightness) > blue_threshold:
        return "black"
    else:
        return "white"


def format_time(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours} hr, {minutes} min, {remaining_seconds} seg"
    elif minutes > 0:
        return f"{minutes} min, {remaining_seconds} seg"
    else:
        return f"{remaining_seconds} seg"


def lightness_threshold_based_on_color(color):
    pass


def interpolated_value(value, from_scale, to_scale):
    value = max(min(value, from_scale[1]), from_scale[0])
    normalized_value = (value - from_scale[0]) / (from_scale[1] - from_scale[0])
    interpolated_value = to_scale[0] + normalized_value * (to_scale[1] - to_scale[0])
    return interpolated_value
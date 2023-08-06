import requests

colors_to_hex = {
    "bright_red": "#FF0000",
    "bright_blue": "#0000FF",
    "bright_green": "#00FF00"
}

hex_to_colors = {
    "#FF0000": "bright_red",
    "#0000FF": "bright_blue",
    "#00FF00": "bright_green"
}

def color_to_hex(color):
    try:
        if colors_to_hex.get(color) is None:
            return None
        else:
            return colors_to_hex[color]
    except:
        print("Returning hex from color failed!")

def hex_to_color(hex):
    try:
        if hex.startswith('#'):
            hex = hex[1:]

        request_url = f'https://www.thecolorapi.com/id?hex={hex}'

        r = requests.get(request_url)

        data = r.json()

        return data['name']['value']

    except:
        return 'There was an error getting the color from the hex! Please make sure you have entered a legitimate value!'

from shapely.geometry import Polygon

LOCATION_CONF = {
    'loc_1': {
        'host': '103.167.31.202:554/H.264',
        'username': 'admin',
        'password': 'KGMJLP',
        'area': 'loc_1',
        'region': [
            {
                "name": "Counting Region",
                "polygon": Polygon([(440, 91), (510, 89), (465, 358), (217, 357)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            }
        ]
    }
}
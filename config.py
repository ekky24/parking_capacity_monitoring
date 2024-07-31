from shapely.geometry import Polygon

LOCATION_CONF = {
    'sol': {
        'host': '182.0.23.170:554/ch1/main',
        'username': 'admin',
        'password': 'FNZLLZ',
        'area': 'sol',
        'max_capacity': [15, 15, 15],
        'region': [
            {
                "name": "sol_1",
                "polygon": Polygon([(12, 381), (3, 471), (124, 508), (165, 403)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
            {
                "name": "sol_2",
                "polygon": Polygon([(439, 222), (384, 349), (552, 347), (540, 212)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
            {
                "name": "sol_3",
                "polygon": Polygon([(858, 218), (759, 241), (1258, 501), (1266, 367)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    }
}
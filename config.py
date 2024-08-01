from shapely.geometry import Polygon

LOCATION_CONF = {
    'tsu': {
        'host': '182.0.22.141:554/ch2/main',
        'username': 'admin',
        'password': 'CZADKZ',
        'area': 'tsu',
        'max_capacity': [9],
        'region': [
            {
                "name": "tsu_1",
                "polygon": Polygon([(983, 645), (1271, 363), (432, 27), (172, 125)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
    'mcd': {
        'host': '182.0.21.152:554/ch1/main',
        'username': 'admin',
        'password': 'IMGTDW',
        'area': 'mcd',
        'max_capacity': [10,4],
        'region': [
            {
                "name": "mcd_1",
                "polygon": Polygon([(716, 281), (621, 221), (69, 314), (131, 456)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
            {
                "name": "mcd_2",
                "polygon": Polygon([(957, 352), (970, 300), (870, 276), (774, 341)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
    'spklu': {
        'host': '182.0.20.72:554/ch2/main',
        'username': 'admin',
        'password': 'WCMWNA',
        'area': 'spklu',
        'max_capacity': [9],
        'region': [
            {
                "name": "spklu_1",
                "polygon": Polygon([(82, 486), (944, 345), (812, 194), (28, 265)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
    'cig': {
        'host': '182.0.23.170:554/ch1/main',
        'username': 'admin',
        'password': 'FNZLLZ',
        'area': 'cig',
        'max_capacity': [15],
        'region': [
            {
                "name": "cig_1",
                "polygon": Polygon([(1242, 441), (670, 368), (429, 329), (270, 291), (1207,313),
                                    (167, 290), (237, 235), (393, 230), (790, 258)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
    'sol': {
        'host': '182.0.20.72:554/ch1/main',
        'username': 'admin',
        'password': 'WCMWNA',
        'area': 'sol',
        'max_capacity': [8],
        'region': [
            {
                "name": "sol_1",
                "polygon": Polygon([(730, 712), (833, 251), (732, 242), (336, 590), (493, 714)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
    'stb': {
        'host': '182.0.21.189:554/ch2/main',
        'username': 'admin',
        'password': 'WGNVQB',
        'area': 'stb',
        'max_capacity': [10,3],
        'region': [
            {
                "name": "stb_1",
                "polygon": Polygon([(1168, 688), (728, 415), (496, 230), (680, 212),
                                    (1268, 434), (1264, 651)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
            {
                "name": "stb_2",
                "polygon": Polygon([(305, 242), (109, 216), (8, 364), (300, 416)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
    'toilet': {
        'host': '182.0.23.101:554/ch2/main',
        'username': 'admin',
        'password': 'XNJELA',
        'area': 'toilet',
        'max_capacity': [6,7],
        'region': [
            {
                "name": "toilet_1",
                "polygon": Polygon([(1264, 410), (934, 455), (717, 210), (878, 170), (1013, 213)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
            {
                "name": "toilet_2",
                "polygon": Polygon([(432, 489), (438, 272), (382, 181), (219, 174), (28, 501)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
}
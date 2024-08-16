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
                "polygon": Polygon([(1120, 687), (1270, 574), (1269, 363), (549, 75), (348, 144)]),  # Polygon points
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
                "polygon": Polygon([(84, 314), (145, 436), (716, 275), (581, 237)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
            {
                "name": "mcd_2",
                "polygon": Polygon([(775, 342), (956, 352), (967, 292), (874, 273)]),  # Polygon points
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
        'max_capacity': [4],
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
    'cig_1': {
        'host': '182.0.23.170:554/ch1/main',
        'username': 'admin',
        'password': 'FNZLLZ',
        'area': 'cig_1',
        'max_capacity': [8],
        'region': [
            {
                "name": "cig_1",
                "polygon": Polygon([(422, 331), (419, 302), (561, 247), 
                                    (1168, 344), (1212, 465)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
    'cig_2': {
        'host': '182.0.23.170:554/ch2/main',
        'username': 'admin',
        'password': 'FNZLLZ',
        'area': 'cig_2',
        'max_capacity': [7],
        'region': [
            {
                "name": "cig_2",
                "polygon": Polygon([(564, 460), (844, 323), (304, 241), 
                                    (77, 332)]),  # Polygon points
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
                "polygon": Polygon([(490, 240), (467, 261), (638, 425), (1052, 706), (1275, 648),
                                    (1275, 463), (669, 222)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
            {
                "name": "stb_2",
                "polygon": Polygon([(3, 401), (318, 451), (310, 263), (90, 254)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
    'masjid': {
        'host': '182.0.23.101:554/ch2/main',
        'username': 'admin',
        'password': 'XNJELA',
        'area': 'masjid',
        'max_capacity': [6,7],
        'region': [
            {
                "name": "masjid_1",
                "polygon": Polygon([(218, 133), (21, 439), (449, 445), (398, 117)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
            {
                "name": "masjid_2",
                "polygon": Polygon([(664, 157), (1011, 410), (1260, 365), (825, 111)]),  # Polygon points
                "counts": 0,
                "draggin": False,
                "region_color": (37, 255, 255), # BGR value
                "text_color": (0, 0, 0) # Region text color
            },
        ]
    },
}

FILE_SIZE_THRESHOLD = 500
FRAME_RATE = 12
TIMEZONE = 'Asia/Jakarta'
class Config:

    """
    Constants for cell states in a 2D occupancy grid.
    """
    __ALL_CONFIGS = {
        "MAX_WIDHT_PIXEL" : 100,
        "MAX_HEIGHT_PIXEL" : 100,
        "FREE" : 255,
        "OBSTACLE" : 0,
        "VISITED" : 160,
        "START" : 200,
        "GOAL" : 50,
    }

    @classmethod
    def get(cls, key):
        return cls.__ALL_CONFIGS[key]


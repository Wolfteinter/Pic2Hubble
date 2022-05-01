class Node:
    def __init__(self, r_pk=0, g_pk=0, b_pk=0, range_dim=0, size=0):
        # Images related 
        self.images = []
        # Identification 
        self.pk = r_pk * pow(size, 2) +  g_pk*pow(size, 1) +  b_pk*pow(size, 0)
        # Ranges
        self.r_range = (r_pk * range_dim, (r_pk * range_dim) + range_dim)
        self.g_range = (g_pk * range_dim, (g_pk * range_dim) + range_dim)
        self.b_range = (b_pk * range_dim, (b_pk * range_dim) + range_dim)
        # Childrens
        self.r = None
        self.g = None
        self.b = None

    def __repr__(self):
        return (
            str(self.pk) + " , " + str(self.r_range) + " , " 
            + str(self.g_range) + " , " + str(self.b_range)
        )

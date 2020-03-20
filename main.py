import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

# TODO: Use Argparse to get this from the commandline
data = pd.read_csv("data.csv")

# determin start and end time
time_start = data["t"].min()
time_end = data["t"].max()

# create dataframe for book keeping of contacts
contacts = pd.DataFrame(columns=["id_a", "id_b", "t", "x", "y"])

# iterate over time
for t in range(time_start, time_end+1):
    # filter for time and find pairwise distances
    current_data = data[data["t"]==t]
    pair_distances = pdist(current_data[["x","y"]], "euclidean")
    
    # use square form of pairwise distances and add diagonal to it, to avoid self matches
    con = np.argwhere(squareform(pair_distances)+np.eye(squareform(pair_distances).shape[0]) == 0)
    # derive contact and add it to contacts
    contact = pd.DataFrame({"id_a": con[0][0],
                            "id_b": con[0][1],
                            "t": t,
                            "x": current_data[current_data["id"] == con[0][0]]["x"].item(),
                            "y": current_data[current_data["id"] == con[0][0]]["y"].item()}, index=[0])
    contacts = pd.concat([contacts, contact])

# sort table of ids by number of contacts
print(contacts)



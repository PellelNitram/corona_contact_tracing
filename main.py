import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from tqdm import tqdm

# TODO: Use Argparse to get this from the commandline
data = pd.read_csv("simulation.csv")

# determin start and end time
time_start = data["t"].min()
time_end = data["t"].max()
number_of_agents = len(set(data["agent"]))

# create dataframe for book keeping of contacts
contacts = pd.DataFrame(columns=["agent_a", "agent_b", "t", "x", "y", "agent_a_state", "agent_b_state"])

# iterate over time
for t in tqdm(range(time_start, time_end+1)):
    # filter for time and find pairwise distances
    current_data = data[data["t"]==t]
    pair_distances = pdist(current_data[["x","y"]], "euclidean")
    
    # use square form of pairwise distances and add diagonal to it, to avoid self matches
    con = np.argwhere(squareform(pair_distances) + np.eye(squareform(pair_distances).shape[0]) == 0)[0]
    # derive contact and add it to contacts
    current_agent_a = current_data[current_data["agent"] == con[0]]
    current_agent_b = current_data[current_data["agent"] == con[1]]
    contact = pd.DataFrame({"agent_a": current_agent_a["agent"].item(),
                            "agent_b": current_agent_b["agent"].item(),
                            "t": t,
                            "x": current_agent_a["x"].item(),
                            "y": current_agent_a["y"].item(),
                            "agent_a_state": current_agent_a["state"].item(),
                            "agent_b_state": current_agent_b["state"].item(),},
                            index=[0])
    contacts = pd.concat([contacts, contact])

# sort/create table of ids by number of contacts with infected people
# if one agent, a or b, is state==2, increase count for the other

sick_agent_a = contacts[(contacts["agent_a_state"]==2) & (contacts["agent_b_state"] != 3)]
sick_agent_b = contacts[(contacts["agent_b_state"]==2) & (contacts["agent_a_state"] != 3)]

# count all contacts towards each agent
contact_counts = [0] * number_of_agents
all_contacts_of_sicks = list(sick_agent_b["agent_a"]) + list(sick_agent_a["agent_b"])
for ac in all_contacts_of_sicks:
    contact_counts[ac] += 1

# reformat as dataframe
contact_counts = pd.DataFrame(data={"agent": range(number_of_agents), "contact_counts": contact_counts}).sort_values(by="contact_counts", ascending=False)

print(contact_counts)


# contacts of contacts
# TODO: Use contacts to second order contact count


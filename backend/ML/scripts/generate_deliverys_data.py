import numpy as np
import pandas as pd




#this function generates a list of a random deliverys data to be used for training the ML model
def make_random_deliverys(number_deliverys):
    deliverys_list=[]
    for _ in range(number_deliverys):
        random_distance=np.random.uniform(low=0, high=60)
        random_hour=np.random.randint(low=0, high=24)
        random_day=np.random.randint(low=0, high=7)
        #the time every km takes on average without traffic
        base_eta=random_distance * 1.5
        traffic_penalty = 0
        #morning traffic penalty
        if 8<random_hour<11:
                traffic_penalty = 15
            #afternoon traffic penalty
        elif 16<random_hour<19:
                traffic_penalty = 30
        #the random noise to simulate real life variations
        random_noise = np.random.uniform(-5, 5)
        final_eta = base_eta + traffic_penalty + random_noise

        delivery_information = {
            "distance_km": round(random_distance,2),
            #the time of arriving base on the time every km takes on average without traffic
            "maps_eta_minutes": round(base_eta,2),
            #the hour of the delivery
            "hour_of_day": random_hour,
            "day_of_week": random_day,
            "actual_delivery_minutes":round(final_eta,2)
        }
       

        deliverys_list.append(delivery_information)

    return deliverys_list


#create a DataFrame from the generated delivery data
df=pd.DataFrame(make_random_deliverys(5000))
#save the DataFrame to a CSV file
df.to_csv("backend/ML/data/deliverys_data.csv", index=False)


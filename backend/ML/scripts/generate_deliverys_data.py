import numpy as np
import pandas as pd




#this function generates a list of a random deliverys data to be used for training the ML model
def make_random_deliverys(number_deliverys):
    deliverys_list=[]
    for _ in range(number_deliverys):
        random_distance=np.random.uniform(low=1.0, high=60.0)
        random_hour=np.random.randint(low=0, high=24)
        random_day=np.random.randint(low=0, high=7)
        #base time every km takes on average without traffic
        base_rate = np.random.uniform(1.2, 1.8)
        #the time every km takes on average without traffic
        base_eta=random_distance * base_rate
        
        traffic_multiplier = 1.0
        #morning traffic penalty
        if 8<random_hour<11:
                traffic_multiplier = np.random.uniform(1.2, 2.5)
        #afternoon traffic penalty
        elif 16<random_hour<19:
                traffic_multiplier = np.random.uniform(1.4, 2.8)
        else:
                traffic_multiplier = np.random.uniform(0.9, 1.3)
        
        random_noise = np.random.uniform(-5.0, 12.0)
        final_eta = (base_eta * traffic_multiplier) + random_noise
        #ensure that the final eta is not negative and has a minimum of 5 minutes
        final_eta = max(4.0, final_eta)

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


from itertools import product, permutations
import json

def open_json(name):

    # opening JSON file
    f = open(name)
    # read JSON file
    data = json.load(f)
    # close the file
    f.close()
    return data

data = open_json('input.json')
#get cost matrix
cost_matrix = data['matrix']
#get vehicle data
vehicles = data['vehicles']
#get job data
jobs = data['jobs']

#write start and job locations into lists
vehicle_start, delivery_location = [], []
for vehicle in vehicles:
    vehicle_start.append(vehicle['start_index']+1)

for job in jobs:
    delivery_location.append(job['location_index'])

#find an index for a given car
def find_index(whoGoesWhere, carNumber):
    indexes = []
    for i, x in enumerate(whoGoesWhere):
        # i is the index, x is the car
        if x == carNumber:
            indexes.append(i+3)
    return indexes

#find all indexes for all the cars
def find_all_index(carList, numberOfRoutes):
    cartesien_product = []
    car_1_index = []
    car_2_index = []
    car_3_index = []
    #all possible combinations of which car goes where
    cartesien_product = list(product(carList, repeat = numberOfRoutes))

    #fill possible combinations for each car
    for index in cartesien_product:
        car_1_index.append(find_index(index, 1))
        car_2_index.append(find_index(index, 2))
        car_3_index.append(find_index(index, 3))

    return car_1_index, car_2_index, car_3_index

#find indexes for all cars
index1, index2, index3 = find_all_index(vehicle_start, len(delivery_location))


#all routes that cars can go
def car_all_routes(car1, car2, car3):
    car1_all_routes = []
    car2_all_routes = []
    car3_all_routes = []
    #calucate all possible permutations for each car
    for route1, route2, route3 in zip(car1, car2, car3):
        car1_all_routes.append(list(permutations(route1)))
        car2_all_routes.append(list(permutations(route2)))
        car3_all_routes.append(list(permutations(route3)))

    return car1_all_routes, car2_all_routes, car3_all_routes

#find all car routes
car1_routes, car2_routes, car3_routes = car_all_routes(index1, index2, index3)

def one_route_cost(route, car):
    sum = 0
    #if the list is empty
    if not route:
        sum = 0
    else:
        #add the first input as vehicle initial location
        route.insert(0, car-1)
        #rest of the route
        for i in range(len(route)-1):
            sum += cost_matrix[route[i]][route[i+1]]
    return sum

#function that calculates costs for all routes and find the optimal one
def calculate_cost(car1_route, car2_route, car3_route):

    #cost parameters
    temp_total_cost, car1_cost, car2_cost, car3_cost = 0, 0, 0, 0
    total_cost = 20000
    min_cost1, min_cost2, min_cost3 = 0, 0, 0
    car1_list, car2_list, car3_list = [], [], []
    min_route1, min_route2, min_route3 = [], [], []


    #all the routes for 3 vehicles and 7 locations
    for i in range(len(car1_route)):

        #indiviual permutations for car 1
        for k in range(len(car1_route[i])):
            if len(car1_route[i][k]) > 0:
                car1_cost = one_route_cost(list(car1_route[i][k]), 1)
            else:
                car1_cost = 0
            car1_list.append(car1_cost)
        # indiviual permutations for car 2
        for m in range(len(car2_route[i])):
            if len(car2_route[i][m]) > 0:
                car2_cost = one_route_cost(list(car2_route[i][m]), 2)
            else:
                car2_cost = 0
            car2_list.append(car2_cost)
        # indiviual permutations for car 3
        for n in range(len(car3_route[i])):
            if len(car3_route[i][n]) > 0:
                car3_cost = one_route_cost(list(car3_route[i][n]), 3)
            else:
                car3_cost = 0
            car3_list.append(car3_cost)
        #calculate minimum of each car from the same permutation list
        min_cost1 = min(car1_list)
        min_cost2 = min(car2_list)
        min_cost3 = min(car3_list)
        temp_total_cost = min_cost1 + min_cost2 + min_cost3
        #define new low cost and route if possible
        if temp_total_cost < total_cost:
            total_cost = temp_total_cost
            min_route1 = car1_route[i][car1_list.index(min_cost1)]
            min_route2 = car2_route[i][car2_list.index(min_cost2)]
            min_route3 = car3_route[i][car3_list.index(min_cost3)]
            last_cost1, last_cost2, last_cost3 = min_cost1, min_cost2, min_cost3


        #clear the list after each iteration
        car1_list.clear()
        car2_list.clear()
        car3_list.clear()
    return total_cost, min_route1, min_route2, min_route3, last_cost1, last_cost2, last_cost3

total_cost, min_route1, min_route2, min_route3, min_cost1, min_cost2, min_cost3 = calculate_cost(car1_routes, car2_routes, car3_routes)

#these could be returned as arrays from the above function as well, just for clarification purposes
car_routes, car_mins = [], []
car_routes.extend([min_route1, min_route2, min_route3])
car_mins.extend([min_cost1, min_cost2, min_cost3])


print("Total Cost: ", total_cost)
print("Car1 Route: ", min_route1)
print("Car2 Route: ", min_route2)
print("Car3 Route: ", min_route3)
print("Car1 Cost: ", min_cost1)
print("Car2 Cost: ", min_cost2)
print("Car3 Cost: ", min_cost3)

jobs_dict, dump_dict = {}, {}

for i in range(len(vehicle_start)):
    temp_dict = \
    {(i+1):
        {"jobs": car_routes[i],
         "delivery_duration": car_mins[i]
        }
    }
    jobs_dict.update(temp_dict)

output={
    "total_delivery_duration": total_cost,
    "routes": jobs_dict}

with open('output.json', 'w') as f:
    json.dump(output, f, indent = 4)



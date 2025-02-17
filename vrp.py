from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import streamlit as st
import pandas as pd
import geopandas as gpd

def prep_data_pred(origin,vec,dist,x,y):
    pred = {'origin_location':origin, 'vehicle_type':vec, 'distance_in_km':dist,'coor_y':y , 'coor_x':x}
    pred = pd.DataFrame([pred])
    pred = pd.get_dummies(pred, columns=['origin_location', 'vehicle_type'],dummy_na=False)
    existingcol = list(pred.columns)
    column = {'distance_in_km', 'coor_y', 'coor_x', 'origin_location_JAKARTA',
       'origin_location_KARAWANG', 'origin_location_KOTA BANDUNG',
       'origin_location_KOTA SEMARANG', 'origin_location_KOTA SURABAYA',
       'origin_location_KOTA YOGYAKARTA', 'vehicle_type_CDD Long',
       'vehicle_type_Double Engkel Box', 'vehicle_type_Double Engkel Pickup',
       'vehicle_type_Ekonomi', 'vehicle_type_Engkel Box',
       'vehicle_type_Engkel Pickup', 'vehicle_type_Fuso Bak',
       'vehicle_type_Fuso Box', 'vehicle_type_L300 Box', 'vehicle_type_MPV',
       'vehicle_type_Pickup', 'vehicle_type_Small Box',
       'vehicle_type_Tronton Bak', 'vehicle_type_Tronton Box',
       'vehicle_type_Tronton Wing Box', 'vehicle_type_Van'}
    rightcolumn = ['distance_in_km', 'coor_y', 'coor_x', 'origin_location_JAKARTA',
        'origin_location_KARAWANG', 'origin_location_KOTA BANDUNG',
        'origin_location_KOTA SEMARANG', 'origin_location_KOTA SURABAYA',
        'origin_location_KOTA YOGYAKARTA', 'vehicle_type_CDD Long',
        'vehicle_type_Double Engkel Box', 'vehicle_type_Double Engkel Pickup',
        'vehicle_type_Ekonomi', 'vehicle_type_Engkel Box',
        'vehicle_type_Engkel Pickup', 'vehicle_type_Fuso Bak',
        'vehicle_type_Fuso Box', 'vehicle_type_L300 Box', 'vehicle_type_MPV',
        'vehicle_type_Pickup', 'vehicle_type_Small Box',
        'vehicle_type_Tronton Bak', 'vehicle_type_Tronton Box',
        'vehicle_type_Tronton Wing Box', 'vehicle_type_Van']

    for col in column.difference(existingcol):
                pred[col] = False
    pred = pred.reindex(columns=rightcolumn)
    return pred

def create_dist_matrix(data):
    gdf = gpd.GeoDataFrame(
        data,
        geometry=gpd.points_from_xy(data['x'], data['y']),
        crs='EPSG:4326'
    )
    distances = []
    for _, row in gdf.iterrows():
        distances.append(round(gdf['geometry'].distance(row['geometry'])*1000))
    distances_df = pd.DataFrame.from_records(distances).astype(int)
    return distances_df

def create_data_model(df, num_vec):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = create_dist_matrix(df)
    data["num_vehicles"] = num_vec
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    max_route_distance = 0
    returnee = []
    dist = []
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        #plan_output = f"Route for vehicle {vehicle_id}:\n"
        plan_output = ""
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}"
        returnee.append(plan_output)
        plan_output += f"Distance of the route: {route_distance}Km\n"
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
        dist.append(route_distance)
    print(f"Maximum of the route distances: {max_route_distance}Km")
    return returnee, dist

def main(df,num_vec):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(df,num_vec)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        30000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        returnee = print_solution(data, manager, routing, solution)
        return returnee
    else:
        print("No solution found !")




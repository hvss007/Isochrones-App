import tkinter as tk
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from descartes import PolygonPatch
from shapely.geometry import Point, LineString, Polygon
ox.config(log_console=True, use_cache=True)
ox.__version__

network_type = 'drive'
trip_times = [5, 10, 15, 20, 25] #in minutes
travel_speed = 60 #walking speed in km/hour

root=tk.Tk()
city_input=tk.Entry(root,width=50)
city_input.pack()
city_input.insert(0,"Enter your city name")


city_centre_input=tk.Entry(root,width=50)
city_centre_input.pack()
city_centre_input.insert(0,"Enter your isochrone center latitude")

city_centre_input1=tk.Entry(root,width=50)
city_centre_input1.pack()
city_centre_input1.insert(0,"Enter your isochrone center longitude")

trip_times_input=tk.Entry(root,width=50)
trip_times_input.pack()
trip_times_input.insert(0,"Enter comma separated values of travel time bins in minutes")
def submitHandler():
    isochrone_city=city_input.get()
    lat=city_centre_input.get()
    lng=city_centre_input1.get()
   
    trip_times=trip_times_input.get().split(',')
   
    for i in range(0,len(trip_times)):
        trip_times[i]=int(trip_times[i])
   
    G = ox.graph_from_place(isochrone_city, network_type=network_type)
    gdf_nodes = ox.graph_to_gdfs(G, edges=False)
    x, y = gdf_nodes['geometry'].unary_union.centroid.xy
    center_node=ox.get_nearest_node(G,(float(lat),float(lng)))
    
    # G1 = ox.graph_from_place(isochrone_centre, network_type=network_type)
    # gdf_nodes1 = ox.graph_to_gdfs(G1, edges=False)
    # x1, y1 = gdf_nodes['geometry'].unary_union.centroid.xy
    # center_node = ox.get_nearest_node(G1, (y1[0], x1[0]))
    
    G = ox.project_graph(G)
    meters_per_minute = travel_speed * 1000 / 60 #km per hour to m per minute
    for u, v, k, data in G.edges(data=True, keys=True):
        data['time'] = data['length'] / meters_per_minute
    

    # get one color for each isochrone
    

    iso_colors = ox.get_colors(n=len(trip_times), cmap='hsv', start=0.3, return_hex=True)
    

    # color the nodes according to isochrone then plot the street network
    
    
    node_colors = {}
    for trip_time, color in zip(sorted(trip_times, reverse=True), iso_colors):
        subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance='time')
        for node in subgraph.nodes():
            node_colors[node] = color
    nc = [node_colors[node] if node in node_colors else 'none' for node in G.nodes()]
    ns = [20 if node in node_colors else 0 for node in G.nodes()]
    fig, ax = ox.plot_graph(G, fig_height=8, node_color=nc, node_size=ns, node_alpha=0.8, node_zorder=2)





submitButton=tk.Button(root,text="Submit Information",command=submitHandler)
submitButton.pack()

root.mainloop()
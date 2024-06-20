import pandas as pd
import numpy as np
import folium # for creating a map
import fiona # for reading shapefiles
from haversine import haversine # for calculating distance between two points
from sklearn.cluster import KMeans
from branca.colormap import LinearColormap # for creating a color map
from shapely.geometry import Point, shape 
# for checking if a point is within a polygon, `Point` is a class to represent a point, `shape` is a function to create a polygon from a GeoJSON object


def check_coordinates_in_vietnam(shapefile_path, housing_df):
    # List of coordinates to check
    coordinates_list = [(lon, lat) for lon, lat in zip(housing_df['Longitude'], housing_df['Latitude'])]

    # Open the shapefile and get the polygon representing Vietnam's territory
    with fiona.open(shapefile_path) as shp:
        geometries = [shape(feature['geometry']) for feature in shp]
        vietnam_shape = geometries[0]  # Vietnam is the first feature in the shapefile

    # Filter out coordinates within Vietnam's territory
    coordinates_in_vietnam = [coord for coord in coordinates_list if Point(coord).within(vietnam_shape)]

    # Save to Latitude and Longitude columns of housing
    return housing_df[housing_df[['Longitude', 'Latitude']].apply(tuple, axis=1).isin(coordinates_in_vietnam)]

class RealEstateVisualizer:
    def __init__(self, housing_df, num_clusters=5):
        self.housing = housing_df
        self.num_clusters = num_clusters
        self.colormap = LinearColormap(
            ['green', 'blue', 'orange', 'red', 'purple', 'brown', 'black'],
            vmin=self.housing['Price'].min(),
            vmax=self.housing['Price'].max()
        )
        self.cluster_centers = None
        self.cluster_radii = None

    def fit_kmeans(self):
        clustering_features = self.housing[['Latitude', 'Longitude']] # Choose the clustering features
        kmeans = KMeans(n_clusters=self.num_clusters, random_state=0).fit(clustering_features)
        self.cluster_centers = kmeans.cluster_centers_
        self.housing['Cluster'] = kmeans.labels_ # Add the cluster labels to the housing DataFrame
        self.housing['Distance to center'] = self.housing.apply(
            lambda row: haversine(
                (row['Latitude'], row['Longitude']),
                self.cluster_centers[row['Cluster']]
            ),
            axis=1 # Apply the function to each row
        )
        self.calculate_cluster_radii()

    # Calculate cluster center and radius, `cluster_radii` is the distance from the center to the farthest point in the cluster
    def calculate_cluster_radii(self):
        self.cluster_radii = [
            max(
                haversine(center, (point.Latitude, point.Longitude))
                for point in self.housing[self.housing['Cluster'] == idx].itertuples() # `itertuples` is a function to iterate through the DataFrame as tuples
            )
            for idx, center in enumerate(self.cluster_centers)
        ]

    # Draw x at the cluster center and a circle around the points in the cluster
    def add_cluster_visualization(self, gmap):
        for idx, (center, radius) in enumerate(zip(self.cluster_centers, self.cluster_radii)):
            # Draw a circle around the cluster
            folium.Circle(
                location=center,
                radius=radius * 1000, # Convert from km to m
                color='black',
                fill=False, # No fill inside the circle
            ).add_to(gmap)

            # Draw a large X at the cluster center
            folium.Marker(
                location=center,
                icon=folium.DivIcon(html=f'<div style="font-size: 24pt; color: black;">x</div>') # `DivIcon` is a class to create a custom icon with HTML content
            ).add_to(gmap)
    
    # Draw markers for each real estate with color based on price
    def add_markers(self, gmap):
        for i, row in self.housing.iterrows():
            marker_color = self.colormap(row['Price'])
            popup_content = f"Diện tích: {row['Diện tích (m2)']} - Giá: {row['Price']}"
            folium.CircleMarker(
                location=(row['Latitude'], row['Longitude']),
                radius=5,
                color=marker_color,
                fill=False,
                fill_color=marker_color, 
                popup=popup_content # `popup` is the text that appears when you click on the marker
            ).add_to(gmap)

    def create_map(self):
        gmap = folium.Map(location=[21.028511, 105.804817], zoom_start=6)
        self.colormap.add_to(gmap)
        self.add_markers(gmap)
        self.add_cluster_visualization(gmap)
        return gmap

def visualize_clusters(housing_df, num_clusters=5):
    visualizer = RealEstateVisualizer(housing_df, num_clusters) # Create a RealEstateVisualizer object
    visualizer.fit_kmeans() # Fit KMeans model and add cluster labels to the dataframe
    return visualizer.create_map() # Create a folium map
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# for creating a map
import folium 

 # for reading shapefiles
import fiona

from haversine import haversine
from sklearn.cluster import KMeans

# for creating a color map
from branca.colormap import LinearColormap 

# for checking if a point is within a polygon, `Point` is a class to represent a point, `shape` is a function to create a polygon from a GeoJSON object
from shapely.geometry import Point, shape


def check_coordinates_in_vietnam(shapefile_path:str, housing_df:pd.DataFrame) -> pd.DataFrame:
    """
    Check if the coordinates in the housing DataFrame are within Vietnam's territory.

    Parameters:
        shapefile_path (str): The path to the shapefile containing the territory of Vietnam.
        housing_df (pd.DataFrame): The DataFrame containing the housing data.

    Returns:
        pd.DataFrame: The DataFrame containing the housing data with coordinates within Vietnam's territory.
    """
    # List of coordinates to check
    coordinates_list = [
        (longitude, latitude)
        for longitude, latitude
        in zip(housing_df['Longitude'], housing_df['Latitude'])
    ]

    # Open the shapefile and get the polygon representing Vietnam's territory
    with fiona.open(shapefile_path) as shp:
        geometries = [shape(feature['geometry']) for feature in shp]

        # Vietnam shape is the first feature in the shapefile
        vietnam_shape = geometries[0]  

    # Filter out coordinates within Vietnam's territory
    coordinates_in_vietnam = [coordinate
                               for coordinate
                               in coordinates_list
                               if Point(coordinate).within(vietnam_shape)]

    # Indices of coordinates within Vietnam's territory
    indices_in_vietnam = housing_df[['Longitude', 'Latitude']].apply(tuple, axis=1).isin(coordinates_in_vietnam)

    # Return the housing data with coordinates within Vietnam's territory
    return housing_df[indices_in_vietnam]

class RealEstateVisualizer:
    """
    A class to visualize real estate data on a map.

    Attributes:
        housing (pd.DataFrame): The DataFrame containing the real estate data.
        num_clusters (int): The number of clusters for KMeans clustering.
        colormap (LinearColormap): The color map for the real estate prices.
        cluster_centers (np.ndarray): The coordinates of the cluster centers.
        cluster_radius (List[float]): The radius of the clusters.

    Methods:
        fit_kmeans: Fit a KMeans model to the real estate data and add cluster labels to the DataFrame.
        calculate_cluster_radius: Calculate the radius of the clusters.
        add_cluster_visualization: Add cluster visualization to the map.
        add_markers: Add markers for each real estate with color based on price.
        create_map: Create a folium map with real estate data and cluster visualization.
    """
    def __init__(self, housing_df:pd.DataFrame, num_clusters:int=5) -> None:
        """
        Initialize the RealEstateVisualizer object.

        Parameters:
            housing_df (pd.DataFrame): The DataFrame containing the real estate data.
            num_clusters (int): The number of clusters for KMeans clustering, default is 5.

        Returns:
            RealEstateVisualizer: The RealEstateVisualizer object.
        """
        self.housing = housing_df
        self.num_clusters = num_clusters
        self.colormap = LinearColormap(
            ['green', 'blue', 'orange', 'red', 'purple', 'brown', 'black'],
            vmin=self.housing['Price'].min(),
            vmax=self.housing['Price'].max()
        )
        self.cluster_centers = None
        self.cluster_radius = None

    def fit_kmeans(self) -> None:
        """
        Fit a KMeans model to the real estate data and add cluster labels to the DataFrame.
        """
        clustering_features = self.housing[['Latitude', 'Longitude']] # Choose the clustering features
        self.num_clusters = self.elbow_method(clustering_features)
        kmeans = KMeans(n_clusters=self.num_clusters, random_state=0).fit(clustering_features)
        self.cluster_centers = kmeans.cluster_centers_ # Get the cluster centers
        self.housing['Cluster'] = kmeans.labels_ # Add the cluster labels to the housing DataFrame
        self.distance_to_center(self.housing)
        self.calculate_cluster_radius()

    def elbow_method(self, clustering_features:pd.DataFrame) -> np.ndarray:
        """
        Find the optimal number of clusters using the elbow method.

        Parameters:
            clustering_features (pd.DataFrame): The features used for clustering.

        Returns:
            np.ndarray: The coordinates of the cluster centers.
        """
        distortions = []
        K = range(1, 11)
        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=0).fit(clustering_features)
            distortions.append(kmeans.inertia_)
            
        # plt.figure(figsize=(16,8))
        plt.plot(K, distortions, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal k')
        plt.show()

        diff = np.diff(distortions)
        return abs(diff).argmax() + 2
    
    def distance_to_center(self, housing:pd.DataFrame) -> None:
        """
        Calculate the distance of each real estate to the cluster center.

        Parameters:
            housing (pd.DataFrame): The DataFrame containing the real estate data.
        """
        for idx, center in enumerate(self.cluster_centers):
            housing[f'Distance to center {idx}'] = housing.apply(
                lambda row: haversine(center, (row['Latitude'], row['Longitude'])),
                axis=1
            )

    def calculate_cluster_radius(self) -> None:
        """
        Calculate the radius of the clusters, which is the distance from the cluster center to the farthest point in the cluster.
        """
        self.cluster_radius = [
            max(
                haversine(center, (point.Latitude, point.Longitude))
                for point in self.housing[self.housing['Cluster'] == idx].itertuples() # `itertuples` is a function to iterate through the DataFrame as tuples
            )
            for idx, center in enumerate(self.cluster_centers)
        ]

    # Draw x at the cluster center and a circle around the points in the cluster
    def add_cluster_visualization(self, gmap: folium.Map) -> None:
        """
        Add cluster visualization to the map.

        Parameters:
            gmap (folium.Map): The folium map object.
        """
        for _, (center, radius) in enumerate(zip(self.cluster_centers, self.cluster_radius)):
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
                # `DivIcon` is a class to create a custom icon with HTML content
                icon=folium.DivIcon(html=f'<div style="font-size: 24pt; color: black;">x</div>') 
            ).add_to(gmap)
    
    def add_markers(self, gmap: folium.Map) -> None:
        """
        Add markers for each real estate with color based on price.

        Parameters:
            gmap (folium.Map): The folium map object.
        """
        for _, row in self.housing.iterrows():
            marker_color = self.colormap(row['Price'])
            popup_content = f"Diện tích: {row['Diện tích (m2)']} - Giá: {row['Price']}"
            folium.CircleMarker(
                location=(row['Latitude'], row['Longitude']),
                radius=5,
                color=marker_color,
                fill=False,
                fill_color=marker_color,
                # `popup` is the text that appears when you click on the marker
                popup=popup_content 
            ).add_to(gmap)

    def create_map(self) -> folium.Map:
        gmap = folium.Map(location=[21.028511, 105.804817], zoom_start=6)
        self.colormap.add_to(gmap)
        self.add_markers(gmap)
        self.add_cluster_visualization(gmap)
        return gmap

def visualize_clusters(housing_df:pd.DataFrame, num_clusters:int=5) -> folium.Map:
    visualizer = RealEstateVisualizer(housing_df, num_clusters) 
    visualizer.fit_kmeans() # Fit KMeans model and add cluster labels to the dataframe
    return visualizer.create_map() # Create a folium map
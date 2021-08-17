import folium
import gpxpy
import pandas as pd
import os

def process_gpx_to_df(directory, file_name):
    # https://towardsdatascience.com/build-interactive-gps-activity-maps-from-gpx-files-using-folium-cf9eebba1fe7
    gpx = gpxpy.parse(open(os.path.join(directory, file_name))) 
    track = gpx.tracks[0]
    segment = track.segments[0]
    # Load the data into a Pandas dataframe (by way of a list)
    data = []
    segment_length = segment.length_3d()
    for point_idx, point in enumerate(segment.points):
        try:
            data.append([point.longitude, point.latitude,point.elevation, point.time, segment.get_speed(point_idx)])
        except:
            data.append([point.longitude, point.latitude, 0, 0, 0])
    columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
    gpx_df = pd.DataFrame(data, columns=columns)
 
    #2(make points tuple for line)
    points = []
    for track in gpx.tracks:
        for segment in track.segments: 
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
 
    return gpx_df, points

if __name__ == "__main__":
    lat, lon = 50.325625, 16.944352
    zoom_start = 5
    dir_mount = 'gpx_files_mountains'
    dir_run = 'gpx_files_running'
    dir_walk = 'gpx_files_walking'
    m = folium.Map(location=[lat, lon], zoom_start = zoom_start, tiles=None)
    folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(m)

    for file in os.listdir(dir_mount):
        if file.endswith(".gpx"):
            df, points = process_gpx_to_df(dir_mount, file)
            folium.PolyLine(points, popup = file[:-4], color='red', weight=4.5, opacity=.5).add_to(m)

    for file in os.listdir(dir_run):
        if file.endswith(".gpx"):
            df, points = process_gpx_to_df(dir_run, file)
            folium.PolyLine(points, popup = file[:-4], color='blue', weight=4.5, opacity=.5).add_to(m)

    for file in os.listdir(dir_walk):
        if file.endswith(".gpx"):
            df, points = process_gpx_to_df(dir_walk, file)
            folium.PolyLine(points, popup = file[:-4], color='green', weight=4.5, opacity=.5).add_to(m)

    places_df = pd.read_csv('interesting_nature.csv', header = 0, encoding= 'unicode_escape')

    for index, row in places_df.iterrows():
        tooltip = row["place"]
        folium.Marker([row["lat"], row["lon"]], popup="<b>" + str(row["place"]) + "</b>" + "<br>" + str(row["region"]), icon=folium.Icon(icon="tree-conifer", color = 'green'), tooltip=tooltip).add_to(m)

    rest_df = pd.read_csv('restaurants.csv', header = 0, encoding= 'unicode_escape')

    for index, row in rest_df.iterrows():
        tooltip = row["place"]
        folium.Marker([row["lat"], row["lon"]], popup="<b>" + str(row["place"]) + "</b>" + "<br>" + str(row["food"]), icon=folium.Icon(icon="cutlery", color = 'red'), tooltip=tooltip).add_to(m)
    
    track_df = pd.read_csv('tracks.csv', header = 0, encoding= 'unicode_escape')

    for index, row in track_df.iterrows():
        tooltip = row["desc"]
        folium.Marker([row["lat"], row["lon"]], popup='<a>' + str(row["link"]) + "</a>", icon=folium.Icon(icon="tag", color = 'black'), tooltip=tooltip).add_to(m)

    m.save('index.html')



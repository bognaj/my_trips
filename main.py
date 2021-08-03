import folium
import gpxpy
import pandas as pd

def process_gpx_to_df(file_name):
    # https://towardsdatascience.com/build-interactive-gps-activity-maps-from-gpx-files-using-folium-cf9eebba1fe7
    gpx = gpxpy.parse(open(file_name)) 
    track = gpx.tracks[0]
    segment = track.segments[0]
    # Load the data into a Pandas dataframe (by way of a list)
    data = []
    segment_length = segment.length_3d()
    for point_idx, point in enumerate(segment.points):
        data.append([point.longitude, point.latitude,point.elevation, point.time, segment.get_speed(point_idx)])
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
    zoom_start = 12
    df, points = process_gpx_to_df('dfbg.gpx')

    m = folium.Map(location=[ df.Latitude.mean(), df.Longitude.mean()], zoom_start = zoom_start, tiles=None)
    folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(m)

    folium.PolyLine(points, color='red', weight=4.5, opacity=.5).add_to(m)

    m.save('index.html')



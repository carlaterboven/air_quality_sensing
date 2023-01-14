import io
import numpy as np
import pandas as pd

file_name = 'log1'
data = pd.read_csv('../air_quality_sensing/data/' + file_name + '.csv')

file = open(file_name + '.kml', 'w')
file.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n')
file.write('<kml xmlns=\"http://earth.google.com/kml/2.2\">\n')
file.write('<Document>\n')
file.write('\t<name>' + file_name + '.kml' + '</name>\n')
file.write(style_string)
for id in range(len(data)):
    file.write('\t<Placemark>\n')
    file.write('\t\t<name>' + str(data.loc[id, 'time']) + '</name>\n')
    # TODO check for nan values
    # TODO use different colors for bad data
    file.write('<styleUrl>#green</styleUrl>')
    file.write('\t\t<ExtendedData>\n')
    # first 5 columns are LogID, lat, lon. alt, time
    # rest of the columns are relevant vor extended data values of kml placemark
    for value_index in range(5, len(data.iloc[id]), 1):
        file.write('\t\t\t<Data name=' + '\"' + data.columns[value_index] + '\"' + '>\n')
        file.write('\t\t\t\t<value>' + str(data.iloc[id, value_index]) + '</value>\n')
        file.write('\t\t\t</Data>\n')
    file.write('\t\t</ExtendedData>\n')
    file.write('\t\t<Point>\n')
    file.write('\t\t\t<coordinates>' + str(data.loc[id, 'lon']) + ',' + str(data.loc[id, 'lat']) + ',' + str(data.loc[id, 'alt']) + '</coordinates>\n')
    file.write('\t\t</Point>\n')
    file.write('\t</Placemark>\n')
file.write('</Document>\n')
file.write('</kml>\n')
file.close()
print('File Created!')

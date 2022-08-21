import io
import numpy as np
import pandas as pd

file_name = 'log'
data = pd.read_csv('../data/' + file_name + '.csv')

file = open(file_name + '.kml', 'w')
file.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n')
file.write('<kml xmlns=\"http://earth.google.com/kml/2.2\">\n')
file.write('<Document>\n')
file.write('\t<name>' + file_name + '.kml' + '</name>\n')
for id in range(len(data)):  
    file.write('\t<Placemark>\n')
    file.write('\t\t<name>' + str(data.loc[id, 'Time']) + '</name>\n')
    file.write('\t\t<ExtendedData>\n')
    file.write('\t\t\t<Data name=' + '\"PM2.5\"' + '>\n')
    file.write('\t\t\t\t<value>' + str(data.loc[id, 'PM2.5']) + '</value>\n')
    file.write('\t\t\t</Data>\n')
    file.write('\t\t</ExtendedData>\n')
    file.write('\t\t<Point>\n')
    # TODO check for nan values
    # TODO use different colors for bad data
    file.write('\t\t\t<coordinates>' + str(data.loc[id, 'Longitude']) + ',' + str(data.loc[id, 'Latitude']) + ',' + str(data.loc[id, 'Altitude']) + '</coordinates>\n')
    file.write('\t\t</Point>\n')
    file.write('\t</Placemark>\n')
file.write('</Document>\n')
file.write('</kml>\n')
file.close()
print('File Created!')

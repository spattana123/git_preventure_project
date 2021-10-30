import csv
import matplotlib
#matplotlib.use("TKAgg")
from matplotlib import pylab
import numpy as np
import dateutil
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import numpy
        
durations = [];
startTimes = [];

with open('dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if(line_count == 0):
            print(f'Column names are {", ".join(row)}')
        else:
            minutes = row[4];
            startTime = row[1];

            durations.append(minutes);
            startTimes.append(startTime);

        line_count += 1


print(durations);

dates = [dateutil.parser.parse(x) for x in startTimes]
startTimesFormatted = mdates.date2num(dates);

tick_spacing = 1000;

fig, ax = plt.subplots(1,1);

ax.plot(startTimesFormatted, durations);

ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing));

#plt.yticks(np.arange(min(durations), max(durations)+1, step=1000000.0))

plt.xlabel('Start Times in seconds')
# naming the y axis
plt.ylabel('Durations')
 
# giving a title to my graph
plt.title('My first graph!')

plt.show();
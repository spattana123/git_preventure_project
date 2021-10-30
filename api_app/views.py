from django.views import View
from django.http import JsonResponse
import json
from .models import BikeHireModel
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import csv
from datetime import date
import heapq
import json

import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pylab
import numpy as np
import dateutil
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class BikeHirePlot(View):
	def get(self, request):
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

		plt.yticks(color='w')
		#plt.yticks(np.arange(min(durations), max(durations)+1, 1000000.0))
		plt.plot(startTimesFormatted, durations);
		


		plt.xlabel('x - axis')
		# naming the y axis
		plt.ylabel('y - axis')
 
		# giving a title to my graph
		plt.title('My first graph!')

		plt.show();
		#rawTrendLine = {};

		'''
		for index in range(len(startTimes)):
			rawTrendLine[startTimes[index]] = durations[index];
			print(startTimes[index], durations[index]);
		'''

		#pylab.plot(startTimesFormatted, durations);

			
		'''
		print("startTimesFormatted:")
		print(startTimesFormatted);

		z = numpy.polyfit(startTimesFormatted.apply(str), durations, 1);
		p = numpy.poly1d(z);

		polyX = numpy.linspace(startTimesFormatted.min(), startTimesFormatted.max(), 100)
		pylab.plot(polyX, p(polyX), "r")

		loc = mdates.AutoDateLocator()
		plt.gca().xaxis.set_major_locator(loc)
		plt.gca().xaxis.set_major_formatter(mdates.AutoDateLocator(loc))
		plt.gcf().autofmt_xdate()

		'''
		
			

		#pylab.show()

		return JsonResponse({"Plot Displayed"}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class BikeHire(View):
	def get(self, request):
		todays_date = date.today();
		year = todays_date.year;
		stations = {};
		stations_age = {};
		stations_revenue = {};
		stations_ids = {};
		durations = [];
		startTimes = [];

		#get data from csv file
		with open('dataset.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if(line_count == 0):
					print(f'Column names are {", ".join(row)}')
				else:
					print(row)
					from_station = row[6];
					end_station = row[8];

					byear = row[10];

					minutes = row[4];
					startTime = row[1];

					durations.append(minutes);
					startTimes.append(startTime);

					minutes_without_symbol=minutes[1:].replace(',', '')
					revenue = (float(minutes_without_symbol)/600);

					if(not from_station in stations_revenue):
						stations_revenue[from_station] = 0;

					stations_revenue[from_station] += revenue;

					stationId = row[3];

					if(not from_station in stations_ids):
						stations_ids[from_station] = stationId

					birthyear = year;

					if(not byear == ''):
						birthyear = int(byear);


					print("current year: ",year)
					print("birthyear: ",birthyear);

					age = year - birthyear;

					print("age is ", age);

					if(not from_station in stations):
						stations[from_station] = {};
					
					if(not end_station in stations[from_station]):
						stations[from_station][end_station] = 1;
					else:
						stations[from_station][end_station] += 1;

					if(not from_station in stations_age):
						stations_age[from_station] = {};
						stations_age[from_station]["0-15"] = 0;
						stations_age[from_station]["16-30"] = 0;
						stations_age[from_station]["35-45"] = 0;
						stations_age[from_station]["46+"] = 0;

					if(age >= 0 and age <= 15):
						stations_age[from_station]["0-15"] += 1;
					elif(age >= 16 and age <= 30):
						stations_age[from_station]["16-30"] += 1;
					elif(age >= 35 and age <= 45):
						stations_age[from_station]["35-45"] += 1;
					else:
						stations_age[from_station]["46+"] += 1;



				line_count += 1

			print(f'Processed {line_count} lines.')

			stations_maxdestination = {};
			for fstation, estation in stations.items():
				print("\nFrom Station:", fstation)
				max_count = 0
				max_destination = ""
				for key in estation:
					val = estation[key]
					print(key + ":", val)

					if(val > max_count):
						max_count = val
						max_destination = key

				print("\nMost Visited Destination from: "+fstation+" is "+max_destination);
				stations_maxdestination[fstation] = max_destination;

			stations_maxage = {};
			for fstation, age_bucket in stations_age.items():
				print("\nFrom Station:", fstation)
				max_count = 0
				max_bucket = ""
				for key in age_bucket:
					val = age_bucket[key]
					print(key + ":", val)
					if(val > max_count):
						max_count = val
						max_bucket = key

				print("\nAges that visit station: "+fstation+" is "+max_bucket);
				stations_maxage[fstation] = max_bucket;

			li = [];
			heapq.heapify(li);
			rev_stations = {};
			repairIds = [];
			for fstation in stations_revenue:
				rev = stations_revenue[fstation];
				heapq.heappush(li, rev);
				rev_stations[rev] = fstation;
				if(rev > 1.66666):
					repairIds.append(stations_ids[fstation]);

				print("\nRevenue From Station:"+fstation+" is "+str(rev));

			largestThreeRevs = heapq.nlargest(3,li);
			largestThreeStations = [];
			for r in largestThreeRevs:
				largestThreeStations.append(rev_stations[r]);

			print("The largest 3 stations are: ");
			print(largestThreeStations);

			print("Bikes that need repair");
			print(repairIds);


		dates = [dateutil.parser.parse(x) for x in startTimes]
		#startTimesFormatted = mdates.date2num(dates);
		rawTrendLine = {};
		for index in range(len(startTimes)):
			rawTrendLine[startTimes[index]] = durations[index];
			print(startTimes[index], durations[index]);


		data = {"Most Frequented Destination For Each Station": stations_maxdestination,
				"Most Frequent Age Group For Each Station": stations_maxage,
				"Revenue From Each Station": stations_revenue,
				"Top 3 Stations that generate the most revenue": largestThreeStations,
				"Stations that need repair": repairIds,
				"Trend line of Raw Values": rawTrendLine
				};

		'''
		pylab.plot(startTimesFormatted, durations,'o');

			
		
		z = numpy.polyfit(startTimesFormatted, durations, 1);
		p = numpy.poly1d(z);

		polyX = numpy.linspace(startTimesFormatted.min(), startTimesFormatted.max(), 100)
		pylab.plot(polyX, p(polyX), "r")

		loc = mdates.AutoDateLocator()
		plt.gca().xaxis.set_major_locator(loc)
		plt.gca().xaxis.set_major_formatter(mdates.AutoDateLocator(loc))
		plt.gcf().autofmt_xdate()
		
			

		pylab.show()
		'''

		return JsonResponse(data, status=201)



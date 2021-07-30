
# Part 1 Tasks
# 1 - Write methods in HourlyWeather class
#          __repr__
#          average_temp
#          __eq__
#          __lt__
#          __gt__
#          freeze_warning
# 2 - Write methods in CompareWeather class
#          __repr__
#          find_av_warmest_city
#          find_av_coldest_city
#
########################################################################

# Import libraries

import requests
import csv
import os


########################################################################

#  HELPER FUNCTIONS - ALREADY DONE FOR YOU

########################################################################

def read_file(filename):
  '''
  DO NOT TOUCH. This is already completed for you.
    
  Reads longitude and latitude data from a csv file
  Stores location (city and state), latitude and longitude in lists
    
  csv file from:
    https://simplemaps.com/data/us-cities
    
  csv file format:
    0(City), 2(State), 6(latitude), 7(longitude)
    
  Parameter 
    filename: a string
    
  Returns: 
    location, a list of strings with city and state
    latitude, a list of strings of the latitude of the locations
    longitude, a list of strings of longitude of the locations
  '''

  # Initialize lists
  location = []
  lat = []
  long = []
    
  # Column locations for city, state, latitude, and longitude data
  CITY = 0
  STATE = 2
  LATITUDE = 6
  LONGITUDE = 7
  with open(filename, newline='') as csvfile: # creates a file object
    csvreader = csv.reader(csvfile, delimiter=',')  # set for reading csv file
        
    next(csvreader) # skips header
        
    for row in csvreader:  # read data
      # Check that all fields are present
      if row[CITY] and row[STATE] and row[LATITUDE] and row[LONGITUDE]:
        # Create a string that includes the city and state
        location.append( row[CITY] + ', ' + row[STATE] )
        # Create lists of strings for latitude and longitude of the location
        lat.append( row[LATITUDE] )
        long.append( row[LONGITUDE] )
                
  return location, lat, long


def print_locations(location, lat, long):
  '''
  DO NOT TOUCH. This is already completed for you.
  
  Print the location, latitude, and longitude
    
  Return: None
  '''
    
  # Print header
  print("-" * 40)
  print(f'{"Location":^20}{"Latitude":^10}{"Longitude":^10}')
  print("-" * 40)

  # Print values
  for i in range(len(location)):
    print(f'{location[i]:^20s}{lat[i]:^10s}{long[i]:^10s}')


def hourly_weather_from_api(loc, lat, long):
  '''
  DO NOT TOUCH. This is already completed for you.
    
  Returns weather data from api.weather.gov
    
  Parameters:
    loc, a string, the location for the given latitude and longitude
    lat, a string, the latitude of a location
    long, a string, the longitude of a location
        
  Return value:
    an instance of HourlyWeather with parameters:
      loc, a string, the location
      start_times, a list of strings with format 
        of yyyy-mm-dd T hr:min:sec-time zone
      temperatures, a list of integers, next week of hourly temperatures 
  '''
    
  # API URL for week of daily forecasts
  api_url = "https://api.weather.gov/points/" + lat + "," + long + "/forecast/hourly"

  # Insure that keys "properties" and "periods" exist
  while True:
    # data is a dictionary
    data = requests.get(api_url).json()
    # If keys not present, data requested again
    if "properties" in data:
      if "periods" in data["properties"]:
        break
            
  # weather_list contains hourly forecasts for the week
  weather_list = data["properties"]["periods"]
  start_times = []
  temperatures = []
    
  # Add the time and temperature for each hourly forecast to lists
  for d in weather_list:
    if d['startTime'] and d['temperature']:
      start_times.append(d['startTime'])
      temperatures.append(d['temperature'])
    
  return HourlyWeather(loc, start_times, temperatures)


def hourly_weather_from_file(filename):
  '''
  DO NOT TOUCH. This is already completed for you.
    
  Reads temperature forecasts from a txt file
  First line of each file is the location: city, state abbreviation
  Remaining lines include start time and temperature for the hourly forecast
  separated by a space
  0(start_times) 1(temperatures)
    
  Parameter 
    filename: a string
    
  Return value:
    an instance of HourlyWeather with parameters:
      loc, a string, the location
      start_times, a list of strings with format 
      of yyyy-mm-dd T hr:min:sec-time zone
      temperatures, a list of integers, next week of hourly temperatures 
  '''

  # Initialize lists
  start_times = []
  temperatures = []
    
  # Location of data in line
  START_TIME = 0
  TEMP = 1
    
  fin = open(filename,'r')
    
  loc = fin.readline() # Reads first line of the file with the location
  loc = loc.strip()    # Strips line feed
    
  # Read in file
  for line in fin:
    line = line.strip()         # Strips line feed
    line_list = line.split()    # Splits line on space
    if line_list[START_TIME] and line_list[TEMP]:
      # Add start_times and temperatures to lists
      start_times.append(line_list[START_TIME])
      temperatures.append(int(line_list[TEMP]))
    
  fin.close()
  
  return HourlyWeather(loc, start_times, temperatures)


########################################################################
#
#     WRITE METHODS FOR THE HourlyWeather class
#
########################################################################

class HourlyWeather:
  '''    
  Class to hold hourly temperature forecasts for an individual city
  '''

  def __init__(self, location, start_times, temperatures):
    '''
    DO NOT TOUCH. This is already completed for you.
    Creates instance of HourlyWeather
    '''    
    self.loc = location  # location as a string
    self.start_times = start_times  # list of strings 
    # each string is in the form of yyyy-mm-dd hr:min:sec time zone
    self.temperatures = temperatures # list of integers
    # each integer is an hourly-forecasted temperatures
        

  def __repr__(self):
    #''' TODO PART 1
    #Returns a string representation of an 
    #instance of the HourlyWeather class
    to_be_returned = "\n------------------------------\n\t"+self.loc+"\t\n------------------------------\n    Date\tTime\tTemperature\n\t\t\t  (degree F)\n------------------------------\n"
    for i,j in zip(self.start_times,self.temperatures):
          to_be_returned = to_be_returned+" "+i+"\t"+str(j)+"\t\n"

    return to_be_returned;

    

  def average_temp(self):
    '''  TODO PART 1
    Find the average temperature over first 24 hours
    of temperature forecasts
        
    Parameters:
      self.temperatures, a list of integers
            
    Returns:
      average temperature, a float
        the average of the first 24 values in self.temperatures
    '''
    temperatures = self.temperatures
    average_temperature = sum(temperatures)/len(temperatures)
    
    return average_temperature
   
  def __eq__(self, other):
    ''' TODO PART 1
    Overloading of == operator
        
    Parameter: 
      other, another member of the HourlyWeather class
        
    Returns:
      True if the average temperature of self.temperatures 
        is the equal to that of other.temperatures
        The average is for the first 24 forecasted temperatures.
      Otherwise, returns False
    '''
    if(other.average_temp() == self.average_temp()):
      return True
    return False
    
    
  def __lt__(self, other):
    ''' TODO PART 1
    Overloading of < operator
        
    Parameter:
      other, another member of the HourlyWeather class
        
    Returns: 
      True if the average temperature of self.temperatures 
      is less than that of other.temperatures
      The average is for the first 24 forecasted temperatures.
      Otherwise, returns False
    '''
    if(other.average_temp() < self.average_temp()):
      return True
    return False

    
    
  def __gt__(self, other):
    ''' TODO PART 1
    Overloading of > operator
        
    Parameter:
      other, another member of the HourlyWeather class
        
    Returns:
      True if the average temperature of self.temperatures 
        is greater than that of other.temperatures
        The average is for the first 24 forecasted temperatures.
      Otherwise, returns False
    '''
    if(other.average_temp() > self.average_temp()):
      return True
    return False
    
    
  def freeze_warning(self):
    '''
    Returns a list of times and dates when frost is forecasted
        
    Return:
      warning_list, a list of strings
        each string corresponds to a date and time when the
        temperature is forcasted to be 32 degrees F or less
    '''
    warning_list = []
    for i,j in zip(self.temperatures,self.start_times):
          if(i <= 32):
                warning_list.append(j)
    return warning_list
    

########################################################################
#
#     WRITE METHODS FOR THE CompareWeather class
#
########################################################################

class CompareWeather:
  '''    
  Class to collect instances of the HourlyWeather class in a list
  '''
    
  def __init__(self):
    '''
    DO NOT TOUCH. This is already completed for you
        
    Creates an instance of the CompareWeather class
    '''
    self.cities_weather = [] # List to hold HourlyWeather class instances
    

  def __repr__(self):
    ''' TODO PART 1
    Returns a string representation of 
    an instance of the CompareWeather class
    '''
    returning_str = "****************************************\n  Location\t\tTemperature\n\t\t\t(degrees F)\n****************************************\n"
    for i in self.cities_weather:
          returning_str = returning_str+i.loc+"\t\t"+str(i.average_temp())+"\n"

  

    return returning_str


    
  def add_single_city_weather(self, city_weather):
    '''
    Method to add a single instance of the 
    HourlyWeather class to the list self.cities_weather
        
    Parameter:
      city_weather, an instance of the HourlyWeather class
    '''
    self.cities_weather.append(city_weather)
        
    
  def add_weather_from_api(self, filename):
    '''
    Method to add instances of the HourlyWeather class
    created from api data to the list self.cities_weather 
        
    Parameter: 
      filename, a string, provides the name of the csv file
        with location, latitude, and longitude data obtained from 
        https://simplemaps.com/data/us-cities
        
    For each location in the csv file named filename, an instance of the 
    HourlyWeather Class is added to self.cities_weather
    '''
        
    # Obtain location( city and state) and latitude and longitude
    location, lat, long = read_file(filename)
    print_locations(location, lat, long)
        
        
    # Create and add instances of HourlyWeather to self.cities_weather
    for i in range(len(location)):
      weather_instance = hourly_weather_from_api(location[i], str(lat[i]), str(long[i]))
      self.cities_weather.append(weather_instance)
      print("Loaded data from", location[i]) # Verify data obtained
            

  def add_weather_from_files(self, filenames):
    '''
    Method to add instances of the HourlyWeather class
    to the list self.cities_weather from forecasts saved in txt files
        
    Parameter:
      filenames, a list of strings
        each string is a filename for txt file with forecast data
                
    For each txt file with forecast data, an instance of the 
    HourlyWeather Class is added to self.cities_weather
    '''
    for filename in filenames:
      hourly_weather_instance = hourly_weather_from_file(filename)
      self.add_single_city_weather(hourly_weather_instance)
            
            
  def find_av_warmest_city(self):
    ''' TODO PART 1
    Returns the HourlyWeather class instance
    with the highest average temperature
        
    Return:
      warmest city, an instance of the HourlyWeather class,
        with the warmest average temperature of all the instances
        in the list self.all_weather
    '''
    instances = self.cities_weather
    highest = instances[0]
    for k in instances:
      k.average_temp()
      if k > highest:
        highest = k
    return highest


  def find_av_coldest_city(self):
    ''' TODO PART 1
    Returns the HourlyWeather class instance
    with the lowest average temperature
        
    Return:
      coldest city, an instance of the HourlyWeather class,
        with the lowest average temperature of all the instances
        in the list self.all_weather
    '''
    instances = self.cities_weather
    lowest = instances[0]
    for j in instances:
      j.average_temp()
      if j < lowest:
        lowest = j
    return lowest
    

########################################################################
#
#     main function is written for you
#
########################################################################

def main():
  '''
  Creates an instance of the CompareWeather class
  from api or saved forecast data
        
  Return: None
  '''
    
  # Create an instance of the CompareWeather class
  all_cities = CompareWeather()
    
  selection = input("Do you want to use the API(1) or saved data?(2)")
  if selection == '1':
    # USE API to populate with HourlyWeather class instances
    filename = 'us_cities_10.csv'
    all_cities.add_weather_from_api(filename)
  elif selection == '2':
    # USE saved data to populate with HourlyWeather class instances
    filenames = ["nyc.txt", "losangeles.txt", "chicago.txt", "miami.txt", "dallas.txt", "philly.txt", "houston.txt", "atlanta.txt", "washington.txt", "boston.txt"]
    all_cities.add_weather_from_files(filenames)
  else:
    print("Selection not found")
  print(all_cities)
  


    
# main()
# Add your name here
# Add date
#
# Part 2 Tasks
# 1  - Write methods in CompareWeather class
#          find_av_of_av(self)
#          find_t_pref_city(self, t_pref)
# 2  - Write functions not part of other classes
#          locations_menu()
#          build_compare_weather_instance() 
#          plot_temperatures(cities)
#          create_report(all_cities)
#
###############################################################################
import os 
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"

# Import libraries

import requests
import csv
import matplotlib.pyplot as plt

###############################################################################

# CONSTANTS USED FOR READING DATA FROM FILE OR API


LOCATIONS = ['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Miami, FL', 'Dallas, TX', 'Philadelphia, PA', 'Houston, TX', 'Atlanta, GA', 'Washington, DC', 'Boston, MA']
LATITUDES =  ['40.6943', '34.1139', '41.8373', '25.7839', '32.7936', '40.0077', '29.7863', '33.7627', '38.9047', '42.3188']
LONGITUDES =  ['-73.9249', '-118.4068', '-87.6862', '-80.2102', '-96.7662', '-75.1339', '-95.3889', '-84.4224', '-77.0163', '-71.0846']
FILENAMES = ["nyc.txt", "losangeles.txt", "chicago.txt", "miami.txt", "dallas.txt", "philly.txt", "houston.txt", "atlanta.txt", "washington.txt", "boston.txt"]


###############################################################################


# Add your functions and classes from Part 1


###############################################################################
# 
# WRITE METHODS FOR THE CompareWeather class
#
###############################################################################

class CompareWeather:
  '''    
  Class to collect instances of the HourlyWeather class in a list
  '''
    
  def __init__(self):
    '''
    DO NOT TOUCH. This is already completed for you
        
    Creates an instance of the CompareWeather class
    '''
    self.cities_weather = [] # List to hold HourlyWeather class instances
  

  def __repr__(self):
    ''' TODO PART 1
    Returns a string representation of 
    an instance of the CompareWeather class
    '''
    returning_str = "****************************************\n  Location\t\tTemperature\n\t\t\t(degrees F)\n****************************************\n"
    for i in self.cities_weather:
          returning_str = returning_str+i.loc+"\t\t"+str(i.average_temp())+"\n"

  

    return returning_str


    
  def add_single_city_weather(self, city_weather):
    '''
    Method to add a single instance of the 
    HourlyWeather class to the list self.cities_weather
        
    Parameter:
      city_weather, an instance of the HourlyWeather class
    '''
    self.cities_weather.append(city_weather)
    
  def add_weather_from_api(self, filename):
    '''
    Method to add instances of the HourlyWeather class
    created from api data to the list self.cities_weather 
        
    Parameter: 
      filename, a string, provides the name of the csv file
        with location, latitude, and longitude data obtained from 
        https://simplemaps.com/data/us-cities
        
    For each location in the csv file named filename, an instance of the 
    HourlyWeather Class is added to self.cities_weather
    '''
        
    # Obtain location( city and state) and latitude and longitude
    location, lat, long = read_file(filename)
    print_locations(location, lat, long)
        
        
    # Create and add instances of HourlyWeather to self.cities_weather
    for i in range(len(location)):
      weather_instance = hourly_weather_from_api(location[i], str(lat[i]), str(long[i]))
      self.cities_weather.append(weather_instance)
      print("Loaded data from", location[i]) # Verify data obtained
            

  def add_weather_from_files(self, filenames):
    '''
    Method to add instances of the HourlyWeather class
    to the list self.cities_weather from forecasts saved in txt files
        
    Parameter:
      filenames, a list of strings
        each string is a filename for txt file with forecast data
                
    For each txt file with forecast data, an instance of the 
    HourlyWeather Class is added to self.cities_weather
    '''
    for filename in filenames:
      hourly_weather_instance = hourly_weather_from_file(filename)
      self.add_single_city_weather(hourly_weather_instance)
            
            
  def find_av_warmest_city(self):
    ''' TODO PART 1
    Returns the HourlyWeather class instance
    with the highest average temperature
        
    Return:
      warmest city, an instance of the HourlyWeather class,
        with the warmest average temperature of all the instances
        in the list self.all_weather
    '''
    instances = self.cities_weather
    highest = instances[0]
    for k in instances:
      k.average_temp()
      if k > highest:
        highest = k
    return highest


  def find_av_coldest_city(self):
    ''' TODO PART 1
    Returns the HourlyWeather class instance
    with the lowest average temperature
        
    Return:
      coldest city, an instance of the HourlyWeather class,
        with the lowest average temperature of all the instances
        in the list self.all_weather
    '''
    instances = self.cities_weather
    lowest = instances[0]
    for j in instances:
      j.average_temp()
      if j < lowest:
        lowest = j
    return lowest
    


# Add other methods from the CompareWeather class


  def find_av_of_av(self):
    '''TODO Part 2
    Returns the average of the average temperatures for each city
    (each HourlyWeather class instance in the list self.cities_weather)
    The average for each city is the average of the first 24 temperature forecasts
        
    Return:
      t_av, a float, the average of the average temperatures for 
            each city
    '''
    avgs = []
    for i in self.cities_weather:
          avgs.append(i.average_temp())
    t_av = sum(avgs)/len(avgs)
    return t_av


  def find_t_pref_city(self, t_pref):
    '''TODO Part 2
    Returns the HourlyWeather class instance in the list self.cities_weather
    with the average temperature closest to a preferred temperature
    
    Parameter:
      t_pref, an integer, the preferred environmental temperature of the user
        
    Return:
      pref_city, an instance of the HourlyWeather class,
          with the 24 hourly-forecast average temperature closest 
          to t_pref
    '''      

    pref_city = min(self.cities_weather, key=lambda x:abs(x.average_temp()-float(t_pref)))
    return pref_city


###############################################################################
# 
# New functions not part of any class
#
###############################################################################


def locations_menu():
    '''TODO Part 2 
    Print menu of location options
    
    Parameter: None
    Return: None
    '''
    locations_output = "**************************************************\nAvailable Locations:\n"
    for i in range(len(LOCATIONS)):
          locations_output = locations_output+str(i)+" "+LOCATIONS[i]+"\n"
    locations_output = locations_output + "**************************************************"
    
    print(locations_output)
    
    pass


def build_compare_weather_instance():
  '''TODO Part 2 
  Returns an instance of the CompareWeather Class
    
  User asked for input to select:
    - location of forecasts included in the instance
    - method to retrieve the forecasts (api or .txt file)

  Return  
    all_cities, an instance of the CompareWeather class
  '''

  all_cities = CompareWeather()
  
  while True:
    locations_menu()
    print("\nTo add a locaation to your weathor report,\nenter a number corresponding to a location (0-9)\nor enter q to stop adding locations.\n**************************************************")
    choice = input("Enter your choice:")
    if(choice=='q'):
      return all_cities
    elif choice.isdigit() and int(choice) <=9:
      h = []
      choice2 = input("Do you want forecast data to be obtained to construct an instance of the HourlyWeather?\n 1 from api.weather.gov, 2 from local files: ")
      if(choice2=='1'):
            h = hourly_weather_from_api(LOCATIONS[int(choice)],LATITUDES[int(choice)],LONGITUDES[int(choice)])

      elif(choice2=='2'):
            h = hourly_weather_from_file(FILENAMES[int(choice)])
      else:
            print("Invalid input")
            pass
      all_cities.add_single_city_weather(h)
      print("Weather added")
    else:
      print("Invalid input")
      pass

  return all_cities
  



def plot_temperatures(cities):
  '''TODO Part 2  Plot the hourly temperatures for each instance
  of HourlyWeather in the list cities

  Parameter
    cities, a list of instances of the HourlyWeather class

  Return
    None
  '''

  fig, ax = plt.subplots(len(cities), figsize=(6, 6))
  for i in range(len(cities)):
        ax[i].scatter(cities[i].start_times,cities[i].temperatures)
        ax[i].legend(cities[i].loc)
        
  
  plt.xlabel("Time (hours from current time)")
  plt.ylabel("Forecasted Temperature")
  plt.show()


def create_report(all_cities):
  '''TODO Part 2
  Ask the user for their preferred environmental temperature
  Make a report to:
    -print the average temperature for each instance of HourlyWeather
      in all_cities
    -print warmest_city, city with the highest average 24 hour temperature
    -print coldest_city, cotu with the lowest average 24 hour temperature
    -print pref_city, city with the average 24 hour temperature closest to the
      prefered temperature of the user
    -print the average of all the 24 hour average temperatures for 
        each city in all cities
    -plot the temperatures for 24 hours for coldest_city,pref_city, and warmest_city
        
  Parameter:
    all_cities, an instance of the CompareWeather class
        
  Return:
    None
    
  '''

  pref_temp = input("Enter your preferred environmental temperature: ")
  print("****************************************\n\tAverage of 24 Hourly Forecasts\n****************************************\n\tLocation\tTemperature (F)\n****************************************\n")

  for i in all_cities.cities_weather:
        print("  "+i.loc+"\t"+str(i.average_temp()))
  print("**** Results ****")
  print("Warmest city: "+all_cities.find_av_warmest_city().loc)
  print("Coldest city: "+all_cities.find_av_coldest_city().loc)
  print("Preferred city: "+all_cities.find_t_pref_city(pref_temp).loc)
  print("Average temperature of all cities: "+str(all_cities.find_av_of_av()))
  plot_temperatures(all_cities.cities_weather)
  


###############################################################################
#
#     main function is written for you
#
###############################################################################

def main():
  '''
  Calls functions for weather analysis
        
  Return: None
  '''

  # Create an instance of the CompareWeather class
  all_cities = CompareWeather()    
  FILENAMES = ["nyc.txt", "losangeles.txt", "chicago.txt", "miami.txt","dallas.txt", "philly.txt", "houston.txt", "atlanta.txt", "washington.txt","boston.txt"]
  all_cities.add_weather_from_files(FILENAMES)
  
  # Analyze the weather
  create_report(all_cities)


main()

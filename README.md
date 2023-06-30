# Summary
In light of Roe v. Wade being overturned and amidst growing concerns about private data security, I wanted to develop an app that would store my data locally on my device, where it won’t be accessed by or sold to third parties.  The user reports periods to the app, which then analyzes the user-provided, locally-stored information to forecast periods and ovulation dates.  

# What are the files in this project?
main.py – this houses all of the code necessary to run the app.  Note that the app has different ‘states’ that determine which screen to load and what actions to take based on user input.

assets folder – this has all the images used in the app, which were created using Inkscape (https://inkscape.org/).

fonts folder – this has the font used in the app (junction from https://www.theleagueofmoveabletype.com/).

# What libraries are used?
pygame – https://www.pygame.org/docs/ - used to build the primary user interface.

sys – https://docs.python.org/3/library/sys.html - used to exit the app when the close button is pressed.

datetime – https://docs.python.org/3/library/datetime.html - used to create date objects and manipulate them for future projections.

calendar – https://docs.python.org/3/library/calendar.html - used to determine the appropriate date ranges to use for the calendar display.

time – https://docs.python.org/3/library/time.html - sleep method used to create short delays to allow the user to read disclaimers.

csv – https://docs.python.org/3/library/csv.html - used to pull data from and write data to the csv file used to track information.

pandas – https://pandas.pydata.org/docs/ - used to create data frames based on the csv file to project next dates and determine averages.

os – https://docs.python.org/3/library/os.html - used to determine if the csv data file exists or if this is the first time the user has launched the app.

# What are the future features/fixes?
It would have been better to have built buttons, animations, and input boxes as reusable classes/functions.  It would also be cool to have settings to toggle things like a bigger screen size, ‘dark’ mode color swaps, and bigger font sizes.

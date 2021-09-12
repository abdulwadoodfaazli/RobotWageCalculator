##########################################################################
# Authors: Masood Ahmed & Abdulwadood Ashraf Faazli
# TeamName: NameError
# Description: This program helps in calculating the wage of a robot which cleans the house
#########################################################################
# Assumptions:
# Input is in a uniform nested Dictionary format
# The shift timings and wage values may change in the input dictionary but there format remains the same
######################################################################

# sample_1 = {"shift": {"start": "2038-01-01T20:15:00","end": "2038-01-02T04:15:00"},"roboRate": {"standardDay": {"start": "07:00:00","end": "23:00:00","value": 20},"standardNight": {"start": "23:00:00","end": "07:00:00","value": 25},"extraDay": {"start": "07:00:00","end": "23:00:00","value": 30},"extraNight": {"start": "23:00:00","end": "07:00:00","value": 35}}}
# sample_2 = {"shift": {"start": "2038-01-01T20:15:00","end": "2038-01-02T08:15:00"},"roboRate": {"standardDay": {"start": "07:00:00","end": "23:00:00","value": 20},"standardNight": {"start": "23:00:00","end": "07:00:00","value": 25},"extraDay": {"start": "07:00:00","end": "23:00:00","value": 30},"extraNight": {"start": "23:00:00","end": "07:00:00","value": 35}}}
# sample_3 = {"shift": {"start": "2038-01-11T07:00:00","end": "2038-01-17T19:00:00"},"roboRate": {"standardDay": {"start": "07:00:00","end": "23:00:00","value": 20},"standardNight": {"start": "23:00:00","end": "07:00:00","value": 25},"extraDay": {"start": "07:00:00","end": "23:00:00","value": 30},"extraNight": {"start": "23:00:00","end": "07:00:00","value": 35}}}
# sample_4 = {"shift": {"start": "2038-01-01T20:15:00","end": "2038-01-02T04:16:00"},"roboRate": {"standardDay": {"start": "07:00:00","end": "23:00:00","value": 20},"standardNight": {"start": "23:00:00","end": "07:00:00","value": 25},"extraDay": {"start": "07:00:00","end": "23:00:00","value": 30},"extraNight": {"start": "23:00:00","end": "07:00:00","value": 35}}}
# sample_5 = {"shift": {"start": "2038-01-01T20:15:00","end": "2038-01-02T05:16:00"},"roboRate": {"standardDay": {"start": "07:00:00","end": "23:00:00","value": 20},"standardNight": {"start": "23:00:00","end": "07:00:00","value": 25},"extraDay": {"start": "07:00:00","end": "23:00:00","value": 30},"extraNight": {"start": "23:00:00","end": "07:00:00","value": 35}}}


# Importing necessary libraries that we are using

import calendar
import ast
from datetime import datetime
from datetime import timedelta

# This code takes dictionary as input and gives type dict for the string input

inputFromUser = input("Please enter a dictionary: ")
formattedInput = ast.literal_eval(inputFromUser)

# Creating variables to store rates

standardDayValue = formattedInput["roboRate"]["standardDay"]["value"]
standardNightValue = formattedInput["roboRate"]["standardNight"]["value"]
extraDayValue = formattedInput["roboRate"]["extraDay"]["value"]
extraNightValue = formattedInput["roboRate"]["extraNight"]["value"]

# This gives us the start and end timings of the robot

endTiming = formattedInput['shift']['end'].split('T')
startTiming = formattedInput['shift']['start'].split('T')

# This piece of code gives us the specific months and dates of the day from the string given in the string

startMonth = int(startTiming[0][5] + startTiming[0][6])
startDay = int(startTiming[0][8] + startTiming[0][9])
endMonth = int(endTiming[0][5] + endTiming[0][6])
endDay = int(endTiming[0][8] + endTiming[0][9])

# Finding the weekday on any given day and night
# 0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday, 5 = Saturday, 6 = Sunday

startDay = calendar.weekday(2038, startMonth, startDay)
endDay = calendar.weekday(2038, endMonth, endDay)

# Creating datetime objects for different timestamps

# For start of robot shift:
robotStartString = formattedInput['shift']['start'].replace('T', ' ')
robotStartDatetime = datetime.strptime(robotStartString, '%Y-%m-%d %H:%M:%S')

# For end of robot shift:
robotEndString = formattedInput['shift']['end'].replace('T', ' ')
robotEndDatetime = datetime.strptime(robotEndString, '%Y-%m-%d %H:%M:%S')

# For start of day shifts:
shiftStartString = formattedInput['roboRate']['standardDay']['start'].replace('T', ' ')
shiftStartDatetime = datetime.strptime(shiftStartString, '%H:%M:%S')

# For start of night shifts:
shiftEndString = formattedInput['roboRate']['standardDay']['end'].replace('T', ' ')
shiftEndDatetime = datetime.strptime(shiftEndString, '%H:%M:%S')

# A variable that stores the final answer

wage = 0

# This code checks if the robot needs to rest now or not

eightHourTimeCheck = robotStartDatetime + timedelta(minutes=480)

# The following block of code checks if the robot only works on a single day and calculates wages accordingly

if (robotStartDatetime.date() == robotEndDatetime.date()):

    # Condition to check whether it is a weekday or a weekend

    if startDay in [0, 1, 2, 3, 4]:
        dayWage = standardDayValue
        nightWage = standardNightValue
    else:
        dayWage = extraDayValue
        nightWage = extraNightValue

    # While Loop will run until robot's working time does not end

    while robotStartDatetime.time() < robotEndDatetime.time():

        # The first IF condition checks for day shifts

        if (
                robotStartDatetime.time() >= shiftStartDatetime.time() and robotStartDatetime.time() < shiftEndDatetime.time()):
            wage += dayWage
            robotStartDatetime += timedelta(minutes=1)

            # To take care of robot's break

            if robotStartDatetime == eightHourTimeCheck:
                robotStartDatetime += timedelta(minutes=60)
                eightHourTimeCheck = robotStartDatetime + timedelta(minutes=480)

        # The second condition checks for night shift from 00:00:00 till 07:00:00

        elif (robotStartDatetime.time() < shiftStartDatetime.time()):
            wage += nightWage
            robotStartDatetime += timedelta(minutes=1)

            # To take care of robot's break

            if robotStartDatetime == eightHourTimeCheck:
                robotStartDatetime += timedelta(minutes=60)
                eightHourTimeCheck = robotStartDatetime + timedelta(minutes=480)

        # The third condition checks for night shift from 23:00:00 till 00:00:00

        elif (robotStartDatetime.time() >= shiftEndDatetime.time()):
            wage += nightWage
            robotStartDatetime += timedelta(minutes=1)

            # To take care of robot's break

            if robotStartDatetime == eightHourTimeCheck:
                robotStartDatetime += timedelta(minutes=60)
                eightHourTimeCheck = robotStartDatetime + timedelta(minutes=480)

# The following block of code checks if the robot works on multiple days and calculates wages accordingly

if (robotStartDatetime != robotEndDatetime):

    # While Loop will run until robot's working time does not end

    while (robotStartDatetime < robotEndDatetime):

        # Condition to check whether it is a weekday or a weekend

        if (robotStartDatetime.weekday() == 5) or (robotStartDatetime.weekday() == 6):
            dayWage = extraDayValue
            nightWage = extraNightValue
        else:
            dayWage = standardDayValue
            nightWage = standardNightValue

        # The first IF condition checks for day shifts

        if (
                robotStartDatetime.time() >= shiftStartDatetime.time() and robotStartDatetime.time() < shiftEndDatetime.time()):
            wage += dayWage
            robotStartDatetime += timedelta(minutes=1)
            if robotStartDatetime == eightHourTimeCheck:
                robotStartDatetime += timedelta(minutes=60)
                eightHourTimeCheck = robotStartDatetime + timedelta(minutes=480)

        # The second condition checks for night shift from 00:00:00 till 07:00:00

        elif (robotStartDatetime.time() < shiftStartDatetime.time()):
            wage += nightWage
            robotStartDatetime += timedelta(minutes=1)
            if robotStartDatetime == eightHourTimeCheck:
                robotStartDatetime += timedelta(minutes=60)
                eightHourTimeCheck = robotStartDatetime + timedelta(minutes=480)

        # The third condition checks for night shift from 23:00:00 till 00:00:00

        elif (robotStartDatetime.time() >= shiftEndDatetime.time()):
            wage += nightWage
            robotStartDatetime += timedelta(minutes=1)
            if robotStartDatetime == eightHourTimeCheck:
                robotStartDatetime += timedelta(minutes=60)
                eightHourTimeCheck = robotStartDatetime + timedelta(minutes=480)

# Outputting Answer in the given format

Answer = {"value": wage}
print(Answer)

#################################### STAY SAFE! ####################################
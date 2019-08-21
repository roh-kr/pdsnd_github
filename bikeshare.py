import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('\nPlease enter the city you would like to choose (chicago, new york city, washington)\n').lower()
        except:
            #Exception Error Handling
            print('\nSorry, that input isn\'t valid, please try again\n')
            continue
        if city not in ('chicago','new york city','washington'):
            #Incorrect Input Handling
            print('\nPlease enter one of the three cities in the question above\n')
            continue
        else:
            break
        # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('\nPlease enter a month (January - June) or all for total available months\n').lower()
        except:
            #Exception Error Handling
            print('\nSorry, that input isn\'t valid, please try again\n')
            continue
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            #Incorrect Input Handling
            print('\nPlease enter full month name within the \n')
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('\nPlease enter a day name or all for total available days in the week\n').lower()
        except:
            #Exception Error Handling
            print('\nSorry, that input isn\'t valid, please try again\n')
            continue
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            #Incorrect Input Handling
            print('\nPlease enter a full day name\n')
            continue
        else:
            break
    print('-'*40)
    return (city, month, day)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular hour
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', popular_month)

    # display the most common day of week
    # extract hour from the Start Time column to create an hour column
    df['Weekday'] = df['Start Time'].dt.weekday_name

    # find the most popular hour
    popular_weekday = df['Weekday'].mode()[0]

    print('Most Popular Weekday:', popular_weekday)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_stn = df['Start Station'].mode()[0]

    print('Most Popular Starting Station:', popular_start_stn)

    # display most commonly used end station
    popular_end_stn = df['Start Station'].mode()[0]

    print('Most Popular End Station:', popular_end_stn)

    # display most frequent combination of start station and end station trip
    # create column with combination of Start & End stations
    df['Journey'] = df['Start Station']+' to '+df['End Station']

    # find the most popular journey
    popular_journey = df['Journey'].mode()[0]

    print('Most Popular Journey:', popular_journey)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours, minutes and seconds
    total_travel_time = df['Trip Duration'].sum()
    travel_time_minutes = int(total_travel_time//60)
    travel_time_hours = int(travel_time_minutes//60)
    travel_time_minutes_remainder = int(travel_time_minutes%60)
    travel_time_seconds_remainder = int(total_travel_time%60) #keep as int to avoid decimal points

    #print('Total Travel Time (Seconds):', total_travel_time)
    print('Total Travel Time is {} Hours, {} Minutes and {} Seconds'.
    format(travel_time_hours, travel_time_minutes_remainder, travel_time_seconds_remainder))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Average(Mean) Travel Time (Seconds):', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    #Error checking for city with no gender/birth year data
    if city == 'washington':
        print('No gender or birth year information exists for Washington')
    else:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print(gender)

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        latest_birth_year = df['Birth Year'].max()
        mode_birth_year = df['Birth Year'].mode()[0]
        print('Earliest Birth Year:', earliest_birth_year)
        print('Latest Birth Year:', latest_birth_year)
        print('Most Common Birth Year:', mode_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def correlation_stats(df):
    """Displays correlation statistics on bikeshare users."""

    print('\nCalculating Correlation Stats...\n')
    start_time = time.time()

    # Display correlation statistics of dataframe
    print('\nHere are the correlation statistics of the filtered dataframe\n')
    print(df.corr())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def not_a_number_stats(df):
    """Displays not a number information on bikeshare users dataframe"""

    print('\nCalculating Not a Number Stats...\n')
    start_time = time.time()

    # Display correlation statistics of dataframe
    print('\nHere are the volume of missing values (NaN) in the dataframe\n')
    print('The total volume of missing values is:', df.isnull().sum().sum())
    print('The volume of missing values by column is:\n', df.isnull().sum())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """Displays not a number information on bikeshare users dataframe"""


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        #correlation_stats(df) #Removed as there were not enough float values
        not_a_number_stats(df)

        #Create loop to print first 5 rows of raw data
        sample_raw_data = input('\nWould you like view 5 rows of the raw data? Enter yes or no.\n')
        if sample_raw_data.lower() != 'yes':
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        elif sample_raw_data.lower() == 'yes':
            print(df.head())
            #Create loop to print subseqent raw data in iterations of 5 as long as requested
            rows = 10
            while input('\nWould you like view 5 more rows of the raw data? Enter yes or no.\n').lower() == 'yes':
                print(df.head(rows))
                rows += 5

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
    main()

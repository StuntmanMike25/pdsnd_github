import time
import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': "chicago.csv",
              'new york city': "new_york_city.csv",
              'washington': "washington.csv" }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

month = 'all'

def city_choice():
    """
    Asks the user to give input on what city should be analysed. Returns the user to the original question if invalid input is given.

    Returns:
        (str) city - name of the individual city to analyze, or "all" to combine the data for all cities
    """
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?...or all of them? ").lower()
        if city in ['ny', 'new york', 'newyork']:
            city = 'new york city'
        
        if city in CITY_DATA:
            print("Cool, let's see some bikeshare data for {}!.".format(city.title()))
            return city
        elif city in ['all', 'all of it', 'all of them']:
            city = 'all'
            print("Huh, you want it all? Ok, you will see what comes at you...")
            return city
        else:
            print("Oh, it looks like you haven't entered one of the three cities. Try again...")

def filter_choice():
    """
    Asks the user to give input on what months and days should be included in the analysis. Returns the user to the original question if invalid input is given.
    
    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter    
    """
    while True:
        choice_filter = input("Would you like to filter the data by month, day, or not at all? ").lower()
        if choice_filter in ['month', 'day', 'not at all', 'no filter', 'none of the above', 'no filter at all']:
            break
        else:
            print("Hmm, this input is unclear. Let's try again...")
    if choice_filter == 'month':
        day = 'all'
        while True:
            month = input("Which month would you like to see? - January, February, March, April, May, or June? ").lower()
            if month in months:
                print("Great! Let's see what {} has to offer for us.".format(month.title()))
                return month, day
            else:
                month = input("Hmm, it looks like you haven't typed in one of the selected months. Try again...")
    elif choice_filter == 'day':
        month = 'all'
        while True:
            day = input("Which day are you interested in? - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()
            if day in days:
                print("Cool, we will have a look at the data specifically for {}.".format(day.title()))
                return month, day
            else:
                day = input("Hmm, it looks like you haven/'t typed in one of the days. Try again...")
    elif choice_filter == 'not at all' or 'no filter' or 'none of the above' or 'no filter at all':
        month = 'all'
        day = 'all'
        return month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the individual city to analyze, or "all" to combine the data for all cities
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    if city in CITY_DATA:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday
        df['hour'] = df['Start Time'].dt.hour
        if city != 'washington':
            df['max age'] = 2017 - df['Birth Year'] #based on time of bike rental. Is only the maximum age, because specific date of birth is not available.

    elif city == 'all':
        df1 = pd.read_csv(CITY_DATA['chicago'])
        df2 = pd.read_csv(CITY_DATA['new york city'])
        df3 = pd.read_csv(CITY_DATA['washington'])
        df = pd.concat([df1, df2, df3], ignore_index=True, sort=False) 
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday
        df['hour'] = df['Start Time'].dt.hour
        df['max age'] = 2017 - df['Birth Year'] #based on time of bike rental. Is only the maximum age, because specific date of birth is not available.

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1    
        df = df[df['month'] == month]

    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)

        df = df[df['day_of_week'] == day]
        
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
    (dataframe) df - dataframe as base for analysis, derived from load_data

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    most_common_month = months[df['month'].value_counts().index[0] -1]
    print("The most common month for bikeshares is {}.".format(most_common_month.title()))

    # display the most common day of week

    most_common_day = days[df['day_of_week'].value_counts().index[0]]
    print("The most common day for bikeshares is {}.".format(most_common_day.title()))

    # display the most common start hour

    most_common_hour = df['hour'].value_counts().index[0]
    print("The most common hour for bikeshares is hour {}.".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 

def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
    (dataframe) df - dataframe as base for analysis, derived from load_data

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    max_start_station = df['Start Station'].value_counts().index[0]
    print(f"The most common starting station is {max_start_station}.")

    # display most commonly used end station
    max_end_station = df['End Station'].value_counts().index[0]
    print(f"The most common end station is {max_end_station}.")


    # display most frequent combination of start station and end station trip
    df_station_combo = df.groupby(['Start Station', 'End Station']).count().reset_index().sort_values(['Unnamed: 0'], ascending=False)
    most_common_station_combo = [df_station_combo.iat[0, 0], df_station_combo.iat[0, 1]]
    print(f"The most frequent combination of start and end station is {most_common_station_combo[0]} and {most_common_station_combo[1]}.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
    (dataframe) df - dataframe as base for analysis, derived from load_data
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print(f"The total travel time is {total_duration} seconds...thats {total_duration // 60} minutes or over {total_duration // (60*24)} days.")

    # display mean travel time
    avg_duration = round(df['Trip Duration'].mean(), 2)
    print("How long do people rent a bike on average? Thats {} seconds or {} minutes - in both cases rounded.".format(avg_duration, avg_duration//60))

    # display some extra stats
    median_duration = round(df['Trip Duration'].median(), 2)
    print("Hmm, maybe there are some extreme values skewing the data...how about the median duration?")
    print("The rounded median for the duration is {} seconds and {} minutes.".format(median_duration, median_duration//60))
    shortest_trip = int(df['Trip Duration'].min())
    longest_trip = int(df['Trip Duration'].max())
    print("...and the shortest trip was only {} seconds, while the longest trip was {} seconds or {} minutes.".format(shortest_trip, longest_trip, longest_trip//60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
    (dataframe) df - dataframe as base for analysis, derived from load_data
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(f"There are {user_type_count.get('Subscriber')} subscribers.")
    print(f"There are {user_type_count.get('Customer')} customers.")
    print(f"And there are {user_type_count.get('Dependent')} dependents.")

    # Display earliest, most recent, and most common year of birth + some additional stats about age

    try:
        earliest_year = df['Birth Year'].min()
        print(f"The earliest year of birth is {earliest_year}.")
        most_recent_year = df['Birth Year'].max()
        print(f"The earliest year of birth is {most_recent_year}.")
        most_common_year = df['Birth Year'].mode()
        print(f"The most common year of birth is {most_common_year}.")
        avg_max_age = int(df['max age'].mean())
        corr_age_dur = round(df['max age'].corr(df['Trip Duration']), 2)
        print(f"On average, a user is between {avg_max_age -1} and {avg_max_age} old.")
        print(f"Are age and trip duration actually correlated? Lets see...")
        print(f"The correlation is {corr_age_dur}. That means...")
        if corr_age_dur > 0.6:
            print("People with higher age definitely take longer trips on average!")
        elif corr_age_dur < 0.6 and corr_age_dur > 0.2:
            print("For people with higher age, there is a tendency to take longer trips on average.")
        elif corr_age_dur < 0.2 and corr_age_dur > -0.2:
            print("That's not much of a correlation at all.")
        elif corr_age_dur > -0.6 and corr_age_dur < -0.2:
            print("For people with lower age, there is a tendency to take longer trips on average.")
        elif corr_age_dur < -0.6:
            print("People with lower age definitely take longer trips on average!")
        print('-'*20)
    except KeyError:
        print("With Washington, there is no data available on birth year. Try one of the other cities or all of them to get more stats.")
        
    # Display counts of gender + some extra stats
    try:
        male_count = df['Gender'].value_counts().get('Male')
        print(f"There are {male_count} male users.")
        female_count = df['Gender'].value_counts().get('Female')
        print(f"And there are {female_count} female users.")
        male_percentage = round(((df['Gender'].value_counts().get('Male')) / (df['Gender'].count()) * 100), 2)
        female_percentage = round(((df['Gender'].value_counts().get('Female')) / (df['Gender'].count()) * 100), 2)
        print(f"The ratio is {male_percentage} % male and {female_percentage} % female users.")

        print("Is there actually a correlation between gender and the trip duration? Lets take a look!")
        df_dummy = pd.get_dummies(df['Gender']) #creating a dummy variable to calc correlation between Gender and Trip Duration
        df = pd.concat((df, df_dummy), axis=1) 
        corr_female_dur = round(df['Trip Duration'].corr(df['Female']), 2)
        print(f"The correlation between being female and the trip duration is {corr_female_dur}.")
        if corr_female_dur > 0.1:
            print("That means, that female users take longer trips on average.")
        elif corr_female_dur < -0.1:
            print("That means, that female users take shorter trips on average.")
        elif corr_female_dur < 0.1 and corr_female_dur > -0.1:
            print("That means basically no correlation.")

    except KeyError:
        print("With Washington, there is no data available on birth year. Try one of the other cities or all of them to get more stats.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """Returns raw data in increments if the user asks for it.
    Args:
    (dataframe) df - dataframe as base for analysis, derived from load_data
    """
    while True:
        i = 5
        raw_data_answer = input("Would you like to see some raw data? ").lower()
        if raw_data_answer in ['yes', 'sure', 'of course', 'y']:
            print(df[:i])
            while True:
                wants_more = input("Would you like to see some more raw data? ").lower()
                if wants_more in ['yes', 'sure', 'of course', 'y']:
                    print(df[i:i+5])
                    i += 5
                elif wants_more in ['no', 'nope', 'n']:
                    return
        elif raw_data_answer in ['no', 'nope', 'n']:
            return
        else:
            print("Sorry, the input was not understandable...")


def main():
    """
    Takes the user input, calls the function load_data and shows descriptive statistics about the dataframe. 

    """
    while True:
        city = city_choice()
        month, day = filter_choice()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for using our service! ")
            break

if __name__ == "__main__":
	main()


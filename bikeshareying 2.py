import time
import pandas as pd
import numpy as np
import datetime as dt

# Define the data files for each city
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Arrays for month and day names
months = ['january', 'february', 'march', 'april', 'may', 'june']

weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_city():
    """ Asks the user to specify a city to analyze. """
    while True: 
        city = input("Which city would you like to explore data for: Chicago, New York City, or Washington? ").lower()
        if city in CITY_DATA:
            return city
        else: 
            print("Invalid input. Please enter either 'Chicago', 'New York City', or 'Washington'.")

def get_filter_type():
    """Asks the user to specify the type of filter (month, day, or none)."""
    while True:
        filter_type = input("Would you like to filter the data by month, day, or not at all? Type 'none' for no filter. ").lower()
        if filter_type in ['month', 'day', 'none']:
            return filter_type
        else:
            print("Invalid input. Please enter 'month', 'day', or 'none'.")

def get_month():
    """Asks the user to specify a month to filter by."""
    while True:
        month = input("Which month - January, February, March, April, May, or June? ").lower()
        if month in months:
            return month
        else:
            print("Invalid input. Please enter a valid month.")

def get_day():
    """Asks the user to specify a day of the week to filter by."""
    while True:
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()
        if day in weekdays:
            return day
        else:
            print("Invalid input. Please enter a valid day.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_city()
    filter_type = get_filter_type()
    
    if filter_type == 'month':
        month = get_month()
        day = 'all'
    elif filter_type == 'day':
        month = 'all'
        day = get_day()
    else:
        month = 'all'
        day = 'all'
 
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """Load data for the specified filters of city(ies), month(s) and
       day(s) whenever applicable.

    Args:
        (str or list) city - name of the city(ies) to analyze
        (str or list) month - name of the month(s) to filter
        (str or list) day - name of the day(s) of week to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    start_time = time.time()

    # Load and concatenate data for multiple cities if provided
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)
        # Reorganize DataFrame columns after concatenation
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'])
        except KeyError:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # Create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name().str.lower()
    df['Start Hour'] = df['Start Time'].dt.hour

    # Filter data by month
    if month != 'all':
        if isinstance(month, list):
            df = df[df['Month'].isin([months.index(m) + 1 for m in month])]
        else:
            df = df[df['Month'] == (months.index(month) + 1)]

    # Filter data by weekday
    if day != 'all':
        if isinstance(day, list):
            df = df[df['Weekday'].isin([d.lower() for d in day])]
        else:
            df = df[df['Weekday'] == day.lower()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df

def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    
    print('\nDisplaying the statistics on the most frequent times of travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Month'].mode()[0]
    print('The month with the most travels is: ' + str(months[most_common_month-1]).title() + '.')

    # Display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('The most common day of the week is: ' + str(most_common_day).title() + '.')

    # Display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' + str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station is: ' + str(common_start_station) + '.')

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station is: ' + str(common_end_station) + '.')

    # Display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['route'].mode()[0]
    print('Most Common Trip is: ' + str(common_trip) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in both formats
    total_seconds = df['Trip Duration'].sum()
    total_time_str = str(dt.timedelta(seconds=int(total_seconds)))
    total_time_detail = (str(int(total_seconds // 86400)) + 'd ' +
                        str(int((total_seconds % 86400) // 3600)) + 'h ' +
                        str(int(((total_seconds % 86400) % 3600) // 60)) + 'm ' +
                        str(int(((total_seconds % 86400) % 3600) % 60)) + 's')
    
    print('The total travel time is: ' + total_time_str)
    print('Details: ' + total_time_detail)
    
    # Display mean travel time in both formats
    mean_seconds = df['Trip Duration'].mean()
    mean_time_str = str(dt.timedelta(seconds=int(mean_seconds)))
    mean_time_detail = (str(int(mean_seconds // 60)) + 'm ' +
                        str(int(mean_seconds % 60)) + 's')

    print('The mean travel time is: ' + mean_time_str)
    print('Details: ' + mean_time_detail)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    try:
        # Display counts of gender  
        gender_counts = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts)
    except KeyError:
        print('\nGender data not available.')

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("The oldest person to ride one bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max())) 
        print("The youngest person to ride one bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("The most common birth year amongst riders is: " + most_common_birth_year)
    except KeyError:
        print("We're sorry! There is no data of birth year.")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

def popular_routes_by_user_type(df):
    """Displays the most popular routes taken by different user types (subscriber vs. customer)."""
    print('\nCalculating Popular Routes by User Type...\n')
    start_time = time.time()

    try:
        user_types = df['User Type'].unique()
        for user_type in user_types:
            user_type_df = df[df['User Type'] == user_type]
            user_type_df['route'] = user_type_df['Start Station'] + ' to ' + user_type_df['End Station']
            common_route = user_type_df['route'].mode()[0]
            print(f'Most Common Route for {user_type}: {common_route}')
    except KeyError:
        print('User Type data not available.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)
    
def raw_data(df, mark_place):
    """Display 5 lines of sorted raw data each time."""
    print("\nYou opted to view raw data.")

    # This variable holds where the user last stopped
    if mark_place > 0:
        last_place = input("\nWould you like to continue from where you stopped last time? [y/n]: ").lower()
        if last_place == 'n':
            mark_place = 0

    # Sort data by column
    if mark_place == 0:
        sort_df = input("\nHow would you like to sort the way the data is displayed in the dataframe? Hit Enter to view unsorted.\n [st] Start Time\n [et] End Time\n [td] Trip Duration\n [ss] Start Station\n [es] End Station\n\n>").lower()
        asc_or_desc = input("\nWould you like it to be sorted ascending or descending? [a] Ascending\n [d] Descending\n\n>").lower()

        if asc_or_desc == 'a':
            asc_or_desc = True
        elif asc_or_desc == 'd':
            asc_or_desc = False

        if sort_df == 'st':
            df = df.sort_values(['Start Time'], ascending=asc_or_desc)
        elif sort_df == 'et':
            df = df.sort_values(['End Time'], ascending=asc_or_desc)
        elif sort_df == 'td':
            df = df.sort_values(['Trip Duration'], ascending=asc_or_desc)
        elif sort_df == 'ss':
            df = df.sort_values(['Start Station'], ascending=asc_or_desc)
        elif sort_df == 'es':
            df = df.sort_values(['End Station'], ascending=asc_or_desc)
        elif sort_df == '':
            pass

    # Each loop displays 5 lines of raw data
    while True:
        for i in range(mark_place, len(df.index), 5):
            print("\n", df.iloc[mark_place:mark_place+5].to_string(), "\n")
            mark_place += 5
            if input("Do you want to keep printing raw data? [y/n]: ").lower() != 'y':
                break
        break

    return mark_place

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        mark_place = 0
        while True:
            print("\nPlease select the information you would like to obtain:\n")
            print("[ts] Time Stats\n[ss] Station Stats\n[tds] Trip Duration Stats\n[us] User Stats\n[pr] Popular Routes by User Type\n[rd] Display Raw Data\n[r] Restart\n")

            select_data = input("Enter your choice: ").lower()
            
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df)
            elif select_data == 'pr':
                popular_routes_by_user_type(df)
            elif select_data == 'rd':
                mark_place = raw_data(df, mark_place)
            elif select_data == 'r':
                break
            else:
                print("Invalid input. Please enter a valid option.")

        restart = input('\nWould you like to restart? Enter yes or no: ').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()


# calgary_dogs.py
# Author: Maheesha_Munasinghe

# This program analyzes dog breed statistics from the Calgary Dog Breeds dataset.
# Users can enter a breed name and see various statistics about it.
# Docstrings and comments are included throughout the code for clarity.


import pandas as pd

def main():
    """
    The main function that orchestrates the program execution.
    It reads the data, gets user input, and calculates breed statistics.
    """
    # Stage 1: DataFrame creation
    # Load data from the Excel file (replace 'CalgaryDogBreeds.xlsx' with your actual file path)
    file_path = 'CalgaryDogBreeds.xlsx'
    df = pd.read_excel(file_path)

    # Set and sort multi-index for easier data access
    df.set_index(['Breed', 'Year', 'Month'], inplace=True)
    df.sort_index(inplace=True)

    print("\nENSF 692 Dogs of Calgary")

    # Stage 2: User input
    user_input = capture_user_input(df)

    # Stage 3: Data analysis
    perform_data_analysis(df, user_input)

def capture_user_input(df):
    """
    Prompts the user to enter a dog breed and validates the input.

    Parameter:
        df (pd.DataFrame): The DataFrame containing the Excel data.

    Return:
        str: The validated dog breed input by the user in uppercase.
    """
    while True:
        try:
            # Request the user to enter a dog breed
            user_input = input("Enter a dog breed: ").upper()
            # Validate if the breed exists in the DataFrame index
            if user_input in df.index.get_level_values('Breed'):
                return user_input
            else:
                raise KeyError
        except KeyError:
            print("The entered dog breed is not found in the data. Please try again.")

def perform_data_analysis(df, breed):
    """
    Computes and displays statistics for the specified dog breed.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the Excel data.
        breed (str): The dog breed input by the user.

    Return:
        None
    """
    # Filter the DataFrame for the selected breed
    breed_data = df.loc[breed]

    # 1. Identify all the years in which the breed appears
    years = breed_data.index.get_level_values('Year').unique()
    print(f"The {breed} appears in the top breeds for the following years: {', '.join(map(str, years))}.")

    # 2. Calculate the total number of registrations for the selected breed
    total_registrations = breed_data['Total'].sum()
    print(f"A total of {total_registrations} {breed} dogs have been registered.")

    # 3. Determine the breed's registration percentage for each year
    for year in [2021, 2022, 2023]:
        yearly_data = df.xs(year, level='Year')
        total_dogs_yearly = yearly_data['Total'].sum()
        breed_dogs_yearly = breed_data.xs(year, level='Year')['Total'].sum() if year in years else 0
        breed_percentage_yearly = round((breed_dogs_yearly / total_dogs_yearly) * 100, 6) if total_dogs_yearly else 0
        print(f"In {year}, {breed} accounted for {breed_percentage_yearly}% of the top breeds.")

    # 4. Calculate the breed's registration percentage across all years
    total_dogs_all_years = df['Total'].sum()
    overall_breed_percentage = round((total_registrations / total_dogs_all_years) * 100, 6)
    print(f"Across all years, {breed} represented {overall_breed_percentage}% of the top breeds.")

    # 5. Identify the most popular months for the selected breed
    monthly_registrations = breed_data.groupby('Month')['Total'].sum()
    mean_registrations = monthly_registrations.mean()
    peak_months = monthly_registrations[monthly_registrations >= mean_registrations].index.tolist()
    print(f"The most popular month(s) for {breed} dogs are: {', '.join(peak_months)}")

if __name__ == '__main__':
    main()

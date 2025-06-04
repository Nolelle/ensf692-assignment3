# school_data.py
# Edmund Yu
#
# A terminal-based application for computing and printing statistics based on given input.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc.
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import numpy as np

from given_data import (year_2013, year_2014, year_2015, year_2016, year_2017,
                        year_2018, year_2019, year_2020, year_2021, year_2022)

# Declare any global variables needed to store the data here
all_year_arrays = [year_2013, year_2014, year_2015, year_2016, year_2017,
                   year_2018, year_2019, year_2020, year_2021, year_2022]

# [10,60] 10 years (20x3) (20 schools 3 grades)
stack_all_year_arrays = np.stack(all_year_arrays)
# reshape to third dimension 10 years, 20 schools, 3 grades
threeD_stack_array = stack_all_year_arrays.reshape((10, 20, 3))

school_dict = {
    1224: "Centennial High School",
    1679: "Robert Thirsk School",
    9626: "Louise Dean School",
    9806: "Queen Elizabeth High School",
    9813: "Forest Lawn High School",
    9815: "Crescent Heights High School",
    9816: "Western Canada High School",
    9823: "Central Memorial High School",
    9825: "James Fowler High School",
    9826: "Ernest Manning High School",
    9829: "William Aberhart High School",
    9830: "National Sport School",
    9836: "Henry Wise Wood High School",
    9847: "Bowness High School",
    9850: "Lord Beaverbrook High School",
    9856: "Jack James High School",
    9857: "Sir Winston Churchill High School",
    9858: "Dr. E. P. Scarlett High School",
    9860: "John G Diefenbaker High School",
    9865: "Lester B. Pearson High School"
}


# You may add your own additional classes, functions, variables, etc.
def validate_school_input(input, dict):
    """
    Validates user input for a school name or code against known school data.

    Args:
        input (str): The raw input string from the user.
        dict (dict): Dictionary mapping school codes to school names.

    Returns:
        int: The valid school code if found.

    Raises:
        ValueError: If the input does not correspond to a valid school.
    """
    processed_input = input.strip()

    # check for valid school code
    try:
        school_code = int(processed_input)
        if school_code in school_dict:
            return school_code

    except ValueError:
        pass

    # check for valid school name
    for code, name in school_dict.items():
        if name.lower() == processed_input.lower():
            return code
    raise ValueError("You must enter a valid school name or school code.")


def generate_school_stats(school_code, dict):
    """
    Generates and prints comprehensive enrollment statistics for a specific school.

    Args:
        school_code (int): The numeric code identifying the school.
        dict (dict): Dictionary mapping school codes to school names.

    Returns:
        None: Prints statistics directly to console.
    """
    # Generate mean enrollment data.

    # Index of school code of second dimension of 3d array maps to first school in dict
    school_codes = list(school_dict.keys())
    school_index = school_codes.index(school_code)

    school_data = threeD_stack_array[:, school_index, :].view()  # [10,3]

    mean_grade_10 = int(np.floor(np.nanmean(school_data[:, 0])))
    mean_grade_11 = int(np.floor(np.nanmean(school_data[:, 1])))
    mean_grade_12 = int(np.floor(np.nanmean(school_data[:, 2])))

    highest_enrollment = int(np.floor(np.nanmax(school_data)))
    lowest_enrollment = int(np.floor(np.nanmin(school_data)))

    yearly_totals = []
    total_ten_year = 0

    print(f"Mean enrollment for Grade 10: {mean_grade_10} ")
    print(f"Mean enrollment for Grade 11: {mean_grade_11} ")
    print(f"Mean enrollment for Grade 12: {mean_grade_12} ")
    print(f"Highest enrolllment for a single grade: {highest_enrollment}")
    print(f"Lowest enrolllment for a single grade: {lowest_enrollment}")

    for year in range(10):
        year_total = int(np.floor(np.nansum(school_data[year, :])))
        yearly_totals.append(year_total)
        total_ten_year += year_total
        print(f"Total enrollment for {2013 + year}: {year_total}")

    print(f"Total ten year enrollment: {total_ten_year}")

    mean_ten_year_total = int(np.floor(total_ten_year / 10))
    print(f"Mean total enrollment over 10 years: {mean_ten_year_total}")

    over_500_mask = school_data > 500
    over_500_values = school_data[over_500_mask]
    if len(over_500_values):
        median_over_500 = int(np.floor(np.median(over_500_values)))
        print(
            f"For all enrollments over 500, the median values was: {median_over_500}")
    else:
        print("No enrollments over 500.")


def generate_all_stats():
    """
    Generates and prints general statistics for all schools across all years.

    Returns:
        None: Prints statistics directly to console.
    """
    # (first year, index 0)
    mean_2013 = int(np.floor(np.nanmean(threeD_stack_array[0, :, :])))

    # (last year, index 9)
    mean_2022 = int(np.floor(np.nanmean(threeD_stack_array[9, :, :])))

    # (Grade 12 in 2022)
    graduating_2022 = int(np.floor(np.nansum(threeD_stack_array[9, :, 2])))

    highest_single_grade = int(np.floor(np.nanmax(threeD_stack_array)))
    lowest_single_grade = int(np.floor(np.nanmin(threeD_stack_array)))

    print(f"Mean enrollment in 2013: {mean_2013}")
    print(f"Mean enrollment in 2022: {mean_2022}")
    print(f"Total graduating class of 2022: {graduating_2022}")
    print(f"Highest enrollment for a single grade: {highest_single_grade}")
    print(f"Lowest enrollment for a single grade: {lowest_single_grade}")


def main():
    """
    Main function that orchestrates the school enrollment statistics program.

    Displays array information, prompts for user input, validates the input,
    and generates both school-specific and general statistics.

    Returns:
        None: Prints results directly to console.
    """
    print("ENSF 692 School Enrollment Statistics")

    # Print Stage 1 requirements here
    print(f"Shape of full data array: {threeD_stack_array.shape}")
    print(f"Dimensions of full data array: {threeD_stack_array.ndim}")

    # Prompt for user input
    selected_valid_school = None

    while selected_valid_school is None:
        try:
            user_input = input(
                "Please enter the high school name or school code: ")
            selected_valid_school = validate_school_input(
                user_input, school_dict)
        except ValueError as e:
            print("You must enter a valid school name or code.")

    # Print Stage 2 requirements here
    print("\n***Requested School Statistics***\n")
    print(
        f"School Name: {school_dict[selected_valid_school]}, School Code: {selected_valid_school}")
    generate_school_stats(selected_valid_school, school_dict)

    # Print Stage 3 requirements here
    print("\n***General Statistics for All Schools***\n")

    generate_all_stats()


if __name__ == '__main__':
    main()

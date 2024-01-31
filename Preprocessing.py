import os
import tkinter as tk
from tkinter import simpledialog
import numpy as np
import pandas as pd

class SolarDataPreProcessing:
    def __init__(self) -> None:
        # Initialize attributes for storing input paths
        self.text_file_path = None
        self.output_directory = None

    def get_input_paths(self):
        # Use tkinter to create a dialogue box to get input paths
        self.text_file_path = simpledialog.askstring("Input", "Enter text file path:")
        self.output_directory = simpledialog.askstring("Input", "Enter output directory path:")

    def text_to_csv(self):
        # Check if input paths are set
        if self.text_file_path is None or self.output_directory is None:
            raise ValueError("Input paths are not set. Call get_input_paths() first.")

        # Read data from the specified text file
        with open(self.text_file_path) as data:
            solar_data = data.read()
        
        # Extract relevant data starting from "DATA_COLUMNS"
        data_lines = solar_data.splitlines()
        for i in range(0, len(data_lines) - 1):
            if "DATA_COLUMNS" in data_lines[i]:
                starting_index = i
                break
        updated_data = data_lines[starting_index:]
        updated_data[0] = updated_data[0].split(" : ")[1]
        
        # Clean the data
        for lines in updated_data:
            if len(lines) == 1:
                updated_data.remove(lines)
                break
        for i in range(len(updated_data)):
            if i > 0:
                updated_data[i] = updated_data[i].split()
        
        # Create output directory if it doesn't exist
        if self.output_directory not in os.listdir():
            os.makedirs(self.output_directory)
        
        # Write cleaned data to a CSV file
        with open(f"{self.output_directory}/data.csv", "w") as f:
            count = 0
            for line in updated_data:
                count += 1
                if count == 1:
                    f.write(line)
                else:
                    f.write(",".join(line) + "\n")
        
        return f"{self.output_directory}/data.csv"
    
    def dataframe(self):
        # Check if the output directory is set
        if self.output_directory is None:
            raise ValueError("Output directory is not set. Call get_input_paths() first.")

        # Read CSV file into a DataFrame
        csv_file_path = f"{self.output_directory}/data.csv"
        data = pd.read_csv(csv_file_path)
        df = pd.DataFrame(data)
        return df

if __name__ == "__main__":
    # Create an instance of SolarDataPreProcessing
    pre_processing = SolarDataPreProcessing()

    # Get input paths from the user using a dialogue box
    pre_processing.get_input_paths()

    # Perform text to CSV conversion
    csv_data = pre_processing.text_to_csv()

    # Create a dataframe from the CSV data
    data = pre_processing.dataframe()
    print(data.head())
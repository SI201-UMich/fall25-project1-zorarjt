# Name: Zora Tucker
# Student ID: 28071696
# Email: zrtucker@umich.edu
# Worked Alone
# GenAI Use: Used ChatGPT to generate test case ideas and plain-English descriptions of functions to implement
# Also used for percentages and temperature formatting

import unittest
import os
import csv

csv_file = "crop_yield.csv"

# only take region, crop, and temperature_celcius columns
def load_crop_data(csv_file):
    pass

def get_crop_data(crops):
    pass

# What percentage of rice is grown in the South?
def calculate_rice_percentage(crops_entries):
    pass

# What is the average temperature (°C) that Maize was grown in?
def calculate_average_temperature(crop_entries):
    pass

# prints to text file
def generate_report(rice_percentage, avg_temp):
    pass


# Test Functions

class TestCropData(unittest.TestCase):
    def setUp(self):
        with open("crop_data.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Region", "Crop", "Temperature_Celsius"])
            writer.writerow(["North", "Rice", "25.0"])
            writer.writerow(["South", "Rice", "0"])
            writer.writerow(["East", "Maize", "NA"])
            writer.writerow(["West", "Wheat", "15.0"])
            writer.writerow(["South", "Maize", "28.0"])
            writer.writerow(["South", "Maize", "NA"])

    def test_load_crop_data_valid_file(self):
        crops = load_crop_data("crop_data.csv")
        self.assertEqual(len(crops), 6)
        self.assertEqual(crops[0], {"Region": "North", "Crop": "Rice", "Temperature_Celsius": "25.0"})
        self.assertEqual(crops[1], {"Region": "South", "Crop": "Rice", "Temperature_Celsius": "0"})
    def test_load_crop_data_invalid_temperature(self):
        crops = load_crop_data("crop_data.csv")
        temps = [entry['Temperature_Celsius'] for entry in crops]
        self.assertNotIn("NA", temps)
        self.assertTrue(all(isinstance(t, float) for t in temps))
    def test_load_crop_data_file_not_found(self):
        self.assertIsNone(load_crop_data("missing_file.csv"))
    def test_load_crop_data_empty_file(self):
        with open("empty.csv", mode="w") as file:
            file.write("")
        crops = load_crop_data("empty.csv")
        self.assertEqual(crops, [])
        os.remove("empty.csv")
    
    def test_get_crop_data_valid(self):
        crops = load_crop_data("crop_data.csv")
        data = get_crop_data(crops)
        self.assertEqual(len(data['Region']), len(crops)) 
    def test_get_crop_data_fields(self):
        crops = load_crop_data("crop_data.csv")
        data = get_crop_data(crops)
        for key in ['Region', 'Crop', 'Temperature_Celsius']:
            self.assertIn(key, data)
    def test_get_crop_data_empty(self):
        result = get_crop_data([])
        self.assertEqual(result, {'Region': [], 'Crop': [], 'Temperature_Celsius': []})
    def test_crop_data_none(self):
        self.assertIsNone(get_crop_data(None))
    
    def test_calculate_rice_percentage_norm(self):
        crops = load_crop_data("crop_data.csv")
        result = calculate_rice_percentage(crops)
        self.assertEqual(result, "50.0%")
    def test_calculate_rice_percentage_no_rice(self):
        crops = [{'Region': 'West', 'Crop': 'Wheat', 'Temperature_Celsius': 15.0}]
        result = calculate_rice_percentage(crops)
        self.assertEqual(result, "0.0%")
    def test_calculate_rice_percentage_all_south(self):
        crops = [
            {'Region': 'South', 'Crop': 'Rice', 'Temperature_Celsius': 27.0},
            {'Region': 'South', 'Crop': 'Rice', 'Temperature_Celsius': 28.0}
        ]
        result = calculate_rice_percentage(crops)
        self.assertEqual(result, "100.0%")

    def test_caculate_average_temperature_norm(self):
        crops = load_crop_data("crop_data.csv")
        result = calculate_average_temperature(crops)
        self.assertEqual(result, "28.0°C")
    def test_calculate_average_temperature_no_maize(self):
        crops = [{'Region': 'North', 'Crop': 'Rice', 'Temperature_Celsius': 25.0}]
        result = calculate_average_temperature(crops)
        self.assertEqual(result, "0.0°C")
    def test_calculate_average_temperature_empty(self):
        result = calculate_average_temperature([])
        self.assertEqual(result, "0.0°C")
    def test_calculate_average_temperature_multiple_maize(self):
        crops = [
            {'Region': 'South', 'Crop': 'Maize', 'Temperature_Celsius': 30.0},
            {'Region': 'East', 'Crop': 'Maize', 'Temperature_Celsius': 20.0},
            {'Region': 'West', 'Crop': 'Wheat', 'Temperature_Celsius': 15.0}
        ]
        result = calculate_average_temperature(crops)
        self.assertEqual(result, "25.0°C")
    def test_calculate_average_temperature_invalid_temp(self):
        crops = [
            {'Region': 'South', 'Crop': 'Maize', 'Temperature_Celsius': 'NA'},
            {'Region': 'East', 'Crop': 'Maize', 'Temperature_Celsius': 20.0}
        ]
        result = calculate_average_temperature(crops)
        self.assertEqual(result, "20.0°C")
    
    def test_generate_report_file_creation(self):
        generate_report("50.0%", "28.0°C")
        self.assertTrue(os.path.exists("crop_report.txt"))
        os.remove("crop_report.txt")
    def test_generate_report_content(self):
        generate_report("50.0%", "28.0°C")
        with open("crop_report.txt", "r") as file:
            content = file.read()
            self.assertIn("50.0%", content)
            self.assertIn("28.0°C", content)
        os.remove("crop_report.txt")
    def test_generate_report_empty_values(self):
        generate_report("0.0%", "0.0°C")
        with open("crop_report.txt", "r") as file:
            content = file.read()
            self.assertIn("0.0%", content)
            self.assertIn("0.0°C", content)
        os.remove("crop_report.txt")
    def test_generate_report_overwrite(self):
        generate_report("50.0%", "28.0°C")
        generate_report("75.0%", "30.0°C")
        with open("crop_report.txt", "r") as file:
            content = file.read()
            self.assertIn("75.0%", content)
            self.assertIn("30.0°C", content)
            self.assertNotIn("50.0%", content)
            self.assertNotIn("28.0°C", content)
        os.remove("crop_report.txt")

#def main():
    #unittest.main()
#if __name__ == "__main__":
    #main()
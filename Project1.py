# Name: Zora Tucker
# Student ID: 28071696
# Email: zrtucker@umich.edu
# Worked Alone
# GenAI Use: Used ChatGPT to generate test case ideas and plain-English descriptions of functions to implement
# Also used for percentages and temperature formatting & debugging of type/value errors

import unittest
import os
import csv

csv_file = "crop_yield.csv"

# only take region, crop, and temperature_celcius columns
def load_crop_data(csv_file):
    if not os.path.exists(csv_file):
        return None
    with open(csv_file, 'r') as file:
        lines = file.readlines()
    crops = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            region = row.get('Region', '').strip()
            crop = row.get('Crop', '').strip()
            temp_str = row.get('Temperature_Celsius', '').strip()

            if not region or not crop or not temp_str:
                continue

            try:
                temp = float(temp_str)
            except ValueError:
                continue

            crops.append({
                'Region': region,
                'Crop': crop,
                'Temperature_Celsius': temp
            })
    return crops

def get_crop_data(crops):
    if not crops:
        return {'Region': [], 'Crop': [], 'Temperature_Celsius': []}
    crop_entries = {'Region': [], 'Crop': [], 'Temperature_Celsius': []}
    for entry in crops:
        crop_entries['Region'].append(entry['Region'])
        crop_entries['Crop'].append(entry['Crop'])
        crop_entries['Temperature_Celsius'].append(entry['Temperature_Celsius'])
    return crop_entries

# What percentage of rice is grown in the South?
def calculate_rice_percentage(crops_entries):
    if not crops_entries:
        return "0.0%"
    
    rice_entries = [i for i in crops_entries if i['Crop'] == 'Rice']

    if not rice_entries:
        return "0.0%"
    
    south_rice_valid_temp = sum(
        1 for i in rice_entries 
        if i['Region'] == 'South' and i['Temperature_Celsius'] > 0
    )
    rice_percentage = (south_rice_valid_temp / len(rice_entries)) * 100
    return f"{rice_percentage:.1f}%"
    

# What is the average temperature (°C) that Maize was grown in?
def calculate_average_temperature(crop_entries):
    if not crop_entries:
        return "0.0°C"
    
    maize_entries = [
        i for i in crop_entries
        if i['Crop'] == 'Maize' and i['Region'] == 'South'
    ]
    
    if not maize_entries:
        return "0.0°C"
    
    total_temp = 0.0
    count = 0
    
    for entry in maize_entries:
        temp = entry['Temperature_Celsius']
        try:
            temp = float(temp)
        except (ValueError, TypeError):
            continue
        total_temp += temp
        count += 1

    if count == 0:
        return "0.0°C"

    average_temp = total_temp / count
    return f"{average_temp:.1f}°C"

# prints to text file
def generate_report(rice_percentage, avg_temp):
    report = f"Rice is grown in the South {rice_percentage} of the time.\n"
    report += f"The average temperature for growing Maize is {avg_temp}.\n"
    
    with open("crop_report.txt", "w") as file:
        file.write(report)


# Test Functions

class TestCropData(unittest.TestCase):
    def setUp(self):
        with open("crop_sample.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Region", "Crop", "Temperature_Celsius"])
            writer.writerow(["North", "Rice", "25.0"])
            writer.writerow(["South", "Rice", "0"])
            writer.writerow(["East", "Maize", "NA"])
            writer.writerow(["West", "Wheat", "15.0"])
            writer.writerow(["South", "Maize", "28.0"])
            writer.writerow(["South", "Maize", "NA"])

    def test_load_crop_data_valid_file(self):
        crops = load_crop_data("crop_sample.csv")
        self.assertEqual(len(crops), 4)
        self.assertEqual(crops[0], {"Region": "North", "Crop": "Rice", "Temperature_Celsius": 25.0})
        self.assertEqual(crops[1], {"Region": "South", "Crop": "Rice", "Temperature_Celsius": 0.0})
    def test_load_crop_data_invalid_temperature(self):
        crops = load_crop_data("crop_sample.csv")
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
        crops = load_crop_data("crop_sample.csv")
        data = get_crop_data(crops)
        self.assertEqual(len(data['Region']), len(crops)) 
    def test_get_crop_data_fields(self):
        crops = load_crop_data("crop_sample.csv")
        data = get_crop_data(crops)
        for key in ['Region', 'Crop', 'Temperature_Celsius']:
            self.assertIn(key, data)
    def test_get_crop_data_empty(self):
        result = get_crop_data([])
        self.assertEqual(result, {'Region': [], 'Crop': [], 'Temperature_Celsius': []})
    def test_crop_data_none(self):
        self.assertEqual(get_crop_data(None), {'Region': [], 'Crop': [], 'Temperature_Celsius': []})
    
    def test_calculate_rice_percentage_norm(self):
        crops = load_crop_data("crop_sample.csv")
        result = calculate_rice_percentage(crops)
        self.assertEqual(result, "0.0%")
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
        crops = load_crop_data("crop_sample.csv")
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
        self.assertEqual(result, "30.0°C")
    def test_calculate_average_temperature_invalid_temp(self):
        crops = [
            {'Region': 'South', 'Crop': 'Maize', 'Temperature_Celsius': 'NA'},
            {'Region': 'East', 'Crop': 'Maize', 'Temperature_Celsius': 20.0}
        ]
        result = calculate_average_temperature(crops)
        self.assertEqual(result, "0.0°C")
    
def main():
    unittest.main()

if __name__ == "__main__":
    main()
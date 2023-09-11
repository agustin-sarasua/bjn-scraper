import calendar
from datetime import datetime
import os
import re

def clean_filename(filename):
    # Remove special characters and replace spaces with underscores
    cleaned_filename = re.sub(r'[^\w\s.-]', '', filename)
    cleaned_filename = cleaned_filename.replace(' ', '_')
    return cleaned_filename

def generate_unique_filename(date, type_text, court_number, court_name):
    cleaned_date = date.replace('/', '_')
    cleaned_type_text = type_text.replace(' ', '_').lower()
    cleaned_court_number = court_number.replace('/', '_')
    cleaned_court_name = clean_filename(court_name.replace(' ', '_').lower())

    # timestamp = int(datetime.timestamp(datetime.now()))
    unique_filename = f"{cleaned_date}_{cleaned_type_text}_{cleaned_court_number}_{cleaned_court_name}.html"
    return unique_filename

def create_date_directory(start_date, end_date):
    start_date_parts = start_date.split('/')
    end_date_parts = end_date.split('/')
    
    start_day, start_month, start_year = start_date_parts[0], start_date_parts[1], start_date_parts[2]
    end_day, end_month, end_year = end_date_parts[0], end_date_parts[1], end_date_parts[2]
    
    directory_name = f"data/{start_day}_{start_month}_{start_year}__{end_day}_{end_month}_{end_year}"
    
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created.")
    else:
        print(f"Directory '{directory_name}' already exists.")
    
    return directory_name

def get_start_end_days(year, month):
    start_day = 1
    end_day = calendar.monthrange(year, month)[1]
    start_date = f'{start_day:02d}/{month:02d}/{year}'
    end_date = f'{end_day:02d}/{month:02d}/{year}'
    return start_date, end_date
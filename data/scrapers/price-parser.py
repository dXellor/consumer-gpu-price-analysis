import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from bs4 import BeautifulSoup
import re
import json
import os
import pandas as pd
import numpy as np
import time

last_trigger = 0

def parse_chart_data_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    gpu_title = soup.find('title').get_text()
    scripts = soup.find_all('script')
    pattern = re.compile(r'var\s+chart_data\s*=\s*(\[\{.*?\}\]);', re.DOTALL)

    for script in scripts:
        script_text = script.string
        if script_text:
            match = pattern.search(script_text)
            if match:
                json_str = match.group(1)
                chart_data = json.loads(json_str)
                print(f"Extracted chart_data from {file_path}")
                return gpu_title, chart_data

    print(f"No chart_data found in {file_path}")
    return None, None

def populate_csv(gpu:str, chart_data: list):
    gpu_median_prices_per_timestamp_frame = median_price_with_timestamps(gpu, chart_data, pd.to_datetime('2023-10-21'), pd.to_datetime('2025-10-21'))
    gpu_median_prices_per_timestamp_frame.to_csv(f'price_data_dir/{gpu.replace(' ', '_')}.csv', index=True, header=False)

def prepare_label_series(label_data, start_date, end_date):
    df = pd.DataFrame(label_data, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.normalize()
    df = df.set_index('date').sort_index()

    df = df[~df.index.duplicated(keep='first')]

    # Complete date range
    full_range = pd.date_range(start_date, end_date, freq='D')
    df = df.reindex(full_range)

    # Forward fill missing prices
    df['price'] = df['price'].ffill()
    return df['price']

def median_price_with_timestamps(gpu, labels_data, start_date, end_date):
    all_series = []
    for label_dict in labels_data:
        series = prepare_label_series(label_dict['data'], start_date, end_date)
        all_series.append(series)

    combined_df = pd.concat(all_series, axis=1)
    median_prices = combined_df.median(axis=1)

    result_df = median_prices.to_frame(name='median_price')
    result_df['gpu'] = gpu
    result_df.index.name = 'date' 

    return result_df

class HtmlFileEventHandler(FileSystemEventHandler):
    # def on_modified(self, event):
    #     if not event.is_directory and event.src_path.endswith('.html'):
    #         print(f"Detected modification in {event.src_path}")
    #         title, chart_data = parse_chart_data_from_html(event.src_path)
    #         populate_csv(title, chart_data)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.html'):
            print(f"Detected creation of {event.src_path}")
            title, chart_data = parse_chart_data_from_html(event.src_path)
            populate_csv(title, chart_data)


if __name__ == "__main__":
    path = '.'
    event_handler = HtmlFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Monitoring directory {os.path.abspath(path)} for new or modified HTML files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

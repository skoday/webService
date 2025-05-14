import asyncio
import csv
import os
from datetime import datetime

class AsyncCSVLogger:
    def __init__(self, filepath):
        self.filepath = filepath
        self.columns = ['filename', 'timestamp', 'model', 'prompt', 'response']

    async def save_info(self, filename, model, prompt, response):
        timestamp = datetime.now().isoformat()
        row = [filename, timestamp, model, prompt, response]
        
        file_exists = os.path.isfile(self.filepath)
        
        loop = asyncio.get_event_loop()
        if not file_exists:
            await loop.run_in_executor(None, self._write_header_and_row, row)
        else:
            await loop.run_in_executor(None, self._append_row, row)

    def _write_header_and_row(self, row):
        with open(self.filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.columns)
            writer.writerow(row)

    def _append_row(self, row):
        with open(self.filepath, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

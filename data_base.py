import os
import pandas as pd
from datetime import datetime

FILE_NAME = os.path.dirname(os.path.abspath(__file__)) + '/history.csv'


def sanitize(text):
    if isinstance(text, str):
        return text.replace(',', ' ').replace('\n', '\t')
    else:
        return text


def dump(command, args, response, success):
    ts = datetime.now()
    text = command + ' ' + ' '.join([str(arg) for arg in args])
    new_row = pd.DataFrame({
        'success': [success],
        'timestamp': [ts.strftime('%d.%m.%Y %H:%M:%S')],
        'request': [sanitize(text)],
        'response': [sanitize(response)]
    })
    try:
        df = pd.read_csv(FILE_NAME, index_col=[0]);
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_NAME)
    except FileNotFoundError:
        new_row.to_csv(FILE_NAME)


def read_latest(n_latest):
    try:
        df = pd.read_csv(FILE_NAME, index_col=[0]);
        df_cropped = df.tail(n_latest)
        lines = []
        for _, row in df_cropped[::-1].iterrows():
            status = "SUCCESS" if row["success"] else "FAILED "
            time = row["timestamp"]
            request = row["request"]
            response = row["response"].replace('\t', '\n')
            lines.append(f'{time} | {status} | {request}\n{response}')
        return '\n\n'.join(lines)
        
    except FileNotFoundError:
        return 'Empty history'
    
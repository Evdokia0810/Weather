#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore")

import sys

from weather_api import get_weather, get_location_info, get_current_location_info, get_weather_result
from data_base import dump, read_latest


commands = {
    "get" : {
        "impl" : (lambda args : False, ""),
        "description" : '''
Print current weather conditions info.
Run "get" to access weather information about your current location.
Run "get [City]" to access weather information in desired city.
'''
    },
    "history" : {
        "impl" : (lambda args : False, ""),
        "description" : '''
Print queries history.
Run "history [n]" to see n latest requests.
When invoked with no arguments "history", will return 5 latest requests.
'''
    },
    "help" : {
        "impl" : (lambda args : False, ""),
        "description" : '''
Print useful information from above.
'''
    },
    "exit" : {
        "impl" : (lambda args : False, ""),
        "description" : '''
Run when done.
'''
    }
}


def command_get(args):
    if len(args) != 0 and len(args) != 1:
        return False, f'Insufficient number of input arguments for "get": {len(args)}'
    
    location_rsp = dict()
    if len(args) == 0:
        location_rsp = get_current_location_info()
    else:
        name = args[0]
        location_rsp = get_location_info(name)
    
    if not location_rsp["success"]:
        return False, location_rsp["status"]
    
    weather_rsp = get_weather(location_rsp)
    if not weather_rsp["success"]:
        return False, weather_rsp["status"]
    
    message = get_weather_result(weather_rsp)
    return True, message

def command_history(args):
    if len(args) != 0 and len(args) != 1:
        return False, f'Insufficient number of input arguments for "get": {len(args)}'
    n_lines = 5
    if len(args) == 1:
        if not args[0].isdigit():
            return False, f'History size must be a positive integer. Got: "{args[0]}"'
        n_lines = int(args[0])
        if n_lines <= 0:
            return False, f'History size must be at least 1'
    
    message = read_latest(n_lines)
    return True, message

def command_help(_):
    lines = []
    for cmd_name, cmd_body in commands.items():
        description = cmd_body['description']
        lines.append(f"** {cmd_name} ** {description}")
    return True, '\n'.join(lines)

def command_exit(_):
    return False, 'Bye bye!'


commands["get"]["impl"]     = command_get
commands["history"]["impl"] = command_history
commands["help"]["impl"]    = command_help
commands["exit"]["impl"]    = command_exit


def main():
    print('\n' + 'Welcome to weather app! Type help to get started' + '\n');
    done = False
    while not done:
        inp = input('weather > ')
        args = inp.strip().split()
        if len(args) == 0:
            continue
        command = args[0]
        args = args[1:]
        if command not in commands.keys():
            success = False
            response = f'Unknown command: "{command}"'
        else:
            cmd_body = commands[command]
            success, response = cmd_body["impl"](args)
            if command == "get":
                dump(command, args, response, success)
            if command == "exit":
                done = True
        print(f'\n{response}\n')



if __name__ == '__main__':
    main()

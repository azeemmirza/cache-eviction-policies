from time import time


def current_time():
    '''
    Returns the current time in seconds since the epoch.
    '''
    return time()

def time_after(seconds):
    '''
    Returns the time in seconds after the given number of seconds from now.
    '''
    return time() + seconds

def is_expired(expiration_time):
    '''
    Returns True if the current time is greater than the given expiration time, False otherwise.
    '''
    return time() > expiration_time
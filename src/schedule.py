from beautiful_date import *
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from sys import argv
from requests import HTTPError
from tzlocal import get_localzone_name
from dateparser import parse
from datetime import datetime, time
import logging 
import to_go
import ref

def logging_setup():
    log = logging.getLogger('schedule_log')
    if len(argv > 1):
        match argv:
            case 'warning':
                log.setLevel(logging.WARNING)
            case 'info':
                log.setLevel(logging.INFO)
            case 'debug':
                log.setLevel(logging.DEBUG)
            case _:
                log.error("wrong argument\n details %s", exc_info=1)
                raise
    log.setLevel(logging.INFO)
    return log
                
def event_exists(gc, new_event) -> bool:
         
    events = gc.get_events()
    for existing_event in events:
        # Compare event properties (e.g., summary, start, end)
        if (
            existing_event.summary == new_event.summary
            and existing_event.start == new_event.start
            and existing_event.end == new_event.end
        ):
            return True
    return False

def get_schedule_data(weeks):
    schedule_data = []
    curr_day = None
    dt = datetime.now()

    is1st = True
    for week in weeks:
        for day in week.splitlines():
            if len(day.split()) == 6:
                
                in_time = parse('{}{}{} {}{}'.format(day.split()[0], '\/', dt.year, day.split()[1], day.split()[2]))
                out_time = parse('{}{}{} {}{}'.format(day.split()[0], '\/', dt.year, day.split()[3], day.split()[4]))
                if time(hour=out_time.hour,minute=out_time.minute) == time(0,0):
                    
                    out_time = out_time - 1 * minutes
                    out_time = out_time + 1 * days
                    #out_time += timedelta(hours)
                    # out_time = 
                schedule_data.append({'in_time': in_time, 'out_time': out_time, 'dow': curr_day})
                   
    return schedule_data

def main():
    
    log = logging_setup()
    
    ID = ref.TO_GO_ID    
    weeks = to_go.main()
    log.info('weeks is asigned')
    log.debug(weeks)
    
    schedule_data = get_schedule_data(weeks)
    log.debug('schedule_data: {}'.format(schedule_data))
    gc = GoogleCalendar(ID)

    for data in schedule_data:
        event = Event(summary='work', start=data.get('in_time'), end=data.get('out_time'), timezone=get_localzone_name())
        log.debug('event: {}'.format(event))
        try:
            if not event_exists(gc, event):
                log.debug('does not exist in calendar')
                log.debug('adding :{}'.format(event))
                event = gc.add_event(event)
                print(f'event added:{event}')
            else:
                log.debug('item already exists')
        except HTTPError as e:
            print(f"Error adding event: {e}")
    events = gc.get_events()
    for event in events:
        print(event)

if __name__ == "__main__":
    main()
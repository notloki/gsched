# 1- call myjobtogo.com
# 2- Get Schedule
# 3- Convert Schedule to Dictionary.
# 4- call google and fetch copy of schedule. ifi item doesn't exist, setnwe



import ref
from requests import HTTPError
from tzlocal import get_localzone_name
from to_go import getToGo
from dateparser import parse
from datetime import datetime, timedelta
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
import logging 

OFFLINE = False

    




def event_exists(gc, new_event):
    if not OFFLINE:     
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

    for week in weeks:
        for day in week.splitlines():
            if day.endswith('day'):
                curr_day = day
            elif len(day.split()) == 6:
                in_time = parse('{}{}{} {}{}'.format(day.split()[0], '\/', dt.year, day.split()[1], day.split()[2]))
                out_time = parse('{}{}{} {}{}'.format(day.split()[0], '\/', dt.year, day.split()[3], day.split()[4]))
                if out_time < in_time:
                    out_time += timedelta(days=1)
                schedule_data.append({'in_time': in_time, 'out_time': out_time, 'dow': curr_day})
                curr_day = None
    return schedule_data

def main():
    
    log = logging.getLogger(name='schedule_log')

    ID = ref.TO_GO_ID
    USERNAME = ref.TO_GO_USERNAME
    PASSWORD = ref.TO_GO_PASSWORD
    
    weeks = getToGo(USERNAME, PASSWORD)
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
                print(event)
            else:
                log.debug('item already exists')
        except HTTPError as e:
            print(f"Error adding event: {e}")

    events = gc.get_events()
    for event in events:
        print(event)

if __name__ == "__main__":
    main()

    
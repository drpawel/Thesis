class KeyEvent:
    def __init__(self, key, key_down, key_up):
        self.key = key
        self.key_down = key_down
        self.key_up = key_up


def format_data(events):
    formatted_data = []
    last_event = ()

    for event, next_event in zip(events, events[1:]):
        formatted_data.append((event.key_up - event.key_down) / 1000)
        formatted_data.append((next_event.key_down - event.key_up) / 1000)
        formatted_data.append((next_event.key_down - event.key_down) / 1000)
        last_event = next_event

    formatted_data.append((last_event.key_up - last_event.key_down) / 1000)

    return tuple(formatted_data)


def retrieve_data(events):
    # TODO verify keys
    keys = ['.', 't', 'i', 'e', '5', 'Shift', 'o', 'a', 'n', 'l']
    key_down_list = []
    key_up_list = []

    for event in events:
        if event['keyCode'] not in keys:
            continue

        if event['state'] == 'KEY_DOWN':
            key_down_list.append([event['keyCode'], event['timestamp']])
        if event['state'] == 'KEY_UP':
            key_up_list.append([event['keyCode'], event['timestamp']])

    events = []

    for key_down_event in key_down_list:
        current_key = key_down_event[0]
        for key_up_event in key_up_list:
            if key_up_event[0] == current_key:
                events.append(KeyEvent(current_key, key_down_event[1], key_up_event[1]))
                key_up_list.remove(key_up_event)
                break

    return format_data(events)

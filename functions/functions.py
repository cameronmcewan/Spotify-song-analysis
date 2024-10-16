def convert_duration_ms(duration_ms):
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}m {seconds:02d}s"

def convert_key(key):
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return keys[key] if 0 <= key < len(keys) else "Unknown"

def convert_mode(mode):
    return "Major" if mode == 1 else "Minor"

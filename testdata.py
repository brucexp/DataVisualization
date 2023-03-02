from pylsl import StreamInlet, resolve_stream
import numpy as np

streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

while True:
    this_data, timestamp_ = inlet.pull_sample()
    print(this_data,timestamp_)
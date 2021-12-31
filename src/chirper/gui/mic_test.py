import numpy as np
import sounddevice as sd

from interface import GuiInterface


gui = GuiInterface()

gui.make_request({
    "request_type": "start",
    "source": "microphone",
})

while True:
    data = gui.make_request({
        "request_type": "spectrogram",
        "source": "microphone",
        "blocksize": 4410,
        "return_raw_data": True,
    })
    print(data.shape)
    # print("|" * int(np.linalg.norm(data) * 10))

gui.make_request({
    "request_type": "stop",
    "source": "microphone",
})

# def callback(inread, outread, frames, )

# with sd.InputStream(callback=callback)

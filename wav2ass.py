#!/usr/bin/env python
# -*-coding:utf-8 -*-
__author__ = 'jiang'
import io
import os
import sys
import subprocess
import wave
import aifc
import math
import audioop
import collections
import json
import base64
import threading
import platform
import stat
import hashlib
import hmac
import time
import uuid
try:  # attempt to use the Python 2 modules
    from urllib import urlencode
    from urllib2 import Request, urlopen, URLError, HTTPError
except ImportError:  # use the Python 3 modules
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

import os
import speech_recognition as sr


# from pydub import AudioSegment
import datetime
# ##获取音频时长
# f = wave.open(r"C:\Users\Esri\Desktop\speech.wav","rb")
# timelength=int(f.getparams()[3]/f.getparams()[2])
# print(int(5.6))
#
# ##音频分割输出
# readaudio=AudioSegment.from_wav(r'C:\Users\Esri\Desktop\speech.wav')
# kn=int(timelength/30)+1
# for i in range(kn):
#      readaudio[i*30*1000:((i+1)*30+2)*1000].export(r'C:\Users\Esri\Desktop\speech\speech%d.wav'%(i+1), format="wav")
##获取文件夹下的音频文件名
class WaitTimeoutError(Exception): pass


class RequestError(Exception): pass


class UnknownValueError(Exception): pass

def recognize_ibm(self, audio_data, apikey, language="en-US", show_all=False):
    """
    Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using the IBM Speech to Text API.

    The IBM Speech to Text username and password are specified by ``username`` and ``password``, respectively. Unfortunately, these are not available without `signing up for an account <https://console.ng.bluemix.net/registration/>`__. Once logged into the Bluemix console, follow the instructions for `creating an IBM Watson service instance <https://www.ibm.com/watson/developercloud/doc/getting_started/gs-credentials.shtml>`__, where the Watson service is "Speech To Text". IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX, while passwords are mixed-case alphanumeric strings.

    The recognition language is determined by ``language``, an RFC5646 language tag with a dialect like ``"en-US"`` (US English) or ``"zh-CN"`` (Mandarin Chinese), defaulting to US English. The supported language values are listed under the ``model`` parameter of the `audio recognition API documentation <https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#sessionless_methods>`__, in the form ``LANGUAGE_BroadbandModel``, where ``LANGUAGE`` is the language value.

    Returns the most likely transcription if ``show_all`` is false (the default). Otherwise, returns the `raw API response <https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#sessionless_methods>`__ as a JSON dictionary.

    Raises a ``speech_recognition.UnknownValueError`` exception if the speech is unintelligible. Raises a ``speech_recognition.RequestError`` exception if the speech recognition operation failed, if the key isn't valid, or if there is no internet connection.
    """
    assert isinstance(audio_data, sr.AudioData), "Data must be audio data"
    assert isinstance(apikey, str), "``username`` must be a string"

    flac_data = audio_data.get_flac_data(
        convert_rate=None if audio_data.sample_rate >= 16000 else 16000,  # audio samples should be at least 16 kHz
        convert_width=None if audio_data.sample_width >= 2 else 2  # audio samples should be at least 16-bit
    )

    url = "https://gateway-tok.watsonplatform.net/speech-to-text/api/v1/recognize?timestamps=true&max_alternatives=3"

    request = Request(url, data=flac_data, headers={
        "Content-Type": "audio/flac",
    })
    authorization_value = base64.standard_b64encode("{}:{}".format(username, password).encode("utf-8")).decode("utf-8")
    request.add_header("Authorization", "Basic {}".format(authorization_value))
    try:
        response = urlopen(request, timeout=self.operation_timeout)
    except HTTPError as e:
        raise RequestError("recognition request failed: {}".format(e.reason))
    except URLError as e:
        raise RequestError("recognition connection failed: {}".format(e.reason))
    response_text = response.read().decode("utf-8")
    result = json.loads(response_text)

    # return results
    if show_all: return result
    if "results" not in result or len(result["results"]) < 1 or "alternatives" not in result["results"][0]:
        raise UnknownValueError()

    transcription = []
    for utterance in result["results"]:
        if "alternatives" not in utterance: raise UnknownValueError()
        for hypothesis in utterance["alternatives"]:
            if "transcript" in hypothesis:
                transcription.append(hypothesis["transcript"])
    return "\n".join(transcription)

starttime = datetime.datetime.now()
def wav2ass(wav_path, name):
    print("{}开始转换".format(name))
    ##音频分块识别
    r = sr.Recognizer()
    try:
        with sr.WavFile(os.path.join(wav_path, name)) as source:
            audio = r.record(source)
            IBM_USERNAME = '*******************'
            IBM_PASSWORD = '*****'
            text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD, language='en-US')
            print(text)
            open('./ass/{}.txt'.format(name), 'a+').write(text)
            time.sleep(5)
            temptime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('{} {} 已完成'.format(temptime, name))

    except Exception as e:
        print(e)
        temptime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('{} {}  未完成'.format(temptime, name))
    jietime = datetime.datetime.now()
    last=jietime-starttime
    print('总共花费时间：%s'%last)
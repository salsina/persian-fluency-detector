from persian_fluency import *
# import os
# from pydub import AudioSegment
# from pydub.silence import split_on_silence
# from persian_syllable_counter import *

# import subprocess
# import wave
# import sys
# import os

# class SpeechToText:        
#     def __init__(self):
#         try:
#             from vosk import Model, KaldiRecognizer, SetLogLevel
#             print("module 'vosk' is installed")
#         except ModuleNotFoundError:
#             print("module 'vosk' is not installed")
#             # or
#             subprocess.check_call([sys.executable, "-m", "pip", "install", "vosk==0.3.30"])

#         SetLogLevel(-1)
#         if not os.path.exists("model"):
#             print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
#             exit (1)


#     def get_text_vosk(self, filename):
#         from vosk import Model, KaldiRecognizer
#         wf = wave.open(filename , "rb")
#         if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#             print ("Audio file must be WAV format mono PCM.")
#             exit (1)

#         model = Model("model")
#         rec = KaldiRecognizer(model, wf.getframerate())
#         rec.SetWords(True)

#         #clean file
#         final_text = ""
#         while True:
#             data = wf.readframes(4000)
#             if len(data) == 0:
#                 break
#             if rec.AcceptWaveform(data):
#                 string = rec.Result()
#                 text = string[string.find('"text"')+10:-3] + " "
#                 final_text += text
#         string = rec.FinalResult()
#         text = string[string.find('"text"')+10:-3]
#         final_text += text

#         return final_text


# class Fluency:
#     def __init__(self, _filename):
#         self.filename = _filename
#         self.SpeechToText = SpeechToText()
#         self.SyllableCounter = PersianSyllableCounter()
#         self.audio = AudioSegment.from_wav(self.filename)
#         self.SpeachRate = None
#         self.ArticulationRate = None
#         self.PhonationTimeRatio = None
#         self.MeanLengthOfRuns = None

#     def get_SpeechRate(self):
#         # The actual number of syllables uttered, divided by the total speech time in minutes. 
#         # This is the gross measure of speed of speech production, it includes the hesitation 
#         # in the total time spent speaking
#         if self.SpeachRate != None:
#             return self.SpeachRate
        
#         text = self.SpeechToText.get_text_vosk(self.filename)
#         text_syllables = self.SyllableCounter.count_syllables_in_text(text)
#         audio_length = self.audio.duration_seconds / 60
#         self.SpeachRate = text_syllables / audio_length
#         return self.SpeachRate
    
#     def get_ArticulationRate(self):
#         # The actual number of syllables uttured, divided by the total amount of time spent speaking.
#         # In this case, the hesitation time is eliminated from the calculation; this gives a measure
#         # of the speed of actual articulation only
#         if self.ArticulationRate != None:
#             return self.ArticulationRate
#         text = self.SpeechToText.get_text_vosk(self.filename)
#         text_syllables = self.SyllableCounter.count_syllables_in_text(text)
#         audio_chunks = split_on_silence(self.audio, min_silence_len=100, silence_thresh=-40)
#         audio_efficient_time_seconds = 0
#         for i, chunk in enumerate(audio_chunks):
#             audio_efficient_time_seconds += chunk.duration_seconds
#         self.ArticulationRate = text_syllables / (audio_efficient_time_seconds/60)
#         return self.ArticulationRate

#     def get_PhonationTimeRatio(self):
#         # This is determined by totaling the pause times for each speech sample and calculating it
#         # as a percent of the total speech time. It indicates the amount of hesitation relative to actual
#         # apeaking time, a combination measure of pause frequency and duration
#         if self.PhonationTimeRatio != None:
#             return self.PhonationTimeRatio
#         audio_chunks = split_on_silence(self.audio, min_silence_len=100, silence_thresh=-40)
#         audio_efficient_time_seconds = 0
#         for i, chunk in enumerate(audio_chunks):
#             audio_efficient_time_seconds += chunk.duration_seconds
        
#         self.PhonationTimeRatio = 1 - (audio_efficient_time_seconds / self.audio.duration_seconds)
#         return self.PhonationTimeRatio
    
#     def get_MeanLengthOfRuns(self):
#         # The mean number of syllables uttured between hesitations. It indicates the length of 
#         # utturance between pauses.
#         if self.MeanLengthOfRuns != None:
#             return self.MeanLengthOfRuns
#         audio_chunks = split_on_silence(self.audio, min_silence_len=800, silence_thresh=-40)
#         syllables_in_runs = []
#         if not os.path.exists("cache"):
#             os.mkdir("cache")
#         for i, chunk in enumerate(audio_chunks):
#             temp_output_file = "cache/segment"+str(i)+".wav"
#             chunk.export(temp_output_file, format="wav")
#             text = self.SpeechToText.get_text_vosk(temp_output_file)
#             os.remove(temp_output_file)
#             text_syllables = self.SyllableCounter.count_syllables_in_text(text)
#             syllables_in_runs.append(text_syllables)
#         os.rmdir("cache")
#         self.MeanLengthOfRuns = sum(syllables_in_runs) / len(syllables_in_runs)
#         return self.MeanLengthOfRuns
    
# # sample use
# # fluency = Fluency("Sample_Audios/wav/titleA.wav")
# # print(fluency.get_PhonationTimeRatio())

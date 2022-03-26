import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from persian_syllable_counter import PersianSyllableCounter
from persian_speech_to_text import SpeechToText

class Fluency:
    def __init__(self, _filename):
        self.filename = _filename
        self.SpeechToText = SpeechToText()
        self.SyllableCounter = PersianSyllableCounter()
        self.audio = AudioSegment.from_wav(self.filename)
        self.SpeachRate = None
        self.ArticulationRate = None
        self.PhonationTimeRatio = None
        self.MeanLengthOfRuns = None

    def get_SpeechRate(self):
        # The actual number of syllables uttered, divided by the total speech time in minutes. 
        # This is the gross measure of speed of speech production, it includes the hesitation 
        # in the total time spent speaking
        if self.SpeachRate != None:
            return self.SpeachRate
        
        text = self.SpeechToText.get_text_vosk(self.filename)
        text_syllables = self.SyllableCounter.count_syllables_in_text(text)
        audio_length = self.audio.duration_seconds / 60
        self.SpeachRate = text_syllables / audio_length
        return self.SpeachRate
    
    def get_ArticulationRate(self):
        # The actual number of syllables uttured, divided by the total amount of time spent speaking.
        # In this case, the hesitation time is eliminated from the calculation; this gives a measure
        # of the speed of actual articulation only
        if self.ArticulationRate != None:
            return self.ArticulationRate
        text = self.SpeechToText.get_text_vosk(self.filename)
        text_syllables = self.SyllableCounter.count_syllables_in_text(text)
        audio_chunks = split_on_silence(self.audio, min_silence_len=100, silence_thresh=-40)
        audio_efficient_time_seconds = 0
        for i, chunk in enumerate(audio_chunks):
            audio_efficient_time_seconds += chunk.duration_seconds
        self.ArticulationRate = text_syllables / (audio_efficient_time_seconds/60)
        return self.ArticulationRate

    def get_PhonationTimeRatio(self):
        # This is determined by totaling the pause times for each speech sample and calculating it
        # as a percent of the total speech time. It indicates the amount of hesitation relative to actual
        # apeaking time, a combination measure of pause frequency and duration
        if self.PhonationTimeRatio != None:
            return self.PhonationTimeRatio
        audio_chunks = split_on_silence(self.audio, min_silence_len=100, silence_thresh=-40)
        audio_efficient_time_seconds = 0
        for i, chunk in enumerate(audio_chunks):
            audio_efficient_time_seconds += chunk.duration_seconds
        
        self.PhonationTimeRatio = 1 - (audio_efficient_time_seconds / self.audio.duration_seconds)
        return self.PhonationTimeRatio
    
    def get_MeanLengthOfRuns(self):
        # The mean number of syllables uttured between hesitations. It indicates the length of 
        # utturance between pauses.
        if self.MeanLengthOfRuns != None:
            return self.MeanLengthOfRuns
        audio_chunks = split_on_silence(self.audio, min_silence_len=800, silence_thresh=-40)
        syllables_in_runs = []
        if not os.path.exists("cache"):
            os.mkdir("cache")
        for i, chunk in enumerate(audio_chunks):
            temp_output_file = "cache/segment"+str(i)+".wav"
            chunk.export(temp_output_file, format="wav")
            text = self.SpeechToText.get_text_vosk(temp_output_file)
            os.remove(temp_output_file)
            text_syllables = self.SyllableCounter.count_syllables_in_text(text)
            syllables_in_runs.append(text_syllables)
        os.rmdir("cache")
        self.MeanLengthOfRuns = sum(syllables_in_runs) / len(syllables_in_runs)
        return self.MeanLengthOfRuns
    
# sample use
# fluency = Fluency("Sample_Audios/wav/titleA.wav")
# print(fluency.get_PhonationTimeRatio())

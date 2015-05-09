#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Sun Mar  3 11:15:48 2013
##################################################

from gnuradio import audio
from gnuradio import blks2
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import acars
import osmosdr
import wx

class top_block(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Top Block")

		##################################################
		# Variables
		##################################################
		self.threshold = threshold = 1
		self.samp_rate = samp_rate = 48000
		self.rf_freq = rf_freq = 136780000
		self.ch0ifgain = ch0ifgain = 36
		self.ch0gain = ch0gain = 24
		self.audiogain = audiogain = 200

		##################################################
		# Blocks
		##################################################
		_threshold_sizer = wx.BoxSizer(wx.VERTICAL)
		self._threshold_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_threshold_sizer,
			value=self.threshold,
			callback=self.set_threshold,
			label='threshold',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._threshold_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_threshold_sizer,
			value=self.threshold,
			callback=self.set_threshold,
			minimum=0,
			maximum=1000,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_threshold_sizer, 1, 1, 1, 1)
		_ch0ifgain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._ch0ifgain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_ch0ifgain_sizer,
			value=self.ch0ifgain,
			callback=self.set_ch0ifgain,
			label="ch0ifgain",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._ch0ifgain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_ch0ifgain_sizer,
			value=self.ch0ifgain,
			callback=self.set_ch0ifgain,
			minimum=0,
			maximum=42,
			num_steps=42,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_ch0ifgain_sizer, 4, 1, 1, 1)
		_ch0gain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._ch0gain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_ch0gain_sizer,
			value=self.ch0gain,
			callback=self.set_ch0gain,
			label='ch0gain',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._ch0gain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_ch0gain_sizer,
			value=self.ch0gain,
			callback=self.set_ch0gain,
			minimum=-1,
			maximum=42,
			num_steps=43,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_ch0gain_sizer, 3, 1, 1, 1)
		_audiogain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._audiogain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_audiogain_sizer,
			value=self.audiogain,
			callback=self.set_audiogain,
			label='audiogain',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._audiogain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_audiogain_sizer,
			value=self.audiogain,
			callback=self.set_audiogain,
			minimum=0,
			maximum=1000,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_audiogain_sizer, 2, 1, 1, 1)
		self.wxgui_fftsink2_1 = fftsink2.fft_sink_f(
			self.GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=20,
			ref_scale=2.0,
			sample_rate=6000,
			fft_size=1024,
			fft_rate=10,
			average=False,
			avg_alpha=None,
			title="Audio",
			peak_hold=False,
		)
		self.GridAdd(self.wxgui_fftsink2_1.win, 6, 1, 1, 1)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=rf_freq,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate*24,
			fft_size=1024,
			fft_rate=5,
			average=False,
			avg_alpha=None,
			title="RF",
			peak_hold=False,
		)
		self.GridAdd(self.wxgui_fftsink2_0.win, 5, 1, 1, 1)
		self.osmosdr_source_c_0 = osmosdr.source_c( args="nchan=" + str(1) + " " + "" )
		self.osmosdr_source_c_0.set_sample_rate(samp_rate*24)
		self.osmosdr_source_c_0.set_center_freq(rf_freq, 0)
		self.osmosdr_source_c_0.set_freq_corr(-32, 0)
		self.osmosdr_source_c_0.set_gain_mode(1, 0)
		self.osmosdr_source_c_0.set_gain(ch0gain, 0)
		self.osmosdr_source_c_0.set_if_gain(ch0ifgain, 0)
			
		self.low_pass_filter_0 = gr.fir_filter_ccf(6, firdes.low_pass(
			1, samp_rate*24, 500000, 150000, firdes.WIN_HAMMING, 6.76))
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vff((audiogain, ))
		self.gr_keep_one_in_n_0 = gr.keep_one_in_n(gr.sizeof_float*1, 8)
		self.gr_dc_blocker_0 = gr.dc_blocker_ff(64, True)
		self.blks2_am_demod_cf_0 = blks2.am_demod_cf(
			channel_rate=samp_rate*4,
			audio_decim=4,
			audio_pass=5000,
			audio_stop=5500,
		)
		self.audio_sink_0 = audio.sink(samp_rate, "", True)
		self.acars_decodeur_0 = acars.decodeur(threshold,"/tmp/log_jmf.txt")

		##################################################
		# Connections
		##################################################
		self.connect((self.osmosdr_source_c_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.blks2_am_demod_cf_0, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.low_pass_filter_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.acars_decodeur_0, 0))
		self.connect((self.blks2_am_demod_cf_0, 0), (self.gr_dc_blocker_0, 0))
		self.connect((self.gr_dc_blocker_0, 0), (self.gr_multiply_const_vxx_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.gr_keep_one_in_n_0, 0))
		self.connect((self.gr_keep_one_in_n_0, 0), (self.wxgui_fftsink2_1, 0))


	def get_threshold(self):
		return self.threshold

	def set_threshold(self, threshold):
		self.threshold = threshold
		self.acars_decodeur_0.set_seuil(self.threshold)
		self._threshold_slider.set_value(self.threshold)
		self._threshold_text_box.set_value(self.threshold)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate*24, 500000, 150000, firdes.WIN_HAMMING, 6.76))
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate*24)
		self.osmosdr_source_c_0.set_sample_rate(self.samp_rate*24)

	def get_rf_freq(self):
		return self.rf_freq

	def set_rf_freq(self, rf_freq):
		self.rf_freq = rf_freq
		self.wxgui_fftsink2_0.set_baseband_freq(self.rf_freq)
		self.osmosdr_source_c_0.set_center_freq(self.rf_freq, 0)

	def get_ch0ifgain(self):
		return self.ch0ifgain

	def set_ch0ifgain(self, ch0ifgain):
		self.ch0ifgain = ch0ifgain
		self._ch0ifgain_slider.set_value(self.ch0ifgain)
		self._ch0ifgain_text_box.set_value(self.ch0ifgain)
		self.osmosdr_source_c_0.set_if_gain(self.ch0ifgain, 0)

	def get_ch0gain(self):
		return self.ch0gain

	def set_ch0gain(self, ch0gain):
		self.ch0gain = ch0gain
		self._ch0gain_slider.set_value(self.ch0gain)
		self._ch0gain_text_box.set_value(self.ch0gain)
		self.osmosdr_source_c_0.set_gain(self.ch0gain, 0)

	def get_audiogain(self):
		return self.audiogain

	def set_audiogain(self, audiogain):
		self.audiogain = audiogain
		self._audiogain_slider.set_value(self.audiogain)
		self._audiogain_text_box.set_value(self.audiogain)
		self.gr_multiply_const_vxx_0.set_k((self.audiogain, ))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = top_block()
	tb.Run(True)


from bf_nlu.nlu.components import Component
from bf_nlu.nlu import utils
from bf_nlu.nlu.model import Metadata
import os
import pandas as pd
import typing
from typing import Any, Optional, Text, Dict
import numpy as np
import regex as re


class Extract_dupont(Component):
	"""A custom sentiment analysis component"""
	name = "FACT_EXTRACTION"
	provides = ["entities"]
	requires = ["tokens"]
	defaults = {}
	language_list = ["fr"]
	print('initialised the class')

	def __init__(self, component_config=None):
		super(Extract_dupont, self).__init__(component_config)

	def train(self, training_data, cfg, **kwargs):
		"""Load the sentiment polarity labels from the text
		   file, retrieve training tokens and after formatting
		   data train the classifier."""



	def convert_to_bf_nlu_finition(self, value):
		"""Convert model output into the bf_nlu NLU compatible output format."""

		
		entity = {"value": value,
				  
				"entity": "finition",
				"extractor": "dupont"}

		return entity

	


	def process(self, message, **kwargs):
		"""Retrieve the tokens of the new message, pass it to the classifier
			and append prediction results to the message class."""
		if not self :
			entities = []
		else:
	
#detection pays	
			print("ok")
			tokens = [t.text for t in message.get("tokens")]
			datas = pd.read_csv('finition.csv',sep=';',encoding="utf_8")
			finition= np.array(datas['finition'])
			code= np.array(datas['code'])
			ent_val = {}
			entity_conv = []
			entity = ""
			for i in range(len(code)):
				ent_val[finition[i]] = code[i]
			for word in tokens:
				for key in ent_val:
					if key == word:
						entity = ent_val[key]
						
			entity_finit = self.convert_to_bf_nlu_finition(entity)

#detection de poids !!!!
			

			


			message.set("entity_finition", [entity_finit], add_to_output=True)
			
import nltk
import string
import re

def textToEntityRelations(allResponses, min_length=1):

	tokenDict = {}

	for response in allResponses:
		
		#strip punctuation
		regex = re.compile('[%s]' % re.escape(string.punctuation))
		text = regex.sub(' ', response.openEnded)

		textList = text.split()
		tokens = filter(lambda x: len(x[0]) > min_length and ('NN' in x[1] or 'JJ' in x[1]),nltk.pos_tag(textList))
		adjectives = filter(lambda x: 'JJ' in x[1], tokens)
		nouns = filter(lambda x: 'NN' in x[1], tokens)
		if len(nouns) > 0 and len(adjectives) > 0:
			print nouns[0],'->',adjectives[0], response.openEnded
			print '----'


	"""
	print 
		for t in tokens:
			lowerCaseToken = t[0].lower()
			if lowerCaseToken in tokenDict:
				tokenDict[lowerCaseToken] = tokenDict[lowerCaseToken] + 1
			else:
				tokenDict[lowerCaseToken] = 1

	for response in allResponses:
		text = response.openEnded.split()
		#Top noun
		tokens = filter(lambda x: len(x[0]) > min_length and ('NN' in x[1]),nltk.pos_tag(text))
		rankedNNTokens = [(tokenDict[t[0].lower()],t[0]) for t in tokens]
		rankedNNTokens.sort()

		#Top adjective
		tokens = filter(lambda x: len(x[0]) > min_length and ('JJ' in x[1]),nltk.pos_tag(text))
		rankedJJTokens = [(tokenDict[t[0].lower()],t[0]) for t in tokens]
		rankedJJTokens.sort()

		if len(rankedNNTokens) > 0 and len(rankedJJTokens) > 0:
			print response.openEnded,rankedNNTokens[-1],'->',rankedJJTokens[-1]
	"""

	
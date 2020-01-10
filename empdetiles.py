import io
import os
import re
import nltk,docx
import spacy
import pandas as pd
#import doc2text
#from . import constants as cs
from spacy.matcher import Matcher
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import psycopg2
from psycopg2 import Error 

class main():
	file = str(input("provied the input file path...!"))
	name,ext = os.path.splitext(file)
	global name
	global textformate

	if ext == '.pdf':
		resource_manager = PDFResourceManager()
		fake_file_handle = io.StringIO()
		converter = TextConverter(resource_manager, fake_file_handle)
		page_interpreter = PDFPageInterpreter(resource_manager, converter)
		pdf = open(file,'rb')

		for i in PDFPage.get_pages(pdf):
			page_interpreter.process_page(i)
		textformate = fake_file_handle.getvalue()
		#print(textfoemate)

	elif ext == '.docx':
		doc = docx.Document(file)
		for para in doc.paragraphs:
			textformate = para.text
			#print(textformate)
	
	elif ext == '.txt':
		f = open(file,'r')
		textformate = f.read()
		#print(textformate)
	
	elif ext == '.doc':
		temp = doc2text.process(file)
		textformate = [line.replace('\t', ' ') for line in temp.split('\n') if line]
		textformate = ' '.join(textformate)
		#print(textformate)

	def Process(self):
		global lines,sentences,tockens
		try:
			lines=[el.strip() for el in textformate.split("\n") if len(el)>0]
			lines=[nltk.word_tokenize(el) for el in lines]
			lines=[nltk.pos_tag(el) for el in lines]

			sentences = nltk.sent_tokenize(textformate)
			sentences = [nltk.word_tokenize(sent) for sent in sentences]
			tokens = sentences
			sentences = [nltk.pos_tag(sent) for sent in sentences]

			dummy = []
			for el in tokens:
				dummy += el
				tockens = dummy
			#return lines, sentences, tockens
		except Exception as e:
			print(e)

	def getName1(self):
		global c1
		regex = re.compile(r"([A-Z][a-z]+(?:[A-Za-z]\.)?)") #name=re.findall("([A-Za-z]{2,15})",textformate)
		name = regex.findall(textformate)
		if name:
			a1=name[0]
			b=name[1]
			c1 = a1+b
			#return c1
			
	def getName1(self):
		global c1
		nlp = spacy.load('en_core_web_sm')
		nlp_text = nlp(textformate)
		tokens = [token.text for token in nlp_text if not token.is_stop]

		file = "D:/python/PdfProgram/allNames.txt"
		name = open(file,'r')
		names = name.read()

		nameset = []
		for token in tokens:
			if token.lower() in names:
				nameset.append(token)

		for token in nlp_text:
			token = token.text.lower().strip()
			if token in names:
				nameset.append(token)

		name = [i.capitalize() for i in set([i.lower() for i in nameset])] #regex = re.compile(r"([A-Z][a-z]+(?:[A-Za-z]\.)?)")
		name=re.findall("([A-Za-z]{2,15})",' '.join(name)) #name = regex.findall(' '.join(name))
		if name:
			a1=name[0]
			b=name[1]
			c1 = a1+b

	def getMail(self):
		global em
		email = re.findall("([a-z0-9{2,5}.+_]+@[^@]+\.[com]+)",textformate)
		#email = re.findall('[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}',textformate)
		#print(email)
		if email:
			em=email[0].split()[0].strip(';')
		#if em = 
			#return em
			

	def getMobile(self):
		global number
		mobile = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{7})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), textformate)
		if mobile:
			number = ' '.join(mobile[0])
			if len(number)>13:
				number = '+'+number
				#return number
			else:
				return number
				
	def getPersantage(self):
		global per
		Percentage = re.findall(re.compile(r'([+-]?[0-9][0-9]+\.[0-9]+)|\%'),textformate)
		if Percentage:
			per = ' '.join(Percentage[0])
		else:
			per = "not defind"
			#return per
			

	def getEducation(self):
		global education
		edu = {}
		# Extract education degree
		nlp = spacy.load('en_core_web_sm')
		STOPWORDS = set(stopwords.words('english'))
		#noun_chunks = nlp.noun_chunks
		EDUCATION = ['BE','B.E.', 'B.E', 'BS', 'B.S', 'ME', 'M.E', 'M.E.', 'MS', 'M.S', 'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII']

		nlp_text = nlp(textformate)
		nlp_text = [sent.string.strip() for sent in nlp_text.sents]
		edu = {}
		for i,txt in enumerate(nlp_text):
			for tex in txt.split():
				tex = re.sub(r'[?|$|.|!|,]', r'', tex)
				if tex.upper() in EDUCATION and tex not in STOPWORDS:
					edu[tex] = txt + nlp_text[i + 1]
		
		education = []
		for key in edu.keys():
			year = re.search(r'(((20|19)(\d{2})))', edu[key])
			if year:
				education.append((key, ''.join(year[0])))
			else:
				education.append(key)
		#return education
		

	def getSkill(self):
		global skill
		nlp = spacy.load('en_core_web_sm')
		nlp_text = nlp(textformate)
		tokens = [token.text for token in nlp_text if not token.is_stop]

		data = pd.read_csv(os.path.join(os.path.dirname(__file__), "D:/python/New folder/skills.csv"))
		skills = list(data.columns.values)

		skillset = []
		for token in tokens:
			if token.lower() in skills:
				skillset.append(token)

		for token in nlp_text:
			token = token.text.lower().strip()
			if token in skills:
				skillset.append(token)

		skill=[i.capitalize() for i in set([i.lower() for i in skillset])]
		#print(skill)

	def getExperiance(slef):
		global exp
		exp = re.search('experience',textformate)
		a = exp.span()
		i = a[0]-1
		j = 1000+a[0]
		while i<=j:
			i+=1
			word = (stri[i])
			print(word,end="")
			exp = 


	def getExperiance1(self):
		global experience

		wordnet_lemmatizer = WordNetLemmatizer()
		stop_words = set(stopwords.words('english'))

		word_tokens = nltk.word_tokenize(textformate)
		filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words]
		sent = nltk.pos_tag(filtered_sentence)
		cp = nltk.RegexpParser('P: {<NNP>+}')
		cs = cp.parse(sent)
		test = []
		for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):
			test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))
			experience = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
		#print(experience)

	def Insert(self):
		try:
			connection = psycopg2.connect(user="postgres",
                                  password="vee",
                                  host="localhost",
                                  port="1624",
                                  database="pion")
			cursor = connection.cursor()
			postgres_insert_query = """ INSERT INTO pppp2(id,name,email,mobile,Percentage,experiance,education) VALUES(default,%s,%s,%s,%s,%s,%s) """
			data  = (c1,em,number,per,experience,education)
			cursor.execute(postgres_insert_query,data)
			connection.commit()
			count = cursor.rowcount
			print (count, "Record inserted successfully into pppp2 table")
		except (Exception, psycopg2.Error) as error :
			if(connection):
				print("Failed to insert record into pppp2 table", error)
		finally:
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")



if __name__ == '__main__':
	m = main()
	m.Process()
	#m.getName()
	m.getMail()
	m.getMobile()
	m.getPersantage()
	m.getEducation()
	m.getExperiance()
	m.getSkill()
	#m.Insert()


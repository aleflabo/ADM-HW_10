#!/usr/bin/env python
# coding: utf-8

from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
from nltk import pos_tag, ne_chunk
import nltk


# list of stopwords
stopWords = set(stopwords.words('english'))
# the stemmer used
ps = PorterStemmer()
# list of punctuation used
string.punctuation = string.punctuation + '–“”’'


# preprocess takes a list of words as input and RETURNS a list of stemmed words without stopwords and punctuation
def preprocess(l):
    final = []
    for i in l:
        if not((ps.stem(i) in stopWords) or (ps.stem(i) in (string.punctuation) )):
            final.append(ps.stem(i))
    return (final)

# takes a dictionary, a list of words and an integer. RETURNS a dictionary of words and an integer.
# this functions map each word in vocabulary to an integer (that starts from index)
def vocabularization(vocabulary, final, index):
    for word in final:
        if not(word in vocabulary):
            vocabulary[word] = str(index)
            index = index + 1
    return(vocabulary, index)




# RETRIEVING AVERAGE REVIEWS STARS
# rating value of reviews; it can be None if there is no review

def rating_value_reviews(airbnb_content, airbnb_soup):
    
    if not(airbnb_content.history):
        rating_value_reviews_text = airbnb_soup.find_all("div", attrs={"itemprop": "ratingValue"})
        
        if rating_value_reviews_text != []:
            indx = str(rating_value_reviews_text).find("content")+len("content")+2
            rating_value_reviews = float(str(rating_value_reviews_text)[indx:].split('" ')[0])            
        else:
            rating_value_reviews = numpy.nan
    
    else:
        rating_value_reviews = numpy.nan
        
    return(rating_value_reviews)


def listing_amenities(airbnb_content, airbnb_soup):

    if not(airbnb_content.history):
        idx = airbnb_soup.text.find("listing_amenities")+len("listing_amenities")+2
        having_amenities = {}
        nothaving_amenities = {}
        
        for a in airbnb_soup.text[idx:].split("}"):
            if all(keyword in a for keyword in ["category","icon","id","is_business_ready_feature","is_present",
                                                "is_safety_feature","name","select_list_view_photo",
                                                "select_tile_view_photo","tooltip"]):
                
                amenity = a[(a.find("name")+len("name"))+3:].split('",')[0]
                amenity_idx = int(a[(a.find("id")+len("id"))+2:].split(',')[0])
                
                idx_is_present = a.find("is_present")+len("is_present")+2 #check whether the amenity provides or not
                if a[idx_is_present:idx_is_present+1].upper() == 'T':
                    having_amenities[amenity] = amenity_idx
                else:
                    nothaving_amenities[amenity] = amenity_idx
            
        having_amenities = ",".join(list(having_amenities.keys()))
        nothaving_amenities = ",".join(list(nothaving_amenities.keys()))
        
    else:
        having_amenities = numpy.nan
        nothaving_amenities = numpy.nan

    return(having_amenities, nothaving_amenities)




# Is the host superhost? We'll get answer as boolean

def is_superhost(airbnb_content, airbnb_soup):
    if not(airbnb_content.history):
        idx = airbnb_soup.text.find("is_superhost")+len("is_superhost")+2
        is_superhost = airbnb_soup.text[idx:idx+1].upper() # T or F
    else:
        is_superhost = numpy.nan
        
    return(is_superhost)




# number of guest

def guest_no(airbnb_content, airbnb_soup):
    if not(airbnb_content.history):
        start_indx = airbnb_soup.text.find("guest_label")+len("guest_label")+2
        guest_no = int(re.search(r'\d+', airbnb_soup.text[start_indx:].split(",")[0]).group())
    else:
        guest_no = numpy.nan
        
    return(guest_no)




# bath_type

def bath_type(airbnb_content, airbnb_soup):
    if not(airbnb_content.history):
        start_idx = airbnb_soup.text.find("bathroom_label")+len("bathroom_label")+3
        end_idx = airbnb_soup.text[start_idx:].find(",")
        bath_type = airbnb_soup.text[start_idx:start_idx+end_idx-1]
    else:
        bath_type = numpy.nan

    return(bath_type)




# number of bed

def bed_no(airbnb_content, airbnb_soup):
    if not(airbnb_content.history):
        start_idx = airbnb_soup.text.find("bed_label")+len("bed_label")+3
        end_idx = airbnb_soup.text[start_idx:].find("bed")
        bed_no = int(re.search(r'\d+', airbnb_soup.text[start_idx:start_idx+end_idx-1]).group())
    else:
        bed_no = numpy.nan
        
    return(bed_no)






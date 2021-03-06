  #  <automated topic extraction tool for PDF documents.>
  #  Copyright (C) <2016>  <Maoyi Huang & Maomao Chen>

  # This program is free software: you can redistribute it and/or modify
  #  it under the terms of the GNU General Public License as published by
  #  the Free Software Foundation, either version 3 of the License, or
  #  (at your option) any later version.

  #  This program is distributed in the hope that it will be useful,
  #  but WITHOUT ANY WARRANTY; without even the implied warranty of
  #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  #  GNU General Public License for more details.

  #  You should have received a copy of the GNU General Public License
  #  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-

# -----------------------------------------------------

#   Function: Convert pdf to txt(without processing images), and analyze the content using ngrams, then filter
#   the processed with a blacklist and whitelist.

#   Author: Maoyi Huang & Maomao Chen

#   Date：2016-06-08

#   Lanuguage：Python 2.7.6

#   External Library:  PDFMiner20140328（Must be installed）, pyenchant


#   Traversal Directory is set to: /home/maoyi/Downloads/PDF in ubuntu environment
#   The traversal directory can be modified into the accordingly useful directory

# -----------------------------------------------------

import re

import os

import os.path

import sys

#   Need to install a pyenchant

import enchant



from pdfminer.converter import TextConverter

from pdfminer.layout import LAParams

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.pdfpage import PDFPage



from pdfminer.pdfpage import PDFTextExtractionNotAllowed

from pdfminer.pdfdocument import PDFDocument

from pdfminer.pdfparser import PDFParser

from pdfminer.pdfdevice import PDFDevice

from pdfminer.converter import PDFPageAggregator

from pdfminer.layout import *



from collections import Counter

import pdb



#Declare a Blacklist

BLACKLIST = ['a','xi', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t',

             'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can\'t',

             'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down',

             'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t',

             'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself',

             'his', 'how', 'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it',

             'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my', 'myself', 'no', 'nor', 'not',

             'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over',

             'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t', 'so', 'some',

             'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',

             'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through',

             'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve',

             'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while', 'who',

             'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll',

             'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves', '', 'a', 'able', 'about', 'above', 'abst',

             'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected',

             'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along',

             'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another',

             'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently',

             'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth',

             'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming',

             'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe',

             'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c',

             'ca', 'came', 'can', 'cannot', 'can\'t', 'cause', 'causes', 'certain', 'certainly', 'co', 'com', 'come',

             'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'd', 'date', 'did', 'didn\'t',

             'different', 'do', 'does', 'doesn\'t', 'doing', 'done', 'don\'t', 'down', 'downwards', 'due', 'during',

             'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end',

             'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone',

             'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix',

             'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from',

             'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go',

             'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', 'hasn\'t', 'have', 'haven\'t',

             'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon',

             'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit',

             'however', 'hundred', 'i', 'id', 'ie', 'if', 'i\'ll', 'im', 'immediate', 'immediately', 'importance',

             'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is',

             'isn\'t', 'it', 'itd', 'it\'ll', 'its', 'itself', 'i\'ve', 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'kg',

             'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least',

             'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', '\'ll', 'look', 'looking',

             'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means',

             'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most',

             'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd',

             'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new',

             'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos',

             'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often',

             'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other',

             'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing',

             'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed',

             'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present',

             'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly',

             'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs',

             'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted',

             'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec',

             'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent',

             'seven', 'several', 'shall', 'she', 'shed', 'she\'ll', 'shes', 'should', 'shouldn\'t', 'show', 'showed',

             'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six',

             'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime',

             'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify',

             'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently',

             'suggest', 'sup', 'sure', 't', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks',

             'thanx', 'that', 'that\'ll', 'thats', 'that\'ve', 'the', 'their', 'theirs', 'them', 'themselves', 'then',

             'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', 'there\'ll', 'thereof',

             'therere', 'theres', 'thereto', 'thereupon', 'there\'ve', 'these', 'they', 'theyd', 'they\'ll', 'theyre',

             'they\'ve', 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through',

             'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried',

             'tries', 'truly', 'try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless',

             'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully',

             'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', '\'ve', 'very', 'via', 'viz', 'vol',

             'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome', 'we\'ll', 'went',

             'were', 'werent', 'we\'ve', 'what', 'whatever', 'what\'ll', 'whats', 'when', 'whence', 'whenever', 'where',

             'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which',

             'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', 'who\'ll', 'whom', 'whomever', 'whos',

             'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world',

             'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', 'you\'ll', 'your', 'youre', 'yours',

             'yourself', 'yourselves', 'you\'ve', 'z', 'zero','&','.',',','/']

#Declare a whitelist

WHITELIST = []



WHITELIST_ALL = []



DEL_WORDS = []

# main

def main():

    #pdb.set_trace()

    traversalFile()

    return





#n-gram algorithm to split the words

def getNgrams(input, n):

    input = input.split(' ')

    output = []

    for i in range(len(input) - n + 1):

        output.append(input[i:i + n])

    return output



#Original idea to split the words with a space, but without using ngram algorithm, now it is not used

def getList(input):

    output = input.split(' ')

    return output



#TO return the 20 most frequently appeared words from the document in order to get the whitelist later, now it is not used

def get_top_twenty(data):

    word_counts = Counter(data)

    top_five = word_counts.most_common(20)



    return top_five



#TO extract the same element in the list, then the high frequency words per page can be put into whitelist

def get_same_data(data_list):

    # num = 0

    # top_fives = []

    # for item in data_list:

    #     for itemn in item:

    #         if len(itemn):

    #             for m in range(len(itemn)):

    #                 item[m]=itemn[m].lower()

    #Use dictionary function to count the matched words appearing frequency

    dics = []

    dic = {}

    for items in data_list:

        for item in items:

            # print(item)

            if ','.join(item) in dic.keys():

                dic[','.join(item)] += 1

            else:

                dic[','.join(item)] = 1

            # print dic

        res = sorted(dic.items(), key=lambda x: x[1], reverse=True)

        for m in range(len(res)):

            if res[m][1] >= 5:

                dics.append(res[m][0])

                #dics+=res[m][0]

    #     print dics

    # # print "over"

    # print dics

    b = [x for x in dics if dics.count(x) != 1]

    b = list(set(b))



    # print b

    #     num += 1

    #     val = get_top_twenty(item)

    #     item = zip(*val)[0]

    #     top_fives.extend(list(item))

    # ret = []

    # top_five = get_top_twenty(top_fives)

    #

    # for item in top_five:

    #     if item[1] == num:ret.append(item[0])

    return b



#Traverse the directory, find the PDF document

def traversalFile():

    chose = raw_input("please enter your gram[1-5]:")

   # chose = 2

    while (int(chose) not in range(1, 6)):

        print("enter error number, please enter again")

        chose = raw_input("please enter your gram[1-5]:")



    for parent, dirnames, filenames in os.walk(r'/home/maoyi/Downloads/manual100'):  # 3 parameters: return 1. Parent directory 2. all directory names 3. all filenames


        for filename in filenames:  # output file information

            if os.path.splitext(filename)[1] == '.pdf':

                print "filename is:" + filename

                pdf = os.path.join(parent, filename)  # output the file directory

                outfile = pdf + '.txt'

                analyseFile(pdf, outfile, int(chose))



#Traverse the PDF by page, then creating a whilte to contain the found high-frequency words

def createWhiteList(pdf, choose):



    f = open("del.dat")

    line = f.readline()

    all_word = line.strip().split(" ")

    all_word = set(all_word)

    all_word = list(all_word)

    DEL_WORDS = all_word



    d = enchant.Dict("en_US")

    global WHITELIST

    fp = file(pdf, 'rb')

    #Create a pdf document analyzer

    parser = PDFParser(fp)


    #Create a PDF document object storage structure

    document = PDFDocument(parser)


    #Check if the PDF document is extractable

    if not document.is_extractable:

        raise PDFTextExtractionNotAllowed

    else:


    #Create a PDF reserce manager to store the shared resrouces

        rsrcmgr=PDFResourceManager()


        #Set up the related parameters to analyze

        laparams=LAParams()


        #Create a PDF device object

        # device=PDFDevice(rsrcmgr)

        device=PDFPageAggregator(rsrcmgr,laparams=laparams)


        #Create a PDF interpreter for reading page by page

        interpreter=PDFPageInterpreter(rsrcmgr,device)


        #Process the document page by page

        pageText=''

        ngramsRes = []

        for page in PDFPage.create_pages(document):

            interpreter.process_page(page)


            #Accept every page's result that has been read in

            layout=device.get_result()

            for x in layout:

                if(isinstance(x, LTTextBoxHorizontal)):

                    # with open('a.txt','a') as f:

                    pageText += x.get_text().encode('utf-8')

            
            #Check to see if the document has reference

            ref_loc = re.search(r'REFERENCES.*|\n\[1\]', pageText)

            if ref_loc:

                pageText = pageText[0:ref_loc.start()]

             # Replace all the e-mail content into a space

            pdelmail = re.compile(r'\s*.*@.*\s*')

            text_del_email = pdelmail.sub(" ", pageText)

            #Replace all the illegal strings into a space

            p = re.compile(r'[^a-z|^A-Z|^\']')

            pageText = p.sub(" ", text_del_email)

            #delete all single characters

            pdelvalp = re.compile(r'\s.\s')

            pageText = pdelvalp.sub(" ", pageText)




            # Return the deleted space result to pageTXT

            p2 = re.compile(r'\s+')

            one_page = p2.split(pageText)



            len_data = len(one_page)

            for i in range(0, len_data):

                if len(one_page[len_data - i - 1]) > 0:

                    if d.check(str(one_page[len_data - i - 1])) == False:

                        del one_page[len_data - i - 1]



            len_data = len(one_page)

            for i in range(0, len_data):

                if len(one_page[len_data - i - 1]) == 1:

                    del one_page[len_data - i - 1]



            len_data = len(one_page)

            for i in range(len_data):

                one_page[i] = one_page[i].lower()



            for i in range(0, len_data):

               if one_page[len_data - i - 1] in DEL_WORDS:

                   del one_page[len_data - i - 1]

            pageText = " ".join(one_page)



            ngrams = getNgrams(pageText, choose)

            ngramsRes.append(ngrams)

            pageText=''

    #print ngramsRes

    WHITELIST = get_same_data(ngramsRes)

    #print WHITELIST



    fp.close()

    return



#Store the pdf content into txt to the current directory

def convertTotxt(pdf, outfile):

    debug = 0

    pagenos = set()

    password = ''

    maxpages = 0

    rotation = 0

    codec = 'utf-8'  # output code

    caching = True

    imagewriter = None

    laparams = LAParams()



    PDFResourceManager.debug = debug

    PDFPageInterpreter.debug = debug



    rsrcmgr = PDFResourceManager(caching=caching)

    outfp = file(outfile, 'w')


    #PDF conversion

    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,

                           imagewriter=imagewriter)



    # print(pdf)

    fp = file(pdf, 'rb')

    interpreter = PDFPageInterpreter(rsrcmgr, device)

    #Process every page's content in the document object

    for page in PDFPage.get_pages(fp, pagenos,

                                  maxpages=maxpages, password=password,

                                  caching=caching, check_extractable=True):

        page.rotate = (page.rotate + rotation) % 360

        interpreter.process_page(page)



    fp.close()

    device.close()

    outfp.close()



#Use the obtained whitelist and blacklist to anlayze the content, then get the higher frequency words

def analyseFile(pdf, outfile, chose):

    d = enchant.Dict("en_US")

    global BLACKLIST

    global DEL_WORDS

    convertTotxt(pdf, outfile)



    f = open("del.dat")

    line = f.readline()

    all_word = line.strip().split(" ")

    all_word = set(all_word)

    all_word = list(all_word)

    DEL_WORDS = all_word



    print("creating whiteList...")

    createWhiteList(pdf, int(chose))



    all_the_text = open(outfile).read()


    #Neglect the content for the reference section

    ref_loc = re.search(r'REFERENCES.*|\n\[1\]', all_the_text)

    if ref_loc:

        all_the_text = all_the_text[0:ref_loc.start()]


    #Replace all the emails into space

    pdelmail = re.compile(r'\s*.*@.*\s*')

    text_del_email = pdelmail.sub(" ", all_the_text)

  
    #Replace all the illegal strings into space

    p = re.compile(r'[^a-z|^A-Z|^\']')

    text = p.sub(" ", text_del_email)




    #Split every word in the content from the document by space

    p2 = re.compile(r'\s+')

    all_data = p2.split(text)



    len_data = len(all_data)

    for i in range(0, len_data):

        if len(all_data[len_data - i - 1]) > 0:

            if d.check(str(all_data[len_data - i - 1])) == False:

                del all_data[len_data - i - 1]




    # Delete the single character in the document

    len_data = len(all_data)

    for i in range(0, len_data):

        if len(all_data[len_data - i - 1]) == 1:

            del all_data[len_data - i - 1]



    len_data = len(all_data)

    for i in range(len_data):

        all_data[i] = all_data[i].lower()



    for i in range(0, len_data):

        if all_data[len_data - i - 1] in DEL_WORDS:

            del all_data[len_data - i - 1]

    all_the_text = " ".join(all_data)





    ngrams = getNgrams(all_the_text, int(chose))

    global WHITELIST

    global WHITELIST_ALL

    print("whiteList is :")

    print(WHITELIST)

    ngramRess = []

    ngramRes = []





    # print(ngrams)




    #The blacklist filtration

    for item in ngrams:

        for m in range(len(item)):

            item[m] = item[m].lower()

        if (len(list(set(item).intersection(set(BLACKLIST)))) == 0):

            ngramRess.append(item)




    # whitelist filtration

    # for item in ngramRess:

    #     # print(item)

    #     if (len(list(set(item).intersection(set(WHITELIST)))) == 0):

    #         ngramRes.append(item)




    #Use dictionary to count the words appearing times

    dic = {}

    for item in ngramRess:

        # print(item)

        if ','.join(item) in dic.keys():

            dic[','.join(item)] += 1

        else:

            dic[','.join(item)] = 1

    # print(dic)




    #Whitelist filtration

    for k in dic.keys():

        for v in WHITELIST:

            if k == v:

                del(dic[k])

        # print k,type(k)

        # print dic[k],type(dic[k])

        # if (len(list(set(item).intersection(set(WHITELIST)))) == 0):

        #     ngramRes.append(item)




    #Store the filtered results in the txt with descendening order

    res = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    wfile = open(pdf + '.result.txt', "w")

    for m in range(len(res)):

        if res[m][1] >= 2:

            wfile.write(str(res[m]))

            WHITELIST_ALL.append(str(res[m]))

    wfile.close()



    print("result is :")



    for m in range(len(res)):

        if res[m][1] >= 2:

            print res[m],



    print



if __name__ == '__main__':

    main()

    fwhite = open("all_white.txt","w")

    all_white = list(set(WHITELIST_ALL))

    all_whitestr = ' '.join(all_white)

    fwhite.write(all_whitestr)

    fwhite.close()



# Example in windows directory
# if __name__ == '__main__' : main(r'D:\aaa\Dumond-2009-Evaluation of Terrain Parameter Es.pdf')


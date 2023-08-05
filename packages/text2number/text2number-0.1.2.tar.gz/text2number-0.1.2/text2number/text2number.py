#text2number
from updates import *


class text2integer:

    def __init__(self):
        pass
    
    def text2int(self,textnum, numwords={},scales_use=None):
        """
        Text to numbers conversion function
        """
        if not numwords:
            units = [
                    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                    "sixteen", "seventeen", "eighteen", "nineteen",
                ]

            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

            scales_eng = ["hundred", "thousand","million", "billion", "trillion"]
            scales_hindi =["sau","thousand","lakh","crore"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):    numwords[word] = (1, idx)
            for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
            if scales_use=="en":
                for idx, word in enumerate(scales_eng):   numwords[word] = (10 ** (idx * 3 or 2), 0)
                
            elif scales_use=="hi":
                for idx, word in enumerate(scales_hindi):
                    if idx in [0,1]:
                        numwords[word] = (10 ** (idx * 3 or 2), 0)
                    else:
                        numwords[word] = (10 ** ((idx * 3 or 2)-1), 0)
                numwords['hazaar'] = (1000,0)
                numwords['sadhe'] = (1,0.5)
                numwords['point'] = (1,.0)
                numwords['thousand'] =(1000,0)
                numwords['tees'] = (1,30)
                numwords['nau'] =(1,9)
                numwords['chaar'] = (1,4)
                numwords['chaunsath'] =(1,64)
                numwords["dhai"] =(1,2.5)
                numwords["dedh"] =(1,1.5)
                numwords['barah']=(1,12)
                numwords['hundred'] = (1,100)
                numwords["lakhs"] = (100000,0)
                numwords['pachchees']=(1,25)
                numwords['ikkatis'] =(1,31)
                numwords['sau'] =(1,100)
                numwords['pichaasi'] =(1,85)
                numwords['sattaanave'] =(1,97)
                numwords.update(update_dict)

                        
            else:
                raise Exception("Language not yet configured")
        
        splits = textnum.split(' ')
        if 'sadhe' in splits and splits.index('sadhe')>0:
            if splits[splits.index('sadhe')-1] in list(numwords.keys()) and splits[splits.index('sadhe')+1] in list(numwords.keys()):
                splits =splits[1:]
                textnum = ' '.join(splits)
        else:
            textnum = ' '.join(splits)
        current = result = 0
        for word in textnum.split():
            if splits[splits.index(word)-1]=='point':
                orig_wrd = numwords[word][1]
                numwords[word] = (1,float(str(0)+'.'+str(orig_wrd)))
                
            if word not in numwords:
                print("Not found: ",word)
            #     raise Exception("Illegal word: " + word)
            # #         import pdb;pdb.set_trace()
            else:

                scale, increment = numwords[word]
                        
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0

        return result + current


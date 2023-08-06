from os import system

def numLetterFinglishi (num_):
    yekan={'0':'', '1':'Yek','2':'Do','3':'Seh','4':'Chahar','5':'Panj','6':'Shesh','7':'Haft','8':'Hasht','9':'Noh'}

    dahgan={'0':'Dah','1':'Yazdah','2':'Davazdah','3':'Sizdah','4':'Chahardah'
    ,'5':'Panzdah','6':'Shanzdah','7':'Hefdah','8':'Hejdah','9':'Noozdah'}

    dahgan2={'0':'', '2':'Bist','3':'Si','4':'Chehel','5':'Panjah','6':'Shast'
    ,'7':'Haftad','8':'Hashtad','9':'Navad'}

    sadgan={'0':'', '1':'YekSad','2':'Devist','3':'SiSad','4':'ChaharSad','5':'PanSad'
    ,'6':'SheshSad','7':'HaftSad','8':'HashtSad','9':'NohSad'}

    hezargan={'0':'', '1':'Hezar','2':'Million','3':'Billion','4':'Trillion','5':'Quadrillion'
    ,'6':'Quintillion','7':'Sextillion','8':'Septillion','9':'Octillion','10':'Nonillion','11':'Decillion'
    ,'12':'Undecillion','13':'Duodecillion','14':'Tredecillion','15':'Quattuordecillion','16':'Quindecillion'
    ,'17':'Sexdecillion','18':'Septen-decillion','19':'Octodecillion','20':'Novemdecillion','21':'Vigintillion'}
    tmpnum=num_
    listDict=[sadgan,dahgan2,yekan,dahgan]
    while True:
        
        
        if tmpnum==0: 
            print ('Sefr')
            break
        digits=[]
        leng=len(str(num_))
        while num_!=0:
            digits.append(str(num_%1000))
            num_ //= 1000
        digits.reverse()
        numletter=[]

        for j in range (len(digits)):
            digitList=[]
            lenDigit=len(digits[j])
            for i in range (lenDigit):
                digitList.append(digits[j][i])
                if len(digits[j])>2 and digits[j][1]=='1' and i==0:
                    numletter.append([listDict[i*3][digitList[i]],' o '])
                elif len(digits[j])>2 and digits[j][1]=='1' and i==1:
                    numletter.append([listDict[i*3][digitList[i]],' '])
                    if i==1:
                        break 
                elif digits[j][0]=='1' and len(digits[j])==2:
                    numletter.append([listDict[3][digits[j][1]],' '])
                    break
                else:
                    if i != len(digits[j])-1 :
                        if digitList[i]=='0' or int(digits[j])%100==0:
                            numletter.append([listDict[abs(lenDigit-3-i)][digitList[i]],''])
                        elif i==1 and int(digits[j][2])==0:
                            numletter.append([listDict[abs(lenDigit-3-i)][digitList[i]],''])
                        elif len(digits[j])==2 and digits[j][1]=='0':
                            numletter.append([listDict[abs(lenDigit-3-i)][digitList[i]],' '])                    
                        else:
                            numletter.append([listDict[abs(lenDigit-3-i)][digitList[i]],' o '])
                    else:
                        numletter.append([listDict[abs(lenDigit-3-i)][digitList[i]],' '])
            if j != len(digits)-1 and digitList !=['0'] and digits[len(digits)-1] !='0':
                numletter.append([hezargan.get(str(len(digits)-1-j)),' o '])
            elif j != len(digits)-1 and digitList !=['0'] and digits[len(digits)-1] =='0':
                numletter.append([hezargan.get(str(len(digits)-1-j))])
            newlist = [item for sublist in numletter for item in sublist]
        while '' in newlist:
            newlist.remove('')
        while ' ' in newlist:
            newlist.remove(' ')
        break
    numletter1=" ".join(newlist)
    return numletter1
    


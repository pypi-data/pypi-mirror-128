def NumToWord (number):

    units_digit = {0:'', 1:'یک',2:'دو',3:'سه',4:'چهار',5:'پنج',6:'شش',7:'هفت', 8:'هشت',9:'نه'}
    tens_digit1 = {0:'ده',1:'یازده', 2:'دوازده',3:'سیزده',4:'چهارده'
    ,5:'پانزده',6:'شانزده',7:'هفده',8:'هجده',9:'نوزده'}
    tens_digit2 = {0:'', 2:'بیست',3:'سی',4:'چهل',5:'پنجاه',6:'شصت'
    ,7:'هفتاد',8:'هشتاد',9:'نود'}
    hundreds_digit = {0:'', 1:'صد',2:'دویست',3:'سیسصد',4:'چهارصد',5:'پانصد'
    ,6:'ششصد',7:'هفتصد',8:'هشتصد',9:'نهصد'}
    decimal = {0:'', 1:'هزار',2:'میلیون',3:'میلیارد',4:'	بیلیون',5:'بیلیارد'
    , 6:'	تریلیون', 7:'تریلیارد', 8:'کوآدریلیون', 9 :'کادریلیارد', 10 :'کوینتیلیون',
    11:'کوانتینیارد', 12:'سکستیلیون', 13:'سکستیلیارد', 14:'سپتیلیون',
    15:'سپتیلیارد', 16:'اکتیلیون', 17:'اکتیلیارد', 18:'	نانیلیون'
    , 19:'نانیلیارد', 20:'دسیلیون', 21:'دسیلیارد', 22:'آندسیلیون', 
    23:'آندسیلیارد',24:'دودسیلیون',25:'دودسیلیارد',26:'تریدسیلیون',27:'تریدسیلیارد',
    28:'کوادردسیلیون',29:'کوادردسیلیارد',30:'	کویندسیلیون',31:'کویندسیلیارد',
    32:'	سیدسیلیون',33:'	سیدسیلیارد',34:'گوگول'}

    #-----------------------------------------------------------------------------------------------------------------------

    list_1 = list()
    list_2 = list()

    if number == 0 :
        print('صفر')

    else:
        while number != 0:
            res = number % 1000
            list_1.append(res)
            number = number // 1000


        for i in range(len(list_1)) :
        
            if list_1[i] != 0:
                list_2.append(decimal.get(i))

            j = 1

            while list_1[i] != 0 :
                res = list_1[i] % 10
                
                if j == 1 :
                    z = res
                    list_2.append(units_digit.get(res))

                elif j == 2 and res == 1:
                    list_2[-1] = ''
                    list_2.append(tens_digit1.get(z))

                elif j == 2 and res > 1 or res == 0:
                    list_2.append(tens_digit2.get(res))
                
                elif j == 3:
                    list_2.append(hundreds_digit.get(res))
                
                list_1[i] = list_1[i] // 10
                j += 1

        while '' in list_2:
            list_2.remove('')

        list_2.reverse()
        list_3 = list()

        for i in range(len(list_2)):
            if i < len(list_2)-1:

                if list_2[i+1] in decimal.values():
                    list_3.append(list_2[i])

                else:
                    list_3.append(list_2[i])
                    list_3.append('و')
                    
            else:
                list_3.append(list_2[i])
        
        
    word =" ".join(list_3)
    return word


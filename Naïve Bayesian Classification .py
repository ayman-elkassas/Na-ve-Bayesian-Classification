import numpy as np
import xlrd
import math

class NaiveBayesianClassifier:

    sheet=0
    attributes=[]
    pattern=[]

    classes_values=[]
    percentage_classes=[]
    prior_info_classes=[]
    liklihood={}

    numeric_x=[]

    res={}


    def __init__(self):

        workbook=xlrd.open_workbook('dataset.xlsx')
        self.sheet=workbook.sheet_by_index(0)

        self.Naiveclassifier()

        return

    def Naiveclassifier(self):

        #TODO:GET ALL ATTRIBUTE IN EXCEL SHEET
        for j in range(self.sheet.ncols):
            try:
                if(str.isidentifier(self.sheet.cell_value(0,j))):
                    self.attributes.append(self.sheet.cell_value(0,j))
            except:
                print("Incorrect input attribute...")
                return

        #TODO:GET PATTERN VALUES
        self.get_pattern()

        #TODO:COMPUTE PRIOR INFO
        self.compute_prior_info()

        #TODO:COMPUTE POSTROIR PROBABITILY
        for i in range(len(self.classes_values)):
            val = self.classes_values[i]
            self.liklihood[val] = []
            self.computeLiklihood(0,i,1)

            self.res[val]=self.liklihood.get(val)*self.prior_info_classes[i]

        self.getResult()

    def get_pattern(self):
        print("Please enter your pattern attributes values : ")

        for j in range(self.sheet.ncols):

            if(j==self.sheet.ncols-2):
                return
            val=input(self.attributes[j+1]+" :")
            flag=str.isnumeric(val)

            if(flag==True):
                self.pattern.append(float(val))
            else:
                self.pattern.append(str(val))

    def compute_prior_info(self):
        counter=0
        num=int(input("enter number of classes : "))
        for j in range(num):
            val=str.strip(input("class "+str(j+1)+" value : "))
            self.classes_values.append(val)

        for num_classes in range(len(self.classes_values)):
            for i in range(1,self.sheet.nrows):
                if(self.sheet.cell_value(i,(self.sheet.ncols-1))==self.classes_values[num_classes]):
                    counter=counter+1
            self.prior_info_classes.append(counter/(self.sheet.nrows-1))
            self.percentage_classes.append(counter)
            counter=0

    def computeLiklihood(self,att_index_in_pattern,classIndex,res):

        counter=0
        val = self.classes_values[classIndex]
        if(att_index_in_pattern==len(self.pattern)):
            self.liklihood[val]=res
            return
        else:
            for i in range(1,self.sheet.nrows):
                if(self.sheet.cell_value(i,att_index_in_pattern+1)==self.pattern[att_index_in_pattern] and self.sheet.cell_value(i,self.sheet.ncols-1)==val):
                    # TODO:DO IF NUMERIC ATRRIBUTE
                    if(str.isnumeric(self.sheet.cell_value(i,att_index_in_pattern+1))):
                        self.numeric_x.append(self.sheet.cell_value(i,att_index_in_pattern+1))
                    else:
                        counter=counter+1
            if(counter==0):
                gaussian_liklihood=((1)/(math.sqrt(2*(22/7))*math.sqrt(np.var(self.numeric_x))))*np.exp((-(math.pow((self.numeric_x-np.mean(self.numeric_x)),2)))/(2*math.pow(math.sqrt(np.var(self.numeric_x)),2)))
                res = res *gaussian_liklihood
            else:
                res=res*(counter / self.percentage_classes[classIndex])
            return self.computeLiklihood(att_index_in_pattern+1,classIndex,res)

    def getResult(self):
        values=list(self.res.values())
        keys=list(self.res.keys())

        m=max(values)
        i=values.index(m)
        print("Then this pattern classified to class : "+keys[i])

NaiveBayesianClassifier()
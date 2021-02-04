class Opcode():
    def __init__(self, name, code):
        self.name=name
        self.code=code

class Label():
    def __init__(self,name,Address):
        self.name=name[:-1]
        self.Address=str(Address)

class Symbol():
    def __init__(self,name,value,Address,size=4):
        self.name=name
        self.value=str(value)
        self.Address=str(Address)
        self.size=str(size)

class Literal():
    def __init__(self,name,Address,value,size=4):
        self.name=name
        self.size=str(size)
        self.Address=str(Address)
        self.value=str(value)

class Instruction():
    def __init__(self,Opcode, Operand,lno,Address):
        self.Opcode=Opcode
        self.Operand=Operand
        self.lno=lno
        self.Address=Address

class Data():
    def __init__(self,name,Address,value,size=4):
        self.name=name
        self.size=str(size)
        self.Address=str(Address)
        self.value=str(value)

end=False
lno=0
LC=0
print("Do you wish to provide the path?(1:YES, 0:NO)")
a=input()
if(a=="1"):
    print("What should be the input path : ")
    InputPath=input();
else:
    InputPath=r"Input.txt"
OutputPath=r"Output.txt"

def get_bin(a):
    a=bin(a)
    a=a[2:]
    l=len(a)
    if(l==1):
        a="00000000"
    elif(l==2):
        a="000000"+a
    elif(l==3):
        a="00000"+a
    elif(l==4):
        a="0000"+a
    elif(l==5):
        a="000"+a
    elif(l==6):
        a="00"+a
    elif(l==7):
        a="0"+a
    return a

MOTable=[Opcode("CLA","0000"),Opcode("LAC","0001"),Opcode("SAC","0010"),
Opcode("ADD","0011"),Opcode("SUB","0100"),Opcode("BRZ","0101"),
Opcode("BRN","0110"),Opcode("BRP","0111"),Opcode("INP","1000"),Opcode("DSP","1001"),
Opcode("MUL","1010"),Opcode("DIV","1011"),Opcode("STP","1100")]

def Is_BR(a):
    if(a=="0110" or a=="0101" or a=="0111"):
        return True
    return False

def Print_MOT():
    print("___MOT___")
    for m in MOTable:
        print(m.name+" # "+m.code)

LabelTable=[]

def Print_Labels():
    print("___LABELS___")
    for l in LabelTable:
        print(l.name+" # "+l.Address)

def GiveLabel(a):
    for l in LabelTable:
        if(l.name==a):
            return l.Address
    return "ERROR"

def Label_Repeat(Word):
    for l in LabelTable:
        if(l.name==Word):
            return True
    return False

def check_Label(a):
    global lno,LC
    if(a==""):
        return True
    if(a[-1]==':'):
        x=Label_Repeat(a)
        y=FindOpcode(a[:-1])
        if(y!="ERROR"):
            Errors.append("Invalid Label name in line : "+str(lno))
        elif(x==True):
            Errors.append("Repeated Label in line : "+str(lno))
        else:
            x=get_bin(LC)
            LabelTable.append(Label(a,x))
        return True
    return False

SymbolTable=[]

def Print_Symbols():
    print("___SYMBOLS TABLE___")
    for s in SymbolTable:
        print(s.name+" # "+str(s.size)+" # "+s.Address+" # "+s.value)

def SymbolRepeat(a):
    global lno,LC
    for s in SymbolTable:
        if(s.name==a):
            return True
    return False

def AddSymbol(a,b=0):
    global lno,LC
    bool=SymbolRepeat(a)
    if(bool):
        Errors.append("Repeated Symbol in line : "+str(lno))
    else:
        x=get_bin(LC)
        s=Symbol(a,b,x)
        SymbolTable.append(s)
        LC+=4

def GiveSymbol(a):
    for sym in SymbolTable:
        if(sym.name==a):
            return sym.Address
    return "ERROR"

LiteralTable=[]

def Print_Literals():
    print("___LITERALS TABLE___")
    for l in LiteralTable:
        print(l.name+" # "+l.size+" # "+l.Address+" # "+l.value)

def LiteralRepeat(a):
    global lno,LC
    for l in LiteralTable:
        if(l.name==a):
            return True
    return False

def AddLiteral(a,b=0,c=4):
    global lno,LC
    bool=LiteralRepeat(a)
    if(bool):
        Errors.append("Repeated Literal in line : "+str(lno)+" -> "+a)
    else:
        x=get_bin(LC)
        l=Literal(a,x,b,c)
        LiteralTable.append(l)
        LC+=int(l.size)

def GiveLiteral(a):
    for l in LiteralTable:
        if(l.name==a):
            return l.Address;
    return "ERROR"

DataTable=[]

def Make_Data_Table():
    global LiteralTable,SymbolTable,DataTable
    for l in LiteralTable:
        DataTable.append(Data(l.name,l.Address,l.value,l.size))
    for s in SymbolTable:
        DataTable.append(Data(s.name,s.Address,s.value,s.size))

def Print_Data():
    global DataTable
    print("__DATA TABLE__")
    for d in DataTable:
        print(d.name+" # "+d.size+" # "+d.Address+" # "+d.value)

InTable=[]

def Print_Instructions():
    print("___INSTRUCTIONS___")
    for i in InTable:
        print(str(i.Address)+" "+i.Opcode+" "+i.Operand)

Errors=[]

def Print_Errors():
    print("___ERRORS___")
    for e in Errors:
        print(e)

def FindOpcode(Word):
    i=-1
    for op in MOTable:
        i+=1
        if(op.name==Word):
            return op.code
    return "ERROR"

def One_Word(l):
    global end,lno,LC
    if(l=="START"):
        LC= -12
    elif(l=="END"):
        end=True
        LC-=12
    else:
        x=FindOpcode(l)
        if(x=="ERROR"):
            Errors.append("Invalid Opcode in line : "+str(lno)+" -> "+l)
        else:
            InTable.append(Instruction(x,"",lno,LC))

def Two_Word(a,b):
    global end,lno,LC
    if(a=="START"):
        b=int(b)
        LC += b
        LC -= 12
    elif(a=="END"):
        end=True
        LC-=12
    else:
        x=FindOpcode(a)
        if(x=="ERROR"):
            Errors.append("Invalid Opcode in line : "+str(lno)+" -> "+a+" "+b)
        else:
            InTable.append(Instruction(x,b,lno,LC))

def Error_in_Table():
    for i in InTable:
        a=i.Opcode
        b=i.Operand
        c=str(i.lno)
        if(a=="0000"  or a=="1100"):
            if(b!=""):
                Errors.append("Incorect no. of opcodes in line -> "+c)
        else:
            if(b==""):
                Errors.append("Incorect no. of opcodes in line -> "+c)
            if(Is_BR(a)):
                if(Label_Repeat(b)==False):
                    Errors.append("Wrong label in line -> "+c)
                if(LiteralRepeat(b)==True):
                    Errors.append("Literal cannot be used as label in line -> "+c)
                elif(SymbolRepeat(b)==True):
                    Errors.append("Symbol cannot be used as label in line -> "+c)
            else:
                if(Label_Repeat(b)==True):
                    Errors.append("Label cannot be used as variable in line -> "+c)
                if((LiteralRepeat(b) or SymbolRepeat(b))==False):
                    Errors.append("Invalid Symbol/Literal in line -> "+c)
    return

def First_Pass():
    global end,LC,lno
    file = open(InputPath)
    data=file.read()
    lines=data.split('\n')
    LC=0
    lno=1
    for line in lines :
        l=line.split(" ")
        c=len(l)
        if(c==1):
            l=l[0]
            bool=check_Label(l)
            if(l==""):
                pass
            elif(l[0]=="#"):
                pass
            elif(bool==False):
                if(end==True):
                    Errors.append("Line occuring after END statement -> "+str(lno))
                else:
                    One_Word(l)
                    LC+=12
        elif(c==2):
            a=l[0]
            b=l[1]
            bool=check_Label(a)
            if(a[0]=="#"):
                pass
            elif(b[0]=="#"):
                bool=check_Label(a)
                if(bool==False):
                    if(end==True):
                        Errors.append("Line occuring after END statement -> "+str(lno))
                    else:
                        One_Word(a)
                        LC+=12
            elif(bool):
                if(end==True):
                    Errors.append("Line occuring after END statement -> "+str(lno))
                else:
                    One_Word(b)
                    LC+=12
            else:
                if(a=="DC" or a=="DS"):
                    if(end!=True):
                        Errors.append("Variable declared before END statement in line "+str(lno))
                    elif(a=="DS"):
                        AddSymbol(b)
                    else:
                        AddLiteral(b)
                else:
                    if(end==True):
                        Errors.append("Line occuring after END statement -> "+str(lno))
                    else:
                        Two_Word(a,b)
                        LC+=12
        else:
            a=l[0]
            b=l[1]
            c=l[2]
            if(a[0]=="#"):
                pass
            elif(b[0]=="#"):
                bool=check_Label(a)
                if(bool==False):
                    if(end==True):
                        Errors.append("Line occuring after END statement -> "+str(lno))
                    else:
                        One_Word(a)
                        LC+=12
            elif(c[0]=="#"):
                if(bool):
                    if(end==True):
                        Errors.append("Line occuring after END statement -> "+str(lno))
                    else:
                        One_Word(b)
                        LC+=12
                else:
                    if(a=="DC" or a=="DS"):
                        if(end!=True):
                            Errors.append("Variable declared before END statement in line "+str(lno))
                        elif(a=="DS"):
                            AddSymbol(b)
                        else:
                            AddLiteral(b)
                    else:
                        if(end==True):
                            Errors.append("Line occuring after END statement -> "+str(lno))
                        else:
                            Two_Word(a,b)
                            LC+=12
            elif(a=="DC" or a=="DS"):
                if(end!=True):
                    Errors.append("Variable declared before END statement in line "+str(lno))
                elif(a=="DS"):
                    AddSymbol(b,c)
                else:
                    AddLiteral(b,c)
            else:
                if(end==True):
                    Errors.append("Line occuring after END statement -> "+str(lno))
                else:
                    bool=check_Label(a)
                    if(bool==False):
                        Errors.append("Error in line : "+str(lno))
                    else:
                        Two_Word(b,c)
                    LC+=12
        lno+=1;

    Error_in_Table()
    if(end==False):
        Errors.append("END statement not found")

def Second_Pass():
    global lno,LC,InTable
    file=open(OutputPath,"w")
    for line in InTable:
        sym=line.Operand
        op=line.Opcode
        if(LiteralRepeat(sym)):
            a=GiveLiteral(sym)
        elif(SymbolRepeat(sym)):
            a=GiveSymbol(sym)
        elif(op=="0000"):
            a=""
        elif(Is_BR(op)):
            a=GiveLabel(sym)
        else:
            a="  ERROR"
        line.Operand=a
        file.write(line.Opcode+" "+line.Operand+"\n")


First_Pass()
Make_Data_Table()

if(Errors==[]):
    Second_Pass()
else:
    file=open(r"C:\Users\shriv\Desktop\Output.txt","w")
    for e in Errors:
        file.write(e+"\n")

Print_MOT()
Print_Labels()
Print_Symbols()
Print_Literals()
Print_Data()
Print_Errors()
Print_Instructions()

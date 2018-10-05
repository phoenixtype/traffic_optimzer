import sys
import re
streetDic = dict()
vertxDic = dict()
graph = dict()
linesDic = list()
vertxTempStore = dict()
vertexCount = 0
edgeDic = dict()
class Vertx(object):
    def __init__(self, x:float, y:float, intercept = False):
        self.x = x
        self.y = y
        self.intercept = intercept
    def __str__(self):
        return '<'+str(self.x)+','+str(self.y)+'>'

class Street(object):
    def __init__(self, name:str, line : list):
        self.name = name
        self.lineSegments = line
        pass

    def __str__(self):
        return self.name

    
class Line(object):
    def __init__ (self, src, dst):
        self.src = src
        self.dst = dst
        self.vertxAlong = []
        # this is gradient y2 - y1/x2 - x1
        y2 = float(dst[1])
        y1 = float(src[1])
        x2 = float(dst[0])
        x1 = float(src[0])
        try:
            self.grad = (y2 - y1)/(x2 - x1)
            pass
        except ZeroDivisionError:
            self.grad = -100
            pass
        # constant c = y - mx
        self.constant = y1 - (self.grad * x1)
        pass

def main():
     while True:
        try:
            line=sys.stdin.readline().strip();
            if line =="":
               break  
            if line =="\0":
               break    
            if line.startswith('a'):
               newStreet = parse(line)
               add(newStreet)
            elif line.startswith('c'):
               newStreet=parse(line)
               change(newStreet)
            elif line.startswith('r'):
                line = str(line)
                line.split(" ")
                parse_remove(line[1])
        except Exception as error:
               print(error)
     sys.exit(0)


def parse(line):
    # getting the street name in string form
    streetna=re.findall(r"\s\"(.*)\"\s",line)
    # getting the list of coords in string form.  
    coord=re.findall(r"\(\-?[0-9]+\,\-?[0-9]+\)",line)
    #error checks
    check_streetna="".join(streetna)+"".join(coord)
    check_streetna=check_streetna.replace(" ","")
    lines = []
    if len(coord)<=1:
        raise Exception ("Error:At least two point to build a street.")
    for i in range (0,len(coord) - 1):
        if eval(coord[i + 1]):
            src = eval(coord[i])
            dst = eval(coord[i + 1])
        else:
            break
        seg = Line(src, dst)
        lines.append(seg)
    if line.replace(" ","").replace("\"","")[1:]!=check_streetna:
       print("Error:Unrecognize command.")
       return("","")
    if len(streetna)!=1:
       print("Error:Wrong street name.")
       return("","")
    else:
        streetna=streetna[0]
##    print(streetna)
    if not coord:
        print ("Error:No route.")
    return Street(streetna, lines)


def parse_remove(streetName : str):
    if streetName not in streetDic:
        print("Error: The street you are about to delete, does not exists")
    else:
        del streetDic[streetName]
    pass

def change(street : Street):
    if  street:
        try:
            if street.name not in streetDic:
               raise Exception ("Error:This street doesn't exsit.")
            streetDic[street.name] = street
        except Exception as error:
             print(error)

def add(street : Street):
    if  street:
        try:
          if street.name in streetDic:
             raise Exception ("Error:This street has already exist.")
             ##         print(streetna)
          streetDic[street.name] = street
    ##      print store.dic
        except Exception as error:
             print(error)

def graphOutput():
    streets = streetDic.values()
    keys = list(streetDic.keys())
    for i in range(0,len(streets) - 1):
        street = streets[i] # A street type
        streetName = keys[i]
        for m in range(0,len(street.lineSegments) - 1):
            line = street.lineSegments[m]
            line.name = streetName + str(m)
            # it comapare the lines of the immediate street
            for z in range(i + 1, len(streets) - 1):
                immediateStreet = streets[z]
                secondStreetName = keys[z]
                for n in range(0, len(immediateStreet.lineSegments) - 1):
                    #check if the are parallel, which means if their gradient are equal
                    line2 = immediateStreet.lineSegments[n]
                    line2.name = secondStreetName + str(n)
                    if line.grad is line2.grad :
                        continue
                    else:
                     intersept(line, line2)

def intersept(l1 : Line, l2 : Line) :
    # parellel lines cannot intercept each
    if l1.grad == -100 :
        #actually means undefined
        x = l1.src[0]
        y = (l2.grad * x) + l2.constant
    elif l2.grad == -100 :
        x = l2.src[0]
        y = (l1.grad * x) + l1.constant
    else:
        x = (l2.constant - l1.constant)/(l1.grad - l2.grad)
        # if x is in range between the two lines
        if (l1.src[0] <= x <= l1.dst[0]) or l2.src[0] <= x <= l2.dst[0]:
            y = (l1.grad * x) + l1.constant
    if str((x,y)) not in vertxTempStore:
        vertxTempStore[str((x,y))] = (x,y)
        if l1.name not in linesDic:
            l1.vertxAlong.append((x,y))
            linesDic[l1.name] = l1
        if l2.name not in linesDic:
            l2.vertxAlong.append((x,y))
            linesDic[l2.name] = l2

def computeEdges():
    for lineName in linesDic:
        line = linesDic[lineName]
        v = (line.src[0], line.src[1])
        for idx in range(-1, len(line.vertxAlong) - 1) :
            if idx == len(line.vertxAlong) - 1:
                nxtVtx = (line.dst[0], line.dst[1])
                edgeName = str(v) + str(nxtVtx)
                if edgeName not in edgeDic:
                    edgeDic[edgeName] = (v, nxtVtx)
                    break
            nxtVtx = line.vertxAlong[idx + 1]
            edgeName = str(v) + str(nxtVtx)
            if edgeName not in edgeDic:
                edgeDic[edgeName] = (v, nxtVtx)
                pass
            v = nxtVtx


if __name__=='__main__':
     main()
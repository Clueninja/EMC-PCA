import random
windowX=20
windowY=10
#stores all prob [sum of adjacent cells][current state of cell]
states = [0,1,2]
#prob of changing from 1-2
#prob of changing from 0-1
#prob of changing from 2-0

# IN FORM [majority state eg 1][current cell state eg 1][future cell state eg 0]
#returns probabilty of transitioning from current cell to future cell
def MajorityTransMatrix(majoritystate,currentstate,p,q,z):
    MAJORITYTRANS = [
        [[1,0,0],
         [1-q,q,0],
         [1,0,0]],
        
        [[p,1-p,0],
         [p,1-p,0],
         [1,0,0]],
        
        [[1,0,0],
         [0,1-z,z],
         [1,0,0]]]
    return MAJORITYTRANS[majoritystate][currentstate]


syncspace = []
statespace = []
prestatespace =[]

def CheckStable():
	return True

def Majority(y,x,rule):
    numofstatecells = [0,0,0]
    if rule == "NEC" and x != 0 and x!=windowX-1 and y !=0 and y != windowY-1:
        numofstatecells[statespace[y-1][x]]+=1
        numofstatecells[statespace[y][x+1]]+=1
        numofstatecells[statespace[y][x]]+=1

    elif rule =="Moore" and x != 0 and x!=windowX-1 and y !=0 and y != windowY-1:
        numofstatecells[statespace[y-1][x]]+=1
        numofstatecells[statespace[y-1][x+1]]+=1
        numofstatecells[statespace[y][x+1]]+=1
        numofstatecells[statespace[y+1][x+1]]+=1
        numofstatecells[statespace[y+1][x]]+=1
        numofstatecells[statespace[y+1][x-1]]+=1
        numofstatecells[statespace[y][x-1]]+=1
        numofstatecells[statespace[y-1][x-1]]+=1
        numofstatecells[statespace[y][x]]+=1
        
    majoritycellstate = [0,0]
    for stateindex in range(0, len(numofstatecells)-1):
        if numofstatecells[stateindex] > majoritycellstate[0]:
            majoritycellstate[1] = stateindex
            majoritycellstate[0] = numofstatecells[stateindex]
            
    return majoritycellstate[1]
        
#updates center cell using adjacent cells
def updatestate(y,x, rule,p,q,z): 
    if rule == "NEC" and x != 0 and x!=windowX-1 and y !=0 and y != windowY-1:
        majoritycellstate = Majority(y,x,rule)
        futurecellstate = random.choices(states, weights = MajorityTransMatrix(majoritycellstate, statespace[y][x],p,q,z), k=1)[0]
        syncspace[y][x] = futurecellstate

    elif rule == "Neu"and x != 0 and x!=windowX-1 and y !=0 and y != windowY-1:
        sumofadjcells = statespace[y-1][x] + statespace[y][x+1] + statespace[y+1][x] + statespace[y][x-1]
        syncspace[y][x] = TRANSMATRIXNEU[sumofadjcells][statespace[y][x]]

    elif rule == "Moore"and x != 0 and x!=windowX-1 and y !=0 and y != windowY-1:
        majoritycellstate = Majority(y,x,rule)
        futurecellstate = random.choices(states, weights = MajorityTransMatrix(majoritycellstate, statespace[y][x],p,q,z), k=1)[0]
        syncspace[y][x] = futurecellstate
        
#assigns initial conditions to the syncspace, statespace is then updated
def initconditions():
    global prestatespace
    for _x in range (0,40):
        syncspace [random.randint(1,windowY-2)][random.randint(1,windowX-2)] = 1

    #windowX = 4
    #windowY = 8
    sync()
    prestatespace = statespace
    printstate()
    
#prints the current states of the statespace


def printstate():
    for i in range (0, windowY):
        output=""
        for j in range(0,windowX):
            output += str(statespace[i][j])
        print(output)
    print()

#syncs the statespace to the syncspace(sync space info could be deleted afterwards to ensure markov effect)
def sync(): 
    for i in range (0,windowY):
        for j in range (0, windowX):
            if (i == 0 or i==windowY-1 or j == 0 or j==windowX-1):
                syncspace[i][j] = 0
            statespace[i][j] = syncspace[i][j]

#passes over the statespace, updates next positions to syncspace, statespace updates, prints current states of cells
def onepass():
    for i in range(0, windowY):
        for j in range (0,windowX):
            #updatestate(i,j,"Moore")
            pass
    sync()
    #printstate()

#currently runs the game indefinetly basicly onepass() on steriods
def gameloop():
    global prestatespace
    p=0
    for _piter in range (0,10):
        p+=0.1
        q=0
        for _qiter in range (0,10):
            q+=0.1
            z=0
            for _ziter in range (0,10):
                z+=0.1
                end = False
                iterations= 0
                reset()
                initconditions()
                while end ==False:
                    iterations+=1
                    for i in range(0, windowY):
                        for j in range (0,windowX):
                            updatestate(i,j,"Moore",p,q,z)
                    sync()

                    if CheckStable():
                        printstate()
                        statespace = prestatespace
                        printstate()
                        print ("p = "+str(p)+" q = "+str(q)+" z = "+str(z)+" iterations = "+str(iterations))
                        end = True
        
        
    return 0

#sets up syncspace and statespace
def reset():
	for y in range (0,windowY):
		for x in range (0,windowX):
			syncspace[y][x] = 0
	sync()
	
def setup():
    for i in range (0,windowY):
        statespace.append([])
        syncspace.append([])
        for _j in range (0,windowX):
            statespace[i].append(0)
            syncspace[i].append(0)
        
if __name__ == "__main__":
    setup()
    #initconditions()
    gameloop()


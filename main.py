import time, random, ggb

# DEFINITIONS

def addPoint():
    P = Point(0,0)
    color = listColors[random.randint(0, len(listColors)-1)]
    P.color = color
    listPoints.append(P)
    listAuras.append(Circle(P, 0.25, color=color))
    scores.append(0)
    
    
def addFood():
    P = Point(random.randint(-5,5),random.randint(-5,5))
    P.color = 'white'
    listFoods.append(P)
    scores.append(0)
    
    
def updateAura():
    topScore = 0
    topPoint = listPoints[0]
    for point in listPoints:
        if scores[listPoints.index(point)] >= topScore:
            topScore = scores[listPoints.index(point)]
            topPoint = point
        
    print('Top Score:'+str(topScore))
        
    for aura in listAuras:
        if listAuras.index(aura) == listPoints.index(topPoint):
            aura.is_visible = True
            
        else:
            aura.is_visible = False
    
        

def catchGoal(point, goal):
    x = point.x
    y = point.y
    
    if goal.x == x and goal.y == y: pass
    else:
        if abs(x - goal.x) >= abs(y - goal.y):
            if goal.x < x:
                x -= 1
            else:
                x += 1
                
        elif abs(x - goal.x) < abs(y - goal.y):
            if goal.y < y:
                y -= 1
            else:
                y += 1
             
            
                
    return [x,y]

def iaPoints(point):
    x = point.x
    y = point.y
    indexPoint = listPoints.index(point)
    score = scores[indexPoint]
    goal = 'none'
    
    
    if Distance(point, centerPoint) > 4.5:
        goal = 'center'
    
    if len(listFoods) > 0:
        possibleFood = listFoods[0]
        for food in listFoods:
            if Distance(point, possibleFood) > Distance(point, food):
                possibleFood = food
        
        if Distance(possibleFood, point) < 5:
            goal = 'food'
    
    if Distance(centerPoint, bait) < 5.5:
        goal = 'bait'
    
    
    if goal == 'none':
        if random.randint(1,4) == 1:
            w = random.randint(1, 4)
            
            if w == 1:   x += 1
            elif w == 2: x -= 1
            elif w == 3: y += 1
            elif w == 4: y -= 1
            
    elif goal == 'center':
        values = catchGoal(point, centerPoint)
        x = values[0]
        y = values[1]
        
    elif goal == 'food':
        values = catchGoal(point, possibleFood)
        x = values[0]
        y = values[1]
        
    elif goal == 'bait':
        values = catchGoal(point, bait)
        x = values[0]
        y = values[1]

    for food in listFoods:
        if food.x == x and food.y == y:
            listFoods.remove(food)
            food.delete()
            score += 5
            print('Food Catched!')
    
    prevPoint = Point(point.x, point.y)
    
    point.x = x
    point.y = y
    
    trail = Segment(prevPoint, point, color = point.color)
    
    listTrails.append(trail)
    prevPoint.is_visible = False
    
    scores[indexPoint] = score
    

# VARIABLES

listColors = ['red','green','blue','orange','purple', 'black']
timeRefresh = 0.25
listPoints = []
listFoods = []
listTrails = []
listAuras = []
scores = []
nRefresh = 0
centerPoint = Point(0,0)
centerPoint.is_visible = False
bait = Point(-8,-3)
centerPoint.is_visible = False
circle = Circle(centerPoint,5.5, color = 'gray')
aura = Circle(centerPoint, 0.5)
aura.is_visible = False




print(dir('ggb'))




# WHILE

while True:
    
    for t in listTrails:
        t.is_visible = False
        pass
    
    listTrails = []
    
    if nRefresh % 5 == 0:
        if len(listPoints) < 5:
            addPoint()
            
        if len(listFoods) < 5:
            addFood()
        
    
    for point in listPoints:
        iaPoints(point)

    updateAura()
    
    nRefresh += 1
    print('Round '+str(nRefresh))
    time.sleep(timeRefresh)

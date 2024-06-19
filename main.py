import time, random, ggb

# DEFINITIONS

def addPoint():
    P = Point(0,0)
    color = listColors[random.randint(0, len(listColors)-1)]
    P.color = color
    listPoints.append(P)
    listAuras.append(Circle(P, 0.25, color=color))
    scores.append(0)
    
    
def killPoint(point):
    id = listPoints.index(point)
    color = listColors[random.randint(0, len(listColors)-1)]
    point.delete()
    listPoints.pop(id)
    listAuras.pop(id)
    #listTrails.pop(id)
    scores.pop(id)
    
    
def addFood():
    P = Point(random.randint(-5,5),random.randint(-5,5))
    P.color = 'white'
    listFoods.append(P)
    scores.append(0)
    
    
def getTopPoint():
    topScore = 0
    topPoint = listPoints[0]
    for point in listPoints:
        if scores[listPoints.index(point)] >= topScore:
            topScore = scores[listPoints.index(point)]
            topPoint = point
            
    return [topPoint, topScore]
    
    
def updateAura():
    topPoint = getTopPoint()
        
    #print('Top Score:'+str(topPoint[1]))
        
    for aura in listAuras:
        if listAuras.index(aura) == listPoints.index(topPoint[0]):
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

    topPoint = getTopPoint()[0]
    topScore = getTopPoint()[1]
    
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
    

    if topPoint == point and len(listPoints) > 1:
        goal = 'kill'
       
    
    if goal == 'none':
        while True:
            w = random.randint(1, 2)
            x = point.x
            y = point.y
            
            if random.randint(1,4) != 1:
                if w == 1:   x += 1
                elif w == 2: x -= 1
                elif w == 3: y += 1
                elif w == 4: y -= 1
                
                cPointsTouching = 0
                for otherPoint in listPoints:
                    if otherPoint.x == x and otherPoint.y == y:
                        cPointsTouching += 1
                        
                if cPointsTouching == 0:
                    break
                    
            
            
    elif goal == 'center':
        values = catchGoal(point, centerPoint)
        x = values[0]
        y = values[1]
        
    elif goal == 'food':
        values = catchGoal(point, possibleFood)
        x = values[0]
        y = values[1]
        
    elif goal == 'kill':
        closestPoint = listPoints[0]
        for otherPoint in listPoints:
            if Distance(point, otherPoint) <= Distance(point, closestPoint) and otherPoint != point:
                closestPoint = otherPoint
                
        print('Closest Point: '+str(closestPoint))
        print('Top Point: '+str(topPoint))
        
        values = catchGoal(point, closestPoint)
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
            
    if topPoint == point:
        for otherPoint in listPoints:
            if otherPoint.x == x and otherPoint.y == y and otherPoint != point:
                killPoint(otherPoint)
                print('Hasta la vista, punto...')
        
    prevPoint = Point(point.x, point.y)
    
    point.x = x
    point.y = y
    
    trail = Segment(prevPoint, point, color = point.color)
    
    listTrails.append(trail)
    prevPoint.is_visible = False
    
    scores[indexPoint] = score
    

# VARIABLES

listColors = ['red','green','blue','orange','purple', 'black', 'pink', 'gray', 'brown']
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
cRounds = 100









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
    
    if nRefresh == cRounds:
        break
    
    nRefresh += 1
    print('Round '+str(nRefresh))
    print('')
    
    time.sleep(timeRefresh)
    
    
print('Felilcidades! Te humillaste solito!')

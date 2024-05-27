import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
fig, ax = plt.subplots()


class neuron():
    position : list[int] = [0,0]
    state : int = 0
    linkedRectangle : Patch = Patch()
    drawMargin : float = 0.05
    def __init__(self, position):
        self.position = position
        self.redraw_rectangle()
    
    def redraw_rectangle(self):
        self.linkedRectangle = ax.add_patch(Rectangle((self.position[0] + self.drawMargin, self.position[1] + self.drawMargin),1- self.drawMargin, 1- self.drawMargin))

    def updateGraphics(self):
        newColor : str = 'cyan'
        if self.state == -1:
            newColor = 'black'
        else:
            newColor = 'grey'
        self.linkedRectangle.set_color(newColor)
        
    def changeState(self, newState: int):
        self.state = newState
        self.updateGraphics()

def sign(i: int) ->int :
    if i>= 0:
        return 1
    else:
        return -1
   
paternSize : list[int] = [4,4]
#N
paternLenght : int = paternSize[0]*paternSize[1] 
storedPaterns : list[list[int]] = [[1,1,1,1,1,1,-1,1,1,-1,1,-1,1,-1,1,1]] 

wMatrix : list[list[float]] = []
neurons : list[neuron] = []

def gen_neurons() -> None:
    global paternLenght
    global neurons
    for i in range(0, paternSize[0]):
        for j in range(0, paternSize[1]):
            neurons.append(neuron([i,j])) 
    return

#hebian rule
def feed_network() -> None:
    global wMatrix
    global storedPaterns
    row: list[float] = []
    xij : float = 0

    for i in range(0, paternLenght):
        for j in range(0, paternLenght):
            for patern in storedPaterns:
                xij += 1/(paternLenght) * patern[i] * patern[j]
            row.append(xij)
            xij = 0
        wMatrix.append(row)
        row = []
    return

def inputSchema(schema: list[int]):
    for i in range(0,len(schema)):
        neurons[i].changeState(schema[i])

def update_network():
    global neurons
    global wMatrix
    i : float = 0
    j : float = 0
    term : float = 0
    for m in neurons:
        for neighboors in neurons:
            term += wMatrix[i][j] * neighboors.state
            j += 1
        m.changeState(sign(term))
        term = 0
        j = 0
        i += 1
    return

def read_patern() -> int:
    global neurons
    global storedPaterns
    currentPaternId : float = 0
    for model in storedPaterns:
        for i in range(0, paternLenght):
            if neurons[i].state != model[i]:
                #if one bit is different we break the check of the patern
                currentPaternId += 1
                print('wrong bit at patern', currentPaternId)
                break; 
        #only correct patern can execute this
        print('correct patern at id', currentPaternId)
  
        return currentPaternId
    #will be execute only if no patern was recognised
    print('no correct paterns found')
    return -1
    
correct_patern : int = -1

def on_pressed(event):
    global correct_patern
    print(correct_patern)
    if event.key == 'enter':
        plt.draw()
        if correct_patern == -1:
            update_network()
            correct_patern = read_patern()
            print('updated')
        print('Finished')

fig.canvas.mpl_connect('key_press_event', on_pressed)
gen_neurons()
#inputSchema([1,-1,-1,-1,1,-1,-1,-1,1,-1,1,1,1,1,-1,-1])
#inputSchema([1,-1,1,1,1,1,1,1,1,1,-1,1,1,1,-1,1])
inputSchema([-1,-1,-1,-1,-1,1,-1,1,1,-1,1,1,1,1,1,1])

ax.plot([0,paternSize[0]-1],[0,paternSize[1]-1])
ax. set_aspect('equal', adjustable= 'box')
feed_network()


#plt.show()
plt.show()




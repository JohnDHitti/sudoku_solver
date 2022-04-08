
# Import tkinter for GUI support and copy for avoiding shallow copies
from tkinter import *
from copy import deepcopy
# Initialize the window from tkinter
window = Tk()
window.geometry('252x278')
window.title("Soduko Solver")


#Initialize the main array where values are stored and displayed to the gui. The datatype is native to tkinter
mainArray = []
for i in range(1,10):
    mainArray += [[0,0,0,0,0,0,0,0,0]]
for i in range(0,9):
    for j in range(0,9):
        mainArray[i][j] = StringVar(window)
# Initialize the array where all solutions are stored.
bigArray = []
# Initialize an array of int for transfering each solution
transferArray=[]
for i in range(1,10):
    transferArray += [[0,0,0,0,0,0,0,0,0]]

##----------------------------------------------------------------------------
# These functions are responsable altering the arrays

# Because lists are mutable we must append a deepcopy of each solution to our main array of solutions
def addToBigArray():
    bigArray.append(deepcopy(transferArray))
    

# Set all unfilled entries to zero in the main array
def setZero():
    for i in range(9):
        for j in range(9):
            if mainArray[i][j].get() not in ['1','2','3','4','5','6','7','8','9']:
                mainArray[i][j].set('0')

##----------------------------------------------------------------------------
# These functions are responsable for solving the puzzle

# main function for checking solution
def mainSolutionAlg(i,j):
    # if we are at the end of the board
    if i==8 and j==8:
        # if the element at the end of the board is not zero we can finish
        if mainArray[i][j].get()!='0':
            #store the current solution into the temporary solution and call the function to add it to the big array
            for i in range(9):
                for j in range(9):
                    transferArray[i][j]=int(mainArray[i][j].get())
            addToBigArray()
        # if the element is zero we must check to see what fits
        else:
            for x in range(1,10):
                #check if x can fit in this element
                if isValid(i,j,x) is True:
                    # if it can store the board
                    mainArray[i][j].set(str(x))
                    for i in range(9):
                        for j in range(9):
                            transferArray[i][j]=int(mainArray[i][j].get())
                    addToBigArray()
                    # set element to zero to continue backtracking and look for more solutions
                    mainArray[i][j].set('0')
        return
    # if the alg is at the end of a row go down a row 
    if j>8:
        mainSolutionAlg(i+1,0)  
        return
    # if an entry is zero
    if (mainArray[i][j].get()=='0'):
        for x in range(1,10):
            #check to see if a value will fit there
            if isValid(i,j,x) is True:
                # if it does set it and continue
                mainArray[i][j].set(str(x))
                mainSolutionAlg(i,j+1) 
                # set to zero to continue backtracking and loot for more solutions
                # this will allow the recursive function to come back to this element and try something else
                mainArray[i][j].set('0')
    else:
    #move on to the right if an element is already populated
        mainSolutionAlg(i,j+1)
    return

# this function is passed a element and a vale and is responsable for checking the board if the value can legally fit in that element
def isValid(i,j,x):
    #Check each coll if valid
    for c in range(9):
        if mainArray[i][c].get()==str(x):
            return False
    
    #Check each row if valid
    for r in range(9):
        if mainArray[r][j].get()==str(x):
            return False
    
    #Check each block if valid
    r=i-i%3
    c=j-j%3
    p=r
    while p<=r+2:
        l=c
        while l<=c+2:
            if mainArray[p][l].get()==str(x):
                return False
            l+=1
        p+=1
    return True
  
##----------------------------------------------------------------------------

# this class is incharge of constructing the GUI using Tkinter
class guiClass():
    
    def __init__(self, window):
        # Generate the Entrybox grid
        entryGrid= []
        for i in range(1,10):
            entryGrid += [[0,0,0,0,0,0,0,0,0]]

        for i in range(0,9):
            for j in range(0,9):
                # set the background color of every other box
                if i in [3,4,5] and j in [3,4,5]:
                    bg = 'light gray'
                elif (i < 3 or i > 5) and (j < 3 or j > 5):
                    bg = 'light gray'
                else:
                    bg = 'white'
                # generate all the enty boxes
                entryGrid[i][j] = Entry(window, width = 2, font = ('Helvetica', 16), bg = bg, cursor = 'arrow', borderwidth = 1,
                                          highlightcolor = 'yellow', highlightthickness = 0, highlightbackground = 'gray',
                                          textvar = mainArray[i][j])
                # if a box its clicked out of the erase function will be called
                entryGrid[i][j].bind('<FocusOut>', self.eraseInvalidInputs)
                # places all the entry boxes into a grid
                entryGrid[i][j].grid(row=i, column=j)

        # Buttons 
        self.btn1 = Button(window, text="Solve", command=self.solve)
        self.btn2 = Button(window, text="Clear", command=self.clear)
        self.btn3 = Button(window, text="Sample 1", command=self.sample1)
        self.btn4 = Button(window, text="Sample 2", command=self.sample2)
        self.btn1.place(x=0,y=252)
        self.btn2.place(x=214,y=252)
        self.btn4.place(x=132,y=252)
        self.btn3.place(x=62,y=252)

    # Erases all invalid inputs (anything that isnt 1-9)
    def eraseInvalidInputs(self, event):
        for i in range(9):
            for j in range(9):
                if mainArray[i][j].get() == '':
                    continue
                if len(mainArray[i][j].get()) > 1 or mainArray[i][j].get() not in ['1','2','3','4','5','6','7','8','9']:
                    mainArray[i][j].set('')

    # The sample functions populate the grid with preset puzzles (puzzles are taken from https://sekika.github.io/kaidoku/)
    def sample1(self):
        demo =[[3, '', 6, '', '', 8, 4, '', ''], 
          [5, 2, '', '', '', '', '', '', ''], 
          ['', '', 7, '', '', '', '', 3, 1], 
          ['', '', 3, '', 1, '', '', 8, ''], 
          [9, '', '', 8, 6, 3, '', '', 5], 
          ['', 5, '', '', 9, '', '', '',''], 
          [1, 3, '', '', '', '', 2, 5, ''], 
          ['', '', '', '', '', '', '', 7, 4], 
          ['', '', 5, 2, '', 6, '', '', '']]
        for i in range(0,9):
            for j in range(0,9):
                mainArray[i][j].set(str(demo[i][j]))
                
    def sample2(self):
        demo =[['', '', '', 7, 9, '', '', 3, 4], 
          [5, '', 9, 2, '', '', '', 1, 8], 
          ['', 3, '', 6, '', '', '', '', ''], 
          [2, 4, '', 1, '', '', '', '', ''], 
          ['', '', 8, '', 4, '', 9, '', ''], 
          ['', '', '', '', '', 6, '', 4,7], 
          ['', '', '', '', '', 8, '', 2, ''], 
          [1, 8, '', '', '', 2, 4, '', 3], 
          [4, 7, '', '', 1, 3, '', '', '']]
        for i in range(0,9):
            for j in range(0,9):
                mainArray[i][j].set(str(demo[i][j]))

    # calls functions that solve the puzzle and takes the gui to the solution screen
    def solve(self):
        #set everything without an entry to zero
        setZero()
        #call the main solution algorythm
        mainSolutionAlg(0,0)
        #populate the grid with the solution
        try:
            for i in range(9):
                for j in range(9):
                    mainArray[i][j].set(str(bigArray[0][i][j]))
        except:
            print("No Solution")
        # change the gui to the solution view
        self.btn1.destroy()
        self.btn3.destroy()
        self.btn2.destroy()
        self.btn4.destroy()
        self.currentSoln=0
        self.btnNext = Button(window, text="Next", command=self.nextSoln)
        self.btnPrev = Button(window, text="Prev", command=self.prevSoln)
        self.clrBoard = Button(window, text="Clear", command=self.clearBoard)
        self.currentSolnDisplay = Label(master=window, text=self.currentSoln+1)
        self.btnPrev.place(x=0,y=252)
        self.btnNext.place(x=102,y=252)
        self.clrBoard.place(x=214,y=252)
        self.currentSolnDisplay.place(x=62,y=255)
        
    # clears the grid
    def clear(self):
        for i in range(9):
            for j in range(9):
                mainArray[i][j].set(' ')
    # displays the next solution
    def nextSoln(self):
        if(self.currentSoln!=(len(bigArray)-1)):
            self.currentSoln+=1
        for i in range(9):
            for j in range(9):
                mainArray[i][j].set(str(bigArray[self.currentSoln][i][j]))
        self.currentSolnDisplay["text"] = self.currentSoln+1
    #displays the previous solution
    def prevSoln(self):
        if self.currentSoln!=0:
            self.currentSoln-=1
        for i in range(9):
            for j in range(9):
                mainArray[i][j].set(str(bigArray[self.currentSoln][i][j]))
        self.currentSolnDisplay["text"] = self.currentSoln+1
    #resets the board to its original state
    def clearBoard(self):
        self.btnNext.destroy()
        self.btnPrev.destroy()
        self.clrBoard.destroy()
        self.currentSolnDisplay.destroy()
        self.clear()
        for x in range(len(bigArray)):
            bigArray.pop()
        self.__init__(window)

##----------------------------------------------------------------------------      
        
## DRIVER
guiClass(window)
window.mainloop()

# code takes approximatly 2-5min for 5000 solutions
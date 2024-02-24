# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:53:58 2023

@author: jones
"""

import PySimpleGUI as gui
import copy

class TreeNode:
    visitedTowns = []
    def __init__(self, name):
        self.name = name
        self.parentNodes = []
        self.childNodes = []
        self.travelCosts = []
        
    def findNode(self, name):
        result = None
        
        if name == self.name:
            return self
        
        for n in self.childNodes:
            if n.name == name:
                result = n
            elif result == None:
                result = n.findNode(name)
        return result
    
    def findNodesAtDepth(self, depth, counter = 0):
        results = []
        
        for n in self.childNodes:
            if counter + 1 == depth:
                if n.name not in TreeNode.visitedTowns:
                    TreeNode.visitedTowns.append(n.name)
                    results.append(n)
            else:
                results.extend(n.findNodesAtDepth(depth, counter + 1))
                
        return results
    
    def __eq__(self, other):
        return not other == None and self.name == other.name
    
    def __hash__(self):
        return hash(("name", self.name, "parentNodes", self.parentNodes, "childNodes", self.childNodes))


class Pair:
    def __init__(self, start, end, cost):
        self.start = start
        self.end = end
        self.cost = cost
        
def init():
    global townSize, labelSize, labelWidth, townList, defaultPairList, pairList, window, graph
    townSize = 15
    
    townList = ["Oradea", "Zerind", "Arad", "Sibiu", "Fagaras", "Timisoara", "Rimnicu Vilcea",
                "Lugoj", "Pitesti", "Mehadia", "Drobeta", "Craiova", "Bucharest", "Giurgiu",
                "Urziceni", "Hirsova", "Eforie", "Vaslui", "Iasi", "Neamt"]
    
    defaultPairList = [Pair("Oradea", "Zerind", 71), Pair("Oradea", "Sibiu", 151), 
            Pair("Zerind", "Arad", 75), Pair("Arad", "Sibiu", 140), Pair("Arad", "Timisoara", 118), 
            Pair("Sibiu", "Rimnicu Vilcea", 80), Pair("Sibiu", "Fagaras", 99), Pair("Timisoara", "Lugoj", 111), 
            Pair("Lugoj", "Mehadia", 70), Pair("Mehadia", "Drobeta", 75), Pair("Drobeta", "Craiova", 120), 
            Pair("Rimnicu Vilcea", "Craiova", 146), Pair("Rimnicu Vilcea", "Pitesti", 97), 
            Pair("Craiova", "Pitesti", 138), Pair("Fagaras", "Bucharest", 211), 
            Pair("Pitesti", "Bucharest", 101), Pair("Bucharest", "Giurgiu", 90), 
            Pair("Bucharest", "Urziceni", 85), Pair("Urziceni", "Hirsova", 98), Pair("Hirsova", "Eforie", 86), 
            Pair("Urziceni", "Vaslui", 142), Pair("Vaslui", "Iasi", 92), Pair("Iasi", "Neamt", 87)]
    
    pairList = copy.deepcopy(defaultPairList)
    
    graphRightClickMenu = [[], ["Edit Distance", "Clear Distance"]]
    
    labelWidth = len(max(townList, key=len)) + 10
    
    layout = [
        [gui.Text("Town Relationships")],
        [gui.Graph((500, 500), (-2 * labelWidth, 350), (350, -2 * labelWidth), key='-GRAPH-',
                  right_click_menu=graphRightClickMenu, change_submits=True, drag_submits=False)],
        [[gui.Text("Choose A Search Algorithm: "), 
          gui.Combo(("Breadth-First Search (BFS)", #"Uniform-Cost Search (UCS)",
                     "Depth-First Search (DFS)", "Iterative-Deepening Search (IDS)"),
                    "Breadth-First Search (BFS)",
                    key = "Method", readonly = True)],
         [gui.Text("Choose The Starting Town: "),
           gui.Combo(list(filter(lambda p: not p == "Bucharest", townList)),
                     "Oradea", key = "Start", readonly= True, enable_events = True)],
         [gui.Text("Choose The Destination Town: "),
           gui.Combo(list(filter(lambda p: not p == "Oradea", townList)),
                     "Bucharest", key = "End", readonly= True, enable_events = True)],
        [gui.Button("Search for Optimal Path", key = "Search"), gui.Button("Reset", key = "Reset")]]
    ]
    
    window = gui.Window('Romania Problem', layout, finalize=True)
    graph = window['-GRAPH-']

    drawTable()
    
def drawTable():
    global townSize, labelSize, labelWidth, townList, pairList, pairTable, graph
    
    pairTable = []
    
    graph.erase()
    for row in range(len(townList)):
        pairs = []
        graph.draw_text(townList[row], (0, row * townSize + 8), 
                        text_location=gui.TEXT_LOCATION_RIGHT)
        for col in range(len(townList)):
            if row == col:
                graph.draw_rectangle((col * townSize + 5, row * townSize + 3), 
                     (col * townSize + townSize + 5, row * townSize + townSize + 3), 
                     line_color='black')
                graph.draw_text('{}'.format("X"),  
                    (col * townSize + townSize - 2.5, row * townSize + townSize - 4),
                    font = "Default 19")
                pairs.append([False, 0])
            else:
                newPair = [False, 0]
                
                for p in pairList:
                    if townList[row] == p.start and townList[col] == p.end or townList[row] == p.end and townList[col] == p.start:
                        newPair = [True, p.cost]
                        break
                if newPair[0]:
                    graph.draw_rectangle((col * townSize + 5, row * townSize + 3), 
                         (col * townSize + townSize + 5, row * townSize + townSize + 3), 
                         line_color='black', fill_color='green')
                    graph.draw_text('{}'.format(str(newPair[1])),  
                        (col * townSize + townSize - 2.5, row * townSize + townSize - 4),
                        font = "Default 8")
                else:
                    graph.draw_rectangle((col * townSize + 5, row * townSize + 3), 
                         (col * townSize + townSize + 5, row * townSize + townSize + 3), 
                         line_color='black')
                    
                pairs.append(newPair)
        pairTable.append(pairs)
            
    for col in range(len(townList)):
        graph.draw_text(townList[col], (col * townSize + townSize, 0), angle = 270,
                        text_location=gui.TEXT_LOCATION_RIGHT)

def addChildrenFromPairList(baseNode, pList, townName):
    baseNode.childNodes = [TreeNode(p.end) for p in pList if p.start == townName]
    pList = list(filter(lambda p: not p.start == townName, pList))
        
    baseNode.childNodes.extend([TreeNode(p.start) for p in pList if p.end == townName])
    pList = list(filter(lambda p: not p.end == townName, pList))
        
    for c in baseNode.childNodes:
        c.parentNodes = [baseNode]
    
    return pList

def findDeepestNodePath(currentNode, pList, destinationTown, depthLimit = 0, counter = 0):
    destinationNode = None
    childNodes = copy.deepcopy(currentNode.childNodes)
    
    if depthLimit == 0 or counter + 1 <= depthLimit:
        for n in childNodes:
            if n.name == destinationTown:
                destinationNode = n
            else:
                if n.name not in TreeNode.visitedTowns:
                    TreeNode.visitedTowns.append(n.name)
                pList = addChildrenFromPairList(n, pList, n.name)
        
        if destinationNode == None:
            for n in childNodes:
                destinationNode = findDeepestNodePath(n, pList, destinationTown, depthLimit, counter + 1)
                if destinationNode == None:
                    currentNode.childNodes.remove(n)
                else:
                    break
    else:
        childNodes = []
        
    currentNode.childNodes = childNodes
    
    if not destinationNode == None and destinationNode.name not in TreeNode.visitedTowns:
        TreeNode.visitedTowns.append(destinationNode.name)
    return destinationNode
                
def BreadthFirstSearch(startingTown, destinationTown):
    global pairList
    
    baseNode = TreeNode(startingTown)
    TreeNode.visitedTowns = [startingTown]
    
    pList = addChildrenFromPairList(baseNode,  pairList.copy(), startingTown)
    
    depth = 1
    nodesAtDepth = baseNode.findNodesAtDepth(depth)
    
    while len(pList) > 0 or len(nodesAtDepth) > 0:
        for n in nodesAtDepth:
            pList = addChildrenFromPairList(n, pList, n.name)
                
        depth += 1
        nodesAtDepth = baseNode.findNodesAtDepth(depth)
    
    printSearchResults(baseNode, destinationTown)

def DepthFirstSearch(startingTown, destinationTown):
    global pairList
    
    baseNode = TreeNode(startingTown)
    TreeNode.visitedTowns = [baseNode.name]
    pList = addChildrenFromPairList(baseNode, pairList.copy(), startingTown)
    
    findDeepestNodePath(baseNode, pList, destinationTown)
    
    printSearchResults(baseNode, destinationTown)

def IterativeDeepeningSearch(startingTown, destinationTown):
    global pairList
    
    depthLimit = gui.popup_get_text("What is the limit for the depth of the search (Default 1)?", keep_on_top=True)
    
    if depthLimit == "":
        depthLimit = 1
    else:
        depthLimit = int(depthLimit)
        
    baseNode = TreeNode(startingTown)
    TreeNode.visitedTowns = [baseNode.name]
    deepestNode = None
    depth = 1
    
    while deepestNode == None and depth <= depthLimit:
        pList = addChildrenFromPairList(baseNode, pairList.copy(), startingTown)
        deepestNode = findDeepestNodePath(baseNode, pList, destinationTown, depth)
        depth += 1
    
    printSearchResults(baseNode, destinationTown)
    
def printSearchResults(baseNode, destinationTown, cost = 0):
    n = baseNode.findNode(destinationTown)
        
    outputString = ""
    
    outputString = "The following towns were visited: " + ", ".join(str(t) for t in TreeNode.visitedTowns)
    outputString += "\n\n"
        
    if not n == None:
        result = [n.name]
        
        while len(n.parentNodes) > 0:
            n = n.parentNodes[0]
            result.append(n.name)
        
        result.reverse()
        
        if cost == 0:
            cost = len(result)
        
        outputString += "The found optimal path is: " + ", ".join(str(r) for r in result)
        outputString += "\n\nThe total cost of the trip is: " + str(cost)
    else:
        outputString += destinationTown + " could not be found with the given depth limit."
    
    gui.popup(outputString)
    
def mainLoop():
    global townSize, labelSize, labelWidth, townList, defaultPairList, pairList, pairTable, window, graph
    while True:
        event, values = window.read()
        print(event, values)
        if event in (gui.WIN_CLOSED, 'Exit'):
            break
        mouse = values['-GRAPH-']
    
        if event == '-GRAPH-':
            if mouse == (None, None):
                continue
            box_x = mouse[0]//townSize
            box_y = mouse[1]//townSize
            
            inXRange = 0 <= box_x < len(townList)
            inYRange = 0 <= box_y < len(townList)
            
            if not box_x == box_y and inXRange and inYRange:
                boxPosition1 = (box_x * townSize + 5, box_y * townSize + 3)
                boxPosition2 = (box_x * townSize + townSize + 5, box_y * townSize + townSize + 3)
                
                pairTable[box_x][box_y][0] = not pairTable[box_x][box_y][0]
                
                if pairTable[box_x][box_y][0]:
                    pairList.append(Pair(townList[box_x], townList[box_y], 0))
                else:
                    pairList = list(filter(lambda p: not (p.start == townList[box_x] and p.end == townList[box_y]), pairList))
                graph.draw_rectangle(boxPosition1, boxPosition2, line_color='black',
                     fill_color='green' if pairTable[box_x][box_y][0] else window.BackgroundColor)
                
                graph.draw_rectangle((boxPosition1[1] + 2, boxPosition1[0] - 2), 
                                     (boxPosition2[1] + 2, boxPosition2[0] - 2),
                                     line_color='black',
                     fill_color='green' if pairTable[box_x][box_y][0] else window.BackgroundColor)
        elif event == "Edit Distance":
            box_x = mouse[0]//townSize
            box_y = mouse[1]//townSize
            
            inXRange = 0 <= box_x < len(townList)
            inYRange = 0 <= box_y < len(townList)
            
            if inXRange and inYRange:
                isEnabled = pairTable[box_x][box_y][0]
            
            if not box_x == box_y and inXRange and inYRange and isEnabled:
                boxPosition1 = (box_x * townSize + 5, box_y * townSize + 3)
                boxPosition2 = (box_x * townSize + townSize + 5, box_y * townSize + townSize + 3)
                cost = gui.popup_get_text("What is the cost between these two towns?", keep_on_top=True)
                
                if not cost == "":
                    foundPair = None
                    
                    for p in pairList:
                        if p.start == townList[box_x] and p.end == townList[box_y]:
                            foundPair = p
                    
                    if not foundPair == None:
                        foundPair.cost = cost
                
                graph.draw_rectangle(boxPosition1, boxPosition2, line_color='black',
                     fill_color='green')
                graph.draw_text('{}'.format(str(cost) if not cost == None else ""),  
                    (box_x * townSize + townSize - 2.5, box_y * townSize + townSize - 4),
                    font = "Default 8")
                
                graph.draw_rectangle((boxPosition1[1] + 2, boxPosition1[0] - 2), 
                                     (boxPosition2[1] + 2, boxPosition2[0] - 2),
                                     line_color='black',
                     fill_color='green')
                graph.draw_text('{}'.format(str(cost) if not cost == None else ""),  
                    (box_y * townSize + townSize - 2.5, box_x * townSize + townSize - 4),
                    font = "Default 8")
        elif event == "Clear Distance":
            box_x = mouse[0]//townSize
            box_y = mouse[1]//townSize
            
            inXRange = 0 <= box_x < len(townList)
            inYRange = 0 <= box_y < len(townList)
            
            if not box_x == box_y and inXRange and inYRange:
                boxPosition1 = (box_x * townSize + 5, box_y * townSize + 3)
                boxPosition2 = (box_x * townSize + townSize + 5, box_y * townSize + townSize + 3)
                
                for p in pairList:
                    if p.start == townList[box_x] and p.end == townList[box_y]:
                        p.cost = 0
                
                graph.draw_rectangle(boxPosition1, boxPosition2, line_color='black',
                     fill_color='green' if pairTable[box_x][box_y][0] else window.BackgroundColor)
                
                graph.draw_rectangle((boxPosition1[1] + 2, boxPosition1[0] - 2), 
                                     (boxPosition2[1] + 2, boxPosition2[0] - 2),
                                     line_color='black',
                     fill_color='green' if pairTable[box_x][box_y][0] else window.BackgroundColor)
        elif event == "Start":
            window["End"].update(values=list(filter(lambda p: not p == values["Start"],
                                townList)), value=values["End"])
        elif event == "End":
            window["Start"].update(values=list(filter(lambda p: not p == values["End"],
                                  townList)), value=values["Start"])
        elif event == "Search":
            if "BFS" in values["Method"]:
                BreadthFirstSearch(values["Start"], values["End"])
            #elif "UCS" in values["Method"]:
            #    UniformCostSearch(values["Start"], values["End"])
            elif "DFS" in values["Method"]:
                DepthFirstSearch(values["Start"], values["End"])
            elif "IDS" in values["Method"]:
                IterativeDeepeningSearch(values["Start"], values["End"])
        elif event == "Reset":
            pairList = copy.deepcopy(defaultPairList)
            drawTable()
init()        
mainLoop()
window.close()
    
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

class plot_chart:
    ''' Plot_chart is a module which plots three different graphs:
        -simple plot or normal
        -scatter plot
        -bar plot
        input variables:-
        column_Ax                  : name of the column in your excel sheet which will treated as x-axis values
        column_By                  : name of the column in your excel sheet which will treated as y-axis values
        GoogleSpreadSheet_ID       : this is the id or part of g-sheet link in google sheet
        GraphType                  : take type of graph like 'normal', 'bar', 'scatter'
        color                      : take name of the color eg. 'blue', 'red', black'
        title                      : title for graph or name of the graph => default 'No Title'
        x_axis = 'X', y_axis = 'Y' : xlabel, ylabel names for x and y line
        linestyle                  : line style e.g. 'solid', 'dashed' etc
    '''
    def __init__(self, column_Ax, column_By, GoogleSpreadSheet_ID, GraphType = 'normal', color = 'blue',title = 'No Title', x_axis = 'X', y_axis = 'Y', linestyle='solid'):
        self.x, self.y = column_Ax, column_By
        self.G_id = GoogleSpreadSheet_ID
        self.Gtype = GraphType
        self.color = color
        self.x_name, self.y_name = x_axis, y_axis
        self.line = linestyle
        plt.title(title)
        plt.xlabel(self.x_name)
        plt.ylabel(self.y_name)
    
    def plot_c(self):
        ''' plot_c function takes no argument
        it's a main function '''
        df= pd.read_csv(f"https://docs.google.com/spreadsheets/d/{self.G_id}/export?format=csv")
        self.l=[]
        self.l.append(self.x)
        self.l.append(self.y)
        #print(type(l))
        self.x1=df[self.l[0]]
        self.x1=list(self.x1)
        #print("X1= ",self.x1)
        self.y1=df[self.l[1]]
        self.y1=list(self.y1)
        #print("Y1= ",self.y1)
        axisx=[]
        axisy=[]
        
        for i in self.x1:
            axisx.append(i)
        for j in self.y1:
            axisy.append(j)
        #print(x,y)
        #print("X Type = ",type(x))
        if self.Gtype == 'normal':
            plt.plot(axisx, axisy, color = self.color, linestyle = self.line)
            plt.show()
        elif self.Gtype == 'bar':
            plt.bar(self.x1, self.y1, color=self.color)
            plt.show()
        elif self.Gtype == 'scatter':
            plt.scatter(self.x1, self.y1)
            plt.show()

if __name__=='__main__':
    z='1jbcRvatx1DmtxWWwC7dcEwSyYOAxD0iFICGN33JoUSk'
    x = 'Name'
    y = 'B'
    p = plot_chart(x ,y, z, 'scatter', color='purple')
    p.plot_c()
    p = plot_chart(x, y, z, 'bar', 'orange', 'The G plot', 'Column A', 'Column B', 'dashed')
    p.plot_c()
    

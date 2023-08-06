This is a simple graph plot which take csv file from googal sheet and plot.
function names : plot_c(self)

functions arguments (column_Ax, column_By, GoogleSpreadSheet_ID, GraphType = 'normal', color = 'blue',title = 'No Title', x_axis = 'X', y_axis = 'Y', linestyle='solid'):

Plot_chart is a module which plots three different graphs:
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

main.py --> main file that runs the Genetic class on a loop and codes to display the tkinter interface
ga.py --> Module with Genetic class containing the properties and methods of a genetic algorithm
d_n_m.csv --> n = {4, 8, 12}, m = {8, 12, 16} containing demand info for certain time periods and inputed as a dictionary in Genetic class
df_n_m.csv --> n = {4, 8, 12}, m = {8, 12, 16} containing normalised travel time info for certain time periods and inputed as a np matrix in Genetic class
demand_norm_loc.csv, Location_scaled.csv --> Contains all the coordinates scaled to fit on the tkinter interface
8_12.csv --> non normalised travel time csv matrix
Pot.csv --> Contains preprocessed potential point's info and inputed as a dictionary in Genetic class
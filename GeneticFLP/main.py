# KAVIN R V
# Ran on Arm based Architecture on M1 chip
import pandas as pd
import tkinter as tk
from ga import Genetic
import tkinter.font as font


time_periods = ['8_12', '12_16']

df = pd.read_csv(f'd_{time_periods[0]}.csv', index_col=0)
demand = df.to_dict('records')

df = pd.read_csv('Pot.csv', index_col=0)
potential = df.to_dict('records')

# Compactness of each potential locations
density = df['density'].to_numpy()
print(density.shape)
# density = np.random.random(432)

pop_size = 1000
mut_rate = 5
travel_time = pd.read_csv(f'df_4_8.csv', header=None, index_col=1)
travel_time = travel_time.to_numpy()
print(travel_time.shape)

# The Algorithm Class
genetic = Genetic(demand=demand, potential=potential, pop_size=pop_size, mut_rate=mut_rate,
                  travel_time=travel_time, densities=density)
genetic.gen_population()

# Reads the potential location coordinates
locations_pot = pd.read_csv('Location_scaled.csv')
locations_pot = locations_pot['loc'].tolist()
locations_pot = [tuple(float(i) for i in x.replace('(', '').replace(')', '').replace('...', '').split(', ')) for x in locations_pot]

# locations_dem = pd.read_csv('demand_norm_loc.csv')
# locations_dem = locations_dem['X,Y'].tolist()
# locations_dem = [tuple(float(i) for i in x.replace('(', '').replace(')', '').replace('...', '').split(', ')) for x in locations_dem]


# ---------------------------- CONSTANTS ------------------------------- #
L_PINK = "#2E4C6D"
PINK = "#2E4C6D"
DICE = "#94DAFF"
LINE = "#94DAFF"
FONT_NAME = "Helvetica"
# Whites
FIXED = '#C64756'
# Red
LOCATION = "#94DAFF"
# Yellow
HUBS = '#FAD586'
END = 0


# ---------------------------- FUNCTIONS ------------------------------- #


def draw():
    """
    Main Function that runs the algorithm on a loop
    :return:
    """
    word_record = 0
    record_holder = []
    global END, L_PINK
    END = 0
    for _ in range(1000):
        genetic.eval_fitness()
        genetic.nat_sel()
        genetic.new_pop()
        avg_fit = sum(genetic.fitness)/len(genetic.fitness)
        b_value, b_gene, incomp_gene, b_len = genetic.get_best
        if b_value > word_record:
            word_record = b_value
            record_holder = incomp_gene
        display = f'\n   loop: {_+1}\n   Average Fit: {avg_fit}' + '\n' + f'   Best Fitness: {b_value}' + '\n' + f'   Population Size: {len(genetic.population)} '
        display = display + f'\n   Current Best: {word_record}'
        T.delete(1.0, tk.END)
        T.insert(tk.END, display)
        canvas.delete('hubs')

        # Best hubs Location Plot
        for j in incomp_gene:
            kx = locations_pot[j][0]
            ky = 925 - locations_pot[j][1]
            canvas.create_oval(kx - 4, ky - 4, kx + 4, ky + 4, fill=HUBS,
                               tags='hubs', outline=HUBS)
        canvas.update()
        if END == 1:
            break
    # Best hubs Location Plot after loop
    for j in record_holder:
        kx = locations_pot[j][0]
        ky = 925 - locations_pot[j][1]
        canvas.create_oval(kx - 4, ky - 4, kx + 4, ky + 4, fill=HUBS,
                           tags='hubs', outline=HUBS)
    canvas.update()


def end_it():
    global END, L_PINK
    END = 1


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.geometry('1600x2000')
window.title("Genetic Algorithm")
window.config(padx=50, pady=50, bg=PINK)

FONT = font.Font(size=40)
FONT2 = font.Font(size=30)

canvas = tk.Canvas(width=1500, height=1200, bg=L_PINK, highlightthickness=0)
canvas.place(x=50, y=50)
canvas.pack()

start_button = tk.Button(text="Start", highlightbackground=DICE, fg=L_PINK, highlightthickness=0,
                         font=FONT_NAME, width=4, height=1)
start_button.config(command=draw)
start_button['font'] = FONT
start_button.place(x=200, y=745)

end_button = tk.Button(text="End", highlightbackground=DICE, fg=L_PINK, highlightthickness=0,
                       font=FONT_NAME, width=4, height=1)
end_button.config(command=end_it)
end_button['font'] = FONT
end_button.place(x=400, y=745)

T = tk.Text(window, height=7, width=30, bg=L_PINK)
T.place(x=150, y=150)
T['font'] = FONT2
T.pack(expand=True)

canvas.create_window(350, 350, window=T)

# Potential Locations Plot
for i in locations_pot:
    px = i[0]
    py = 925 - i[1]
    canvas.create_rectangle(px - 2, py - 2, px + 2, py + 2, fill=LOCATION, outline=LOCATION)

# for i in locations_dem:
#     px = i[0]
#     py = 925 - i[1]
#     canvas.create_rectangle(px - 0.5, py - 0.5, px + 0.5, py + 0.5, fill=LOCATION, outline=LOCATION)

# Fixed Locations Plot
for i in genetic.fixed:
    kx = locations_pot[i][0]
    ky = 925 - locations_pot[i][1]
    canvas.create_oval(kx - 6, ky - 6, kx + 6, ky + 6, fill=FIXED,
                       tags='fixed', outline=FIXED)

window.mainloop()

# draw()

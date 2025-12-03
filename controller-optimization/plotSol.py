#!/usr/bin/env python3
#(c) Izudin Dzafic, 2023
#add chmod +x plotSol.py
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

args = len(sys.argv)-1
if args != 1:
    print('Missing input file name!')
    sys.exit()
    
# set dark background
plt.style.use('dark_background')
# Read the file and extract the relevant lines
lines = []
header = []
iRows = 0
with open(sys.argv[1], 'r') as file:
    foundSolutionData = False
    headerLoaded = False
    firstHeaderLine = False
    secondHeaderLine = False
    for line in file:
        if foundSolutionData and firstHeaderLine and not headerLoaded:
            header = line.strip().split()
            headerLoaded = True
            print('Header is loaded')
        elif foundSolutionData:
            if not firstHeaderLine:
                if line.startswith('------'):
                    firstHeaderLine = True
                    continue
                else:
                    print('File is not formated properly! First line (--------) is not available!')
                    sys.exit()
            if not secondHeaderLine:       
                if line.startswith('------'):
                    secondHeaderLine = True
                    continue
                else:
                    print('File is not formated properly! Second line (--------) is not available!')
                    sys.exit()             
            if line.startswith('----'):
                print('Detected end of SOLUTION_DATA')
                break
            lines.append(line)
            iRows += 1
        elif line.strip() == 'SOLUTION_DATA':
            foundSolutionData = True
            print('Detected SOLUTION_DATA')
if not headerLoaded:
    print('ERROR! Could not detect header')
    sys.exit()
if iRows == 0:
    print('ERROR! Could not load any usable line with data')
    sys.exit()
    
# Parse the data
data = np.loadtxt(lines, dtype=float)
# Check if data is empty
if data.size == 0:
    print("No data found in the file.")
else:
    # Extract the columns
    t = data[:, 0]
    columns = data[:, 1:].T
    
    # Grupiraj varijable u kategorije
    voltage_vars = [i+1 for i, h in enumerate(header[1:]) if h.startswith('V')]
    theta_vars = [i+1 for i, h in enumerate(header[1:]) if h.startswith('theta')]
    from numpy import gradient

    # Računaj frekvenciju svake sabirnice iz derivacije theta
    f_busHz = []  # lista (ime, niz frekvencija)
    for i in theta_vars:
        dtheta_dt = gradient(columns[i-1], t)  # derivacija theta po vremenu
        f_bus = dtheta_dt / (2 * np.pi) * 60   # f = (1/2pi) * dθ/dt * 60
        f_busHz.append((header[i], f_bus))

    delta_vars = [i+1 for i, h in enumerate(header[1:]) if h.startswith('delta')]
    w_vars = [i+1 for i, h in enumerate(header[1:]) if h.startswith('w')]
    elq_vars = [i+1 for i, h in enumerate(header[1:]) if h.startswith('elq')]
    id_vars = [i+1 for i, h in enumerate(header[1:]) if h.startswith('id')]
    iq_vars = [i+1 for i, h in enumerate(header[1:]) if h.startswith('iq')]
    
    # Kreiraj prvu figuru sa 3 grafa
    fig1, axes1 = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
    fig1.suptitle('IEEE 9-bus sistem - Naponi i uglovi', fontsize=16)
    
    # Plotaj napone u prvoj figuri
    for i in voltage_vars:
        axes1[0].plot(t, columns[i-1], label=header[i])
    axes1[0].set_ylabel('Napon [p.u.]')
    axes1[0].set_title('Naponi sabirnica')
    axes1[0].grid(linestyle='dotted', linewidth=1)
    axes1[0].legend(loc='upper right')
    
    # Plotaj theta uglove u prvoj figuri (konvertovano u stepene)
    for i in theta_vars:
        axes1[1].plot(t, np.degrees(columns[i-1]), label=header[i])
    axes1[1].set_ylabel('Uglovi [°]')
    axes1[1].set_title('Fazni uglovi sabirnica')
    axes1[1].grid(linestyle='dotted', linewidth=1)
    axes1[1].legend(loc='upper right')
    
    # Plotaj delta uglove u prvoj figuri (konvertovano u stepene)
    for i in delta_vars:
        axes1[2].plot(t, np.degrees(columns[i-1]), label=header[i])
    axes1[2].set_ylabel('Delta [°]')
    axes1[2].set_title('Uglovi rotora')
    axes1[2].grid(linestyle='dotted', linewidth=1)
    axes1[2].legend(loc='upper right')
    axes1[2].set_xlabel('Vrijeme (t) [s]')
    
    # Poboljšanja za prikaz x-ose
    # Automatski podesi broj tick-ova na x-osi
    axes1[2].xaxis.set_major_locator(plt.MaxNLocator(10))
    
    # Podesi razmak između podgrafova u prvoj figuri - povećaj bottom margin
    fig1.tight_layout(rect=[0, 0.03, 1, 0.96])

    
    # Kreiraj drugu figuru sa preostalim varijablama (maksimalno 4 grafa)
    num_subplots2 = 0
    if w_vars: num_subplots2 += 1
    if elq_vars: num_subplots2 += 1
    if id_vars: num_subplots2 += 1
    if iq_vars: num_subplots2 += 1
    
    if num_subplots2 > 0:
        fig2, axes2 = plt.subplots(num_subplots2, 1, figsize=(12, num_subplots2*3), sharex=True)
        fig2.suptitle('IEEE 9-bus sistem - Varijable generatora', fontsize=16)
        
        # Ako imamo samo jedan subplot u drugoj figuri, stavi ga u listu
        if num_subplots2 == 1:
            axes2 = [axes2]
            
        current_ax = 0
        
        # Plotaj w varijable u drugoj figuri
        if w_vars:
            for i in w_vars:
                axes2[current_ax].plot(t, columns[i-1], label=header[i])
            axes2[current_ax].set_ylabel('Brzina [p.u.]')
            axes2[current_ax].set_title('Brzine rotora generatora')
            axes2[current_ax].grid(linestyle='dotted', linewidth=1)
            axes2[current_ax].legend(loc='upper right')
            current_ax += 1
    
        # Plotaj elq varijable u drugoj figuri
        if elq_vars:
            for i in elq_vars:
                axes2[current_ax].plot(t, columns[i-1], label=header[i])
            axes2[current_ax].set_ylabel('ELQ [p.u.]')
            axes2[current_ax].set_title('ELQ generatora')
            axes2[current_ax].grid(linestyle='dotted', linewidth=1)
            axes2[current_ax].legend(loc='upper right')
            current_ax += 1
        
        # Plotaj id varijable u drugoj figuri
        if id_vars:
            for i in id_vars:
                axes2[current_ax].plot(t, columns[i-1], label=header[i])
            axes2[current_ax].set_ylabel('ID [p.u.]')
            axes2[current_ax].set_title('ID generatora')
            axes2[current_ax].grid(linestyle='dotted', linewidth=1)
            axes2[current_ax].legend(loc='upper right')
            current_ax += 1
        
        # Plotaj iq varijable u drugoj figuri
        if iq_vars:
            for i in iq_vars:
                axes2[current_ax].plot(t, columns[i-1], label=header[i])
            axes2[current_ax].set_ylabel('IQ [p.u.]')
            axes2[current_ax].set_title('IQ generatora')
            axes2[current_ax].grid(linestyle='dotted', linewidth=1)
            axes2[current_ax].legend(loc='upper right')
        
        # Zajednički x-osa label za zadnji graf u drugoj figuri
        if num_subplots2 > 0:
            axes2[-1].set_xlabel('Vrijeme (t) [s]')
            # Poboljšaj prikaz x-ose i za drugu figuru
            axes2[-1].xaxis.set_major_locator(plt.MaxNLocator(10))
        
        # Podesi razmak između podgrafova u drugoj figuri
        fig2.tight_layout(rect=[0, 0.03, 1, 0.96])

    # Plotaj frekvenciju (f = 60 * w)
    f_nominal = 60.0
    freq_vars = [i for i in w_vars]  # koristi iste indekse
    if freq_vars:
        fig_freq, ax_freq = plt.subplots(figsize=(12, 4))
        for i in freq_vars:
            ax_freq.plot(t, f_nominal * columns[i-1], label="f_" + header[i])
        ax_freq.set_title("Frekvencija sistema [Hz]")
        ax_freq.set_ylabel("Frekvencija [Hz]")
        ax_freq.set_xlabel("Vrijeme [s]")
        ax_freq.grid(linestyle='dotted', linewidth=1)
        ax_freq.legend()
        ax_freq.xaxis.set_major_locator(plt.MaxNLocator(10))
        fig_freq.tight_layout()

    # Prikaz frekvencija sabirnica
    if f_busHz:
        fig_fbus, ax_fbus = plt.subplots(figsize=(12, 5))
        for label, f in f_busHz:
            ax_fbus.plot(t, f, label='f_' + label)
        ax_fbus.set_title('Frekvencije svih sabirnica (iz θ)')
        ax_fbus.set_ylabel('Frekvencija [Hz]')
        ax_fbus.set_xlabel('Vrijeme (t) [s]')
        ax_fbus.grid(linestyle='dotted', linewidth=1)
        ax_fbus.legend()
        ax_fbus.xaxis.set_major_locator(plt.MaxNLocator(10))
        fig_fbus.tight_layout()

    # Prikaz ANN signala
    try:
        if "u_ann1_out" in header and "u_ann2_out" in header:
            fig_ann, ax_ann = plt.subplots(figsize=(12, 4))
            ax_ann.plot(t, columns[header.index("u_ann1_out") - 1], label='u_ann1')
            ax_ann.plot(t, columns[header.index("u_ann2_out") - 1], label='u_ann2')
            ax_ann.set_title('ANN kontrolni signali')
            ax_ann.set_ylabel('Vrijednost')
            ax_ann.set_xlabel('Vrijeme [s]')
            ax_ann.grid(linestyle='dotted', linewidth=1)
            ax_ann.legend()
            ax_ann.xaxis.set_major_locator(plt.MaxNLocator(10))
            fig_ann.tight_layout()
    except (ValueError, IndexError):
        print("ANN signali nisu pronađeni u podacima")

    # Prikaži sve figure
    plt.show()
import numpy as np
import matplotlib.pyplot as plt

# Parameter
L = 100  # Gittergröße
T = 2.0  # Temperatur
J = 1.0  # Kopplungskonstante
k_B = 1.0  # Boltzmann-Konstante
n_steps = 10000  # Anzahl der Monte-Carlo-Schritte

# Initialisiere das Gitter mit zufälligen Spins
spins = np.random.choice([-1, 1], size=(L, L))

# Speichere den Anfangszustand
initial_spins = spins.copy()

# Energieänderung berechnen
def delta_E(spins, i, j):
    S = spins[i, j]
    neighbors = spins[(i+1)%L, j] + spins[i, (j+1)%L] + spins[(i-1)%L, j] + spins[i, (j-1)%L]
    return 2 * J * S * neighbors

# Metropolis-Algorithmus
for step in range(n_steps):
    i = np.random.randint(0, L)
    j = np.random.randint(0, L)
    dE = delta_E(spins, i, j)
    if dE < 0 or np.random.rand() < np.exp(-dE / (k_B * T)):
        spins[i, j] *= -1

# Berechne die Energieänderungen für den Endzustand
delta_E_matrix = np.zeros((L, L))
for i in range(L):
    for j in range(L):
        delta_E_matrix[i, j] = delta_E(spins, i, j)

# Erstelle die Plots
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Plot des Anfangszustands
axs[0].imshow(initial_spins, cmap='gray')
axs[0].set_title('Anfangszustand')

# Plot des Endzustands
axs[1].imshow(spins, cmap='gray')
axs[1].set_title('Endzustand')

# Plot der Energieänderungen
cax = axs[2].imshow(delta_E_matrix, cmap='coolwarm')
axs[2].set_title('Energieänderungen')
fig.colorbar(cax, ax=axs[2], orientation='vertical')

plt.show()

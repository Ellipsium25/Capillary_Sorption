import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parameters
r = 1e-6          # pore radius [m]
gamma = 0.072     # surface tension [N/m]
theta = 0         # contact angle [rad]
mu = 1e-3         # viscosity [Pa·s]
P0 = 1e5          # ambient pressure [Pa]
V0 = 1e-12        # initial trapped air volume [m^3]
A = np.pi * r**2  # pore cross-sectional area [m^2]
r_hole = 1e-3     # perforation radius [m]

# Capillary pressure
Pc = 2 * gamma * np.cos(theta) / r

# Bubble release threshold
Pbubble = P0 + 2 * gamma / r_hole

# ODE system
def dLdt(t, L, V_air):
    V = V_air - A * L
    if V <= 0:
        return 0
    P_air = P0 * V_air / V
    DeltaP = Pc - (P_air - P0)
    if DeltaP <= 0:
        return 0
    return (r / (4 * mu * L)) * DeltaP

# Simulation loop with bubble release
t_span = (0, 10)
dt = 0.01
times = [0]
lengths = [1e-9]  # small initial penetration
V_air = V0

L = lengths[-1]
for t in np.arange(0, t_span[1], dt):
    # integrate one step
    dL = dLdt(t, L, V_air) * dt
    L += dL
    times.append(t)
    lengths.append(L)

    # check bubble release
    V = V_air - A * L
    if V > 0:
        P_air = P0 * V_air / V
        if P_air >= Pbubble:
            V_air = V0  # reset trapped air volume

# Plot sorption curve
plt.plot(times, lengths)
plt.xlabel("Time [s]")
plt.ylabel("Penetration length L(t) [m]")
plt.title("Capillary sorption with bubble release")
plt.show()

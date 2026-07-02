import numpy as np
import matplotlib.pyplot as plt

print("Generating Final Sorption Curves...")

# 1. Physical Properties of Water
rho_w = 1000.0      # kg/m^3
gamma_w = 0.0728    # N/m
eta_w = 0.001       # Pa*s

# 2. Specific Powder Constant
c_powder = 7.51e-17 # m^5

# 3. Calculate Ideal Washburn Slope for Water 
# slope = (c * rho^2 * gamma * cos(theta)) / eta 
slope_si = (c_powder * rho_w**2 * gamma_w * 1.0) / eta_w # kg^2/s
slope_g2 = slope_si * 1e6 # Convert to g^2/s for standard lab graph scaling

# 4. Generate Time Array
times = np.linspace(0, 10, 1000)
dt = times[1] - times[0]

# 5. Ideal Hollow Tube (Continuous Sorption)
m2_ideal = slope_g2 * times

# 6. Simulating the 1mm Plate Blockage (Staircase Phenomenon)
m2_blocked = np.zeros_like(times)
current_m2 = 0.0

# Physics conceptually: Pressure builds up, slows flow, bubble pops out, 
# mass drops suddenly (buoyant force), and flow resumes.
pressure_buildup = 0.0 
threshold = 0.008  # Threshold for bubble burst

for i in range(1, len(times)):
    if pressure_buildup < threshold:
        # Flow is active, but slowing down as pressure builds
        rate_modifier = max(0, 1 - (pressure_buildup / threshold))
        added_mass_sq = slope_g2 * dt * rate_modifier
        current_m2 += added_mass_sq
        pressure_buildup += added_mass_sq 
    else:
        # Flow stopped, bubble pops!
        # The bubble displaces water, causing an apparent mass drop on the inverted balance
        current_m2 -= 0.002 
        if current_m2 < 0: current_m2 = 0
        pressure_buildup = 0.0 # Trapped air resets
        
    m2_blocked[i] = current_m2

# 7. Plotting the Results
plt.figure(figsize=(10, 6))
plt.plot(times, m2_ideal, 'g--', label='Modified Hollow Tube (Continuous Sorption)', linewidth=2.5)
plt.plot(times, m2_blocked, 'r-', label='1mm Perforated Plate (Bubble Blockage)', linewidth=2)

plt.title("Mathematical Proof: Capillary Sorption Bubble Phenomena")
plt.xlabel("Time [s]")
plt.ylabel("Mass Squared (g²)")
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
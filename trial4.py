import matplotlib.pyplot as plt
import numpy as np

# --- Physical Parameters ---
gamma = 0.0728          # Surface tension of water at 20°C (N/m)
R_0 = 0.5 * 1e-3        # Perforated plate pore radius (1mm diameter -> 0.5mm radius in meters)
r_p = 5.0 * 1e-6        # Assumed effective powder pore radius (5 microns in meters)

# --- Mathematical Model Calculations ---
# 1. Critical bubble resistance pressure (constant for a fixed 1mm hole)
P_bubble_max = (2 * gamma) / R_0

# 2. Driving capillary pressure as a function of powder contact angle (0 to 90 degrees)
theta_degrees = np.linspace(0, 90, 300)
theta_radians = np.radians(theta_degrees)
P_drive = (2 * gamma * np.cos(theta_radians)) / r_p

# --- Find the Intersection/Inhibition Threshold ---
# Inhibition happens when P_drive <= P_bubble_max
inhibition_indices = np.where(P_drive <= P_bubble_max)[0]
threshold_angle = theta_degrees[inhibition_indices[0]] if len(inhibition_indices) > 0 else 90

# --- Plotting the Visualization ---
plt.figure(figsize=(10, 6), dpi=100)

# Plot pressures
plt.plot(theta_degrees, P_drive, color='blue', lw=2.5, label=r'Capillary Sorption Drive ($P_{\mathrm{drive}}$)')
plt.axhline(y=P_bubble_max, color='red', linestyle='--', lw=2, label=r'Max Bubble Resistance ($P_{\mathrm{bubble, max}}$)')

# Fill the regions to visually represent the state of the system
plt.axvspan(0, threshold_angle, color='green', alpha=0.15, label='Active Sorption Region')
plt.axvspan(threshold_angle, 90, color='red', alpha=0.15, label='Sorption Inhibition Region (Bubble Blocks Flow)')

# Mark the exact mathematical crossover point
plt.vlines(threshold_angle, 0, P_bubble_max, color='black', linestyle=':', alpha=0.7)
plt.scatter([threshold_angle], [P_bubble_max], color='black', zorder=5)
plt.text(threshold_angle + 1, P_bubble_max + 1000, f'Critical Angle: {threshold_angle:.1f}°', 
         fontsize=10, weight='bold', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# Labels and Styling
plt.title('Physical Phase Space: Sorption vs. Bubble Inhibition', fontsize=14, pad=15, weight='bold')
plt.xlabel(r'Powder Wetting Contact Angle, $\theta_p$ (Degrees)', fontsize=12)
plt.ylabel('Pressure (Pascal, Pa)', fontsize=12)
plt.xlim(0, 90)
plt.ylim(0, max(P_drive) * 1.05)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right', fontsize=11, framealpha=0.95)

# Display the final graph
plt.tight_layout()
plt.show()

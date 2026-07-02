import numpy as np
import matplotlib.pyplot as plt

# --- 1. Physical Constants ---
gamma = 0.0728         # Surface tension of water (N/m)
eta = 0.001            # Viscosity of water (Pa.s)
rho = 1000.0           # Density of water (kg/m^3)
P0 = 101325.0          # Atmospheric pressure (Pa)

# Powder Bed Parameters (Estimated for demonstration)
r_p = 100e-6             # Effective pore radius of powder (5 micrometers)
theta_p = np.radians(60) # Contact angle (60 degrees - slightly hydrophobic to show inhibition)
phi = 0.4              # Porosity of powder bed
h_plate = 0.002        # Thickness of the perforated plate (2 mm)

# Capillary Driving Pressure
Pc = (2 * gamma * np.cos(theta_p)) / r_p

# --- 2. Test Cases: Varying Geometry ---
# We keep total area A_eff roughly constant (e.g., ~7.85e-5 m^2) to make it a fair comparison.
# Tuple format: (number_of_holes, hole_radius_in_meters, label)
test_cases = [
    (2500, 0.1e-3, "Case 1: 2500 Micro-Holes (r = 0.1mm)"),  
    (400,  0.25e-3, "Case 2: 400 Small Holes (r = 0.25mm)"), 
    (1,    5.0e-3, "Case 3: 1 Big Pore (r = 5.0mm)")        
]

# --- 3. Integration Parameters ---
t_max = 120            # Simulate for 120 seconds
dt = 0.01
times = np.arange(0, t_max, dt)

# Setup Plot
plt.figure(figsize=(12, 7))

# --- 4. The Main Solver Loop ---
for n, R0, label in test_cases:
    
    # Calculate geometric constraints
    A_eff = n * np.pi * (R0**2)
    V0 = A_eff * h_plate
    P_bubble_threshold = (2 * gamma) / R0
    
    # Pre-calculate the constant multiplier for the ODE (for m^2)
    # ODE: d(m^2)/dt = [ r_p^2 * (A_eff * phi * rho)^2 / (4 * eta) ] * (Pc - P_back)
    K = (r_p**2 * (A_eff * phi * rho)**2) / (4 * eta)
    
    m2_array = []
    m2_current = 0.0
    
    for t in times:
        # Prevent negative mass due to numerical noise
        if m2_current < 0: m2_current = 0
        
        m_current = np.sqrt(m2_current)
        V_water = m_current / rho
        
        # Calculate Boyle's Law Back-Pressure
        if V_water >= V0: 
            V_water = V0 - 1e-12 # Prevent division by zero
            
        P_back_boyle = P0 * (V_water / (V0 - V_water))
        
        # Apply the Universal Piecewise Condition
        if P_back_boyle >= P_bubble_threshold:
            P_back_eff = P_bubble_threshold # Continuous bubbling (capped penalty)
        else:
            P_back_eff = P_back_boyle       # Sealed phase (logarithmic rise)
            
        # Check Inhibition State (Total Lock-up)
        # If back pressure matches or exceeds capillary pressure BEFORE a bubble can form
        if P_back_eff >= Pc:
            P_back_eff = Pc 
            
        # Calculate derivative: d(m^2)/dt
        dm2_dt = K * (Pc - P_back_eff)
        
        # Euler step forward
        m2_next = m2_current + (dm2_dt * dt)
        m2_array.append(m2_next)
        m2_current = m2_next
        
    # Convert results to g^2 for better readability on plot
    m2_g2 = np.array(m2_array) * 1e6
    
    # Plot formatting
    if n == 100: color, style = 'red', '-'
    elif n == 25: color, style = 'orange', '--'
    else: color, style = 'green', '-.'
        
    plt.plot(times, m2_g2, label=label, color=color, linestyle=style, linewidth=2.5)

# --- 5. Finalize Plot ---
plt.title("Capillary Sorption: Transition from Many Small Holes to One Big Pore", fontsize=14, pad=15)
plt.xlabel("Time [s]", fontsize=12)
plt.ylabel("Mass Squared [g²]", fontsize=12)
plt.legend(loc="upper left", fontsize=11)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


# Define the parameters for the demand functions of High Income (HI) and Low Income (LI) groups
# Demand function for HI: q_HI = A - B * p_HI
# Demand function for LI: q_LI = C - D * p_LI
A, B, C, D = 600, 30, 800, 50  # A, B for HI and C, D for LI

# Marginal cost of supplying energy in £/MWh
MC = 50

# Elasticities of demand for HI and LI groups. Negative values indicate inverse relationship
# between price and quantity demanded, which is typical in demand functions.
epsilon_HI, epsilon_LI = -0.5, -1.5  # Less elastic for HI, more elastic for LI

# Fixed costs that the energy provider needs to cover and the number of days per month
fixed_costs = 2_000_000  # Monthly fixed costs in $
days_per_month = 30  # Average number of days in a month for daily revenue calculation

# Capacity constraint (maximum energy supply per day) and daily break-even revenue
capacity_constraint = 1000  # MWh per day
break_even_revenue = fixed_costs / days_per_month  # Daily revenue needed to break even

# Uniform pricing scenario: A single price for both groups
# Define functions for total demand and revenue with a uniform price
def total_demand_uniform_price(price):
    # Total demand at a given uniform price
    return (A - B * price) + (C - D * price)

def total_revenue_uniform_price(price):
    # Total revenue at a given uniform price
    return price * total_demand_uniform_price(price)

# Define a function for the break-even constraint under uniform pricing
def break_even_uniform_price_constraint(price):
    # Revenue should match the daily break-even requirement
    return total_revenue_uniform_price(price) - break_even_revenue

# Solve for the uniform price that meets the break-even requirement
uniform_price_initial_guess = 10
uniform_price_solution = fsolve(break_even_uniform_price_constraint, uniform_price_initial_guess)[0]

# Function to calculate consumer surplus: CS = 0.5 * base * height
def calculate_consumer_surplus(a, b, price):
    base = a - b * price  # base of the demand triangle
    height = a / b - price  # height of the demand triangle
    return 0.5 * base * height  # Area of triangle representing consumer surplus

# Consumer surplus for HI and LI under uniform pricing
cs_HI_uniform = calculate_consumer_surplus(A, B, uniform_price_solution)
cs_LI_uniform = calculate_consumer_surplus(C, D, uniform_price_solution)

# Ramsey pricing formula: p_i - MC = k * p_i * epsilon_i
# The goal is to find prices for HI and LI that satisfy this formula and meet the capacity and break-even constraints

# Define a function to calculate total revenue based on Ramsey pricing
def revenue(k):
    # Prices for HI and LI are calculated using the Ramsey formula
    p_HI = MC / (1 - k * epsilon_HI)
    p_LI = MC / (1 - k * epsilon_LI)
    
    # Quantities demanded for HI and LI are derived from the demand functions
    q_HI = A - B * p_HI
    q_LI = C - D * p_LI
    
    # Total revenue calculation
    return p_HI * q_HI + p_LI * q_LI

# Define a function for the break-even constraint
def break_even_constraint(k):
    # The revenue must match the break-even revenue for sustainability
    return revenue(k) - break_even_revenue

# Solve for k using fsolve, with an initial guess
k_initial = -0.1
k_solution = fsolve(break_even_constraint, k_initial)[0]

# Calculate the prices for HI and LI using the solved value of k
p_HI_solution = MC / (1 - k_solution * epsilon_HI)
p_LI_solution = MC / (1 - k_solution * epsilon_LI)


# Consumer surplus for HI and LI under Ramsey pricing
cs_HI_ramsey = calculate_consumer_surplus(A, B, p_HI_solution)
cs_LI_ramsey = calculate_consumer_surplus(C, D, p_LI_solution)


# Output the results
print("Ramsey Pricing:")
print(f"High Income Price: ${p_HI_solution:.2f}, Consumer Surplus: ${cs_HI_ramsey:.2f}")
print(f"Low Income Price: ${p_LI_solution:.2f}, Consumer Surplus: ${cs_LI_ramsey:.2f}")
print("\nUniform Pricing:")
print(f"Uniform Price: ${uniform_price_solution:.2f}")
print(f"High Income Consumer Surplus: ${cs_HI_uniform:.2f}")
print(f"Low Income Consumer Surplus: ${cs_LI_uniform:.2f}")

print("\nTotal Consumer Surplus under Ramsey Pricing:")
print(cs_HI_ramsey + cs_LI_ramsey)
print("Total Consumer Surplus under Uniform Pricing:")
print(cs_HI_uniform + cs_LI_uniform)


# Plotting

# Function to plot both HI and LI demand curves and consumer surpluses on the same graph
# with total consumer surplus annotation
def plot_combined_demand_curves_with_total_cs(a_HI, b_HI, price_HI, a_LI, b_LI, price_LI, title, cs_HI, cs_LI):
    # Generate a range of quantities for HI and LI
    quantities_HI = np.linspace(0, a_HI, 500)
    quantities_LI = np.linspace(0, a_LI, 500)
    
    # Calculate prices for each quantity using the inverse demand function
    prices_HI = (a_HI - quantities_HI) / b_HI
    prices_LI = (a_LI - quantities_LI) / b_LI

    # Calculate total consumer surplus
    total_cs = cs_HI + cs_LI
    
    # Create the plot
    plt.figure(figsize=(12, 8))

    # Plot HI demand curve and consumer surplus
    plt.plot(quantities_HI, prices_HI, label="HI Demand Curve")
    plt.fill_between(quantities_HI, prices_HI, price_HI, where=(quantities_HI <= (a_HI - b_HI * price_HI)), 
                     color='lightblue', alpha=0.5, label=f"HI CS: ${cs_HI:.2f}")

    # Plot LI demand curve and consumer surplus
    plt.plot(quantities_LI, prices_LI, label="LI Demand Curve", color='orange')
    plt.fill_between(quantities_LI, prices_LI, price_LI, where=(quantities_LI <= (a_LI - b_LI * price_LI)), 
                     color='lightgreen', alpha=0.5, label=f"LI CS: ${cs_LI:.2f}")

    # Price lines for HI and LI
    plt.axhline(y=price_HI, color='blue', linestyle='--', label=f"HI Price = ${price_HI:.2f}")
    plt.axhline(y=price_LI, color='green', linestyle='--', label=f"LI Price = ${price_LI:.2f}")

    # Total consumer surplus annotation
    plt.annotate(f"Total CS: ${total_cs:.2f}", xy=(0.05, 0.95), xycoords='axes fraction', 
                 fontsize=12, bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='yellow'))

    # Labels and title
    plt.xlabel("Quantity Demanded")
    plt.ylabel("Price")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot for both groups under Uniform Pricing with total consumer surplus annotation
plot_combined_demand_curves_with_total_cs(A, B, uniform_price_solution, C, D, uniform_price_solution, 
                                          "Uniform Pricing - High Income & Low Income Groups", 
                                          cs_HI_uniform, cs_LI_uniform)

# Plot for both groups under Ramsey Pricing with total consumer surplus annotation
plot_combined_demand_curves_with_total_cs(A, B, p_HI_solution, C, D, p_LI_solution, 
                                          "Ramsey Pricing - High Income & Low Income Groups", 
                                          cs_HI_ramsey, cs_LI_ramsey)



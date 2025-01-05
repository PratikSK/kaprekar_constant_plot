import streamlit as st
import matplotlib.pyplot as plt

# Function to generate the Kaprekar sequence and intermediates
def kaprekar_with_intermediates(num):
    steps = []
    intermediates = []
    while num != 6174:
        steps.append(num)
        desc = int("".join(sorted(str(num).zfill(4), reverse=True)))
        asc = int("".join(sorted(str(num).zfill(4))))
        intermediates.append((desc, asc))  # Store intermediate values
        num = desc - asc
    steps.append(6174)
    return steps, intermediates

# Function to validate user input
def is_valid_kaprekar_input(num):
    if len(str(num)) != 4:
        return False
    if len(set(str(num))) == 1:
        return False
    return True

# Function to plot Kaprekar sequence
def plot_kaprekar_sequence(start_number, sequence, intermediates):
    step_positions = list(range(1, len(sequence) + 1))
    asc_numbers = [asc for _, asc in intermediates + [(6174, 6174)]]
    desc_numbers = [desc for desc, _ in intermediates + [(6174, 6174)]]

    # Create plot
    plt.figure(figsize=(10, 6))
    step = 1
    for i, (num, (desc, asc)) in enumerate(zip(sequence, intermediates + [(6174, 6174)])):
        plt.plot([step, step], [desc, asc], linestyle="dotted", color="red")
        if i < len(sequence) - 1:
            plt.plot([step, step + 1], [num, sequence[i + 1]], linestyle="solid", color="blue")
        plt.scatter([step, step, step], [num, desc, asc], color="green", s=50)
        plt.text(step, num + 200, f"{num}", fontsize=10, color="blue", ha="center", va="bottom")
        if i == len(sequence) - 1:
            plt.text(step, desc - 200, f"{desc} (desc)", fontsize=9, ha="right", va="center")
            plt.text(step + 0.1, asc - 200, f"{asc} (asc)", fontsize=9, ha="left", va="center")
        else:
            plt.text(step, desc, f"{desc} (desc)", fontsize=9, ha="right", va="center")
            plt.text(step + 0.1, asc, f"{asc} (asc)", fontsize=9, ha="left", va="center")
        step += 1

    plt.plot(step_positions, asc_numbers, linestyle="dashed", color="orange")
    plt.plot(step_positions, desc_numbers, linestyle="dashed", color="purple")
    plt.fill_between(step_positions, asc_numbers, desc_numbers, color="gray", alpha=0.2, hatch="//")
    # plt.axhline(y=6174, color="red", linestyle="solid", linewidth=1.5)
    plt.axhline(y=6174, color="red", linestyle="solid", linewidth=1.5, label="Kaprekar Constant: 6174")
    plt.title(f"Numbers Converging at Kaprekar's Constant (Start: {start_number})", fontsize=14)
    plt.xlabel("Step Number", fontsize=12)
    plt.ylabel("Number", fontsize=12)
    plt.grid(True)
    st.pyplot(plt)

# Streamlit UI
st.title("Kaprekar Constant Visualizer")
st.write("Input a 4-digit number with at least two distinct digits to see its Kaprekar sequence.")

# Default number and user input
default_number = 9831
user_input = st.text_input("Enter a 4-digit number:", value=str(default_number))

if user_input.isdigit() and is_valid_kaprekar_input(int(user_input)):
    start_number = int(user_input)
    sequence, intermediates = kaprekar_with_intermediates(start_number)
    st.success(f"Valid input! Plotting Kaprekar sequence for {start_number}.")
    plot_kaprekar_sequence(start_number, sequence, intermediates)

    # Add explanation and GitHub link below the plot
    st.write("""
        ### What is Kaprekar's Constant?
        Kaprekar's constant, **6174**, is a unique number that all four-digit numbers with at least two distinct digits converge to
        after repeatedly applying the following process:
        1. Arrange the digits in descending and ascending order to form two numbers.
        2. Subtract the smaller number from the larger number.
        3. Repeat the process with the result until you reach **6174**.
    """)
    st.markdown("[View the code on GitHub](https://github.com/PratikSK/kaprekar_constant_plot.git)")

else:
    st.warning("Please enter a valid 4-digit number with at least two distinct digits.")

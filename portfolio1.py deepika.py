import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd

def calculate_advanced_portfolio():
    try:
        # Step 1: Get user input
        stock_names = stock_entry.get().split(',')
        weights = list(map(float, weight_entry.get().split(',')))
        returns = list(map(float, return_entry.get().split(',')))

        if len(stock_names) != len(weights) or len(weights) != len(returns):
            messagebox.showerror("Error", "Number of stocks, returns, and weights must match")
            return

        if round(sum(weights), 2) != 1.0:
            messagebox.showerror("Error", "Weights must add up to 1.0")
            return

        weights = np.array(weights)
        returns = np.array(returns)

        # Step 2: Simulate covariance matrix (in real use-case, this comes from data)
        np.random.seed(42)
        daily_returns = np.random.normal(loc=returns / 252, scale=0.01, size=(252, len(stock_names)))
        cov_matrix = np.cov(daily_returns.T) * 252

        # Step 3: Calculate expected return
        portfolio_return = np.dot(returns, weights)

        # Step 4: Calculate variance and standard deviation
        variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        std_dev = np.sqrt(variance)

        # Step 5: Sharpe Ratio (assume risk-free rate = 2%)
        rf = 0.02
        sharpe_ratio = (portfolio_return - rf) / std_dev

        # Step 6: Display output
        output = f"Portfolio Analysis:\n\n"
        output += f"Expected Annual Return: {portfolio_return * 100:.2f}%\n"
        output += f"Portfolio Risk (Std Dev): {std_dev * 100:.2f}%\n"
        output += f"Sharpe Ratio: {sharpe_ratio:.2f}\n\n"
        output += f"Covariance Matrix:\n{pd.DataFrame(cov_matrix, index=stock_names, columns=stock_names).round(4)}"

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, output)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Advanced Portfolio Manager")
root.geometry("500x600")

tk.Label(root, text="Enter Stock Names (comma separated):").pack()
stock_entry = tk.Entry(root, width=50)
stock_entry.pack()

tk.Label(root, text="Enter Weights (comma separated, total = 1.0):").pack()
weight_entry = tk.Entry(root, width=50)
weight_entry.pack()

tk.Label(root, text="Enter Expected Annual Returns (e.g. 0.10, 0.08):").pack()
return_entry = tk.Entry(root, width=50)
return_entry.pack()

tk.Button(root, text="Calculate Portfolio", command=calculate_advanced_portfolio).pack(pady=10)

result_text = tk.Text(root, height=25, width=60)
result_text.pack()

root.mainloop()
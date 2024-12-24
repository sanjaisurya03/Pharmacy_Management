# Pharmacy Management System

## Overview
The Pharmacy Management System is a GUI-based application built using Python and Tkinter. It integrates with a MySQL database to manage medicines, sales, and customers efficiently. The application features an interactive dashboard for visualizing sales data, making it easier for pharmacy staff to monitor inventory and sales trends.

---

## Features

- **Interactive Dashboard**: Visualize sales data with bar charts.
- **Medicine Management**: Add and view medicines with their pricing.
- **Sales Management**: Make sales, generate bills, and view temporary sales.
- **Database Integration**: Automatically creates and manages a MySQL database for storing medicines and sales information.

---

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python libraries:
  - `tkinter`
  - `ttkbootstrap`
  - `mysql-connector-python`
  - `matplotlib`

Install the required Python libraries using pip:
```bash
pip install ttkbootstrap mysql-connector-python matplotlib
```

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pharmacy-management-system
   ```

2. Configure MySQL credentials:
   - Update the `host`, `user`, and `password` fields in the code to match your MySQL configuration.

3. Run the application:
   ```bash
   python PharmeasyManagement.py
   ```

---

## Usage

- **Dashboard Tab**:
  - View a bar chart displaying the sales data for various medicines.

- **Medicine Tab**:
  - Add new medicines with their name and price.
  - View the list of all medicines in the database.

- **Sales Tab**:
  - Make a new sale by selecting a medicine and entering the quantity.
  - Generate bills and update sales records.
  - View temporary sales records.

---

## Code Structure

- **`create_database_if_not_exists`**: Ensures the necessary database and tables are created.
- **`PharmacyManagementApp`**: The main application class managing the GUI and user interactions.
- **Tabs**:
  - Dashboard: Visualize sales data.
  - Medicine: Manage medicines.
  - Sales: Manage and record sales transactions.

---

## Contribution

Contributions are welcome! Please fork the repository and create a pull request for any improvements or new features.

---

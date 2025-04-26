from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import calendar
import time

class SalaryReport:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Salary Report")
        self.root.config(bg="#f4f5f7")
        self.root.resizable(False, False)
        self.root.focus_force()
        
        # Variables
        self.var_emp_id = StringVar()
        self.var_month = StringVar()
        self.var_year = StringVar()
        self.var_total_days = StringVar()
        self.var_present_days = StringVar()
        self.var_absent_days = StringVar()
        self.var_base_salary = StringVar()
        self.var_final_salary = StringVar()
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Title
        title = Label(self.root, text="Salary Report Generation", 
                     font=("Helvetica", 15, "bold"), bg="#2196F3", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)
        
        # Left Frame - Salary Calculation
        left_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        left_frame.place(x=10, y=60, width=400, height=430)
        
        left_title = Label(left_frame, text="Salary Calculation", 
                          font=("Helvetica", 15), bg="#2196F3", fg="white")
        left_title.pack(side=TOP, fill=X)
        
        # Employee Selection
        lbl_emp = Label(left_frame, text="Select Employee", font=("Helvetica", 12), bg="white")
        lbl_emp.place(x=10, y=60)
        
        self.cmb_emp = ttk.Combobox(left_frame, textvariable=self.var_emp_id,
                                   state='readonly', justify=CENTER, font=("Helvetica", 12))
        self.cmb_emp.place(x=160, y=60, width=200)
        self.fill_employees()
        
        # Month Selection
        lbl_month = Label(left_frame, text="Select Month", font=("Helvetica", 12), bg="white")
        lbl_month.place(x=10, y=100)
        
        months = [str(i) for i in range(1, 13)]
        cmb_month = ttk.Combobox(left_frame, textvariable=self.var_month,
                                values=months, state='readonly', justify=CENTER, font=("Helvetica", 12))
        cmb_month.place(x=160, y=100, width=200)
        cmb_month.current(current_month - 1)  # Set to current month
        
        # Year Selection
        lbl_year = Label(left_frame, text="Select Year", font=("Helvetica", 12), bg="white")
        lbl_year.place(x=10, y=140)
        
        years = [str(i) for i in range(current_year - 5, current_year + 1)]
        cmb_year = ttk.Combobox(left_frame, textvariable=self.var_year,
                               values=years, state='readonly', justify=CENTER, font=("Helvetica", 12))
        cmb_year.place(x=160, y=140, width=200)
        cmb_year.current(5)  # Set to current year
        
        # Buttons
        btn_generate = Button(left_frame, text="Generate Report", command=self.generate_report,
                             font=("Helvetica", 12), bg="#4CAF50", fg="white", cursor="hand2")
        btn_generate.place(x=160, y=180, width=200, height=30)
        
        # Salary Details
        lbl_details = Label(left_frame, text="Salary Details", font=("Helvetica", 12, "bold"), bg="white")
        lbl_details.place(x=10, y=230)
        
        # Working Days
        lbl_total_days = Label(left_frame, text="Total Working Days", 
                              font=("Helvetica", 12), bg="white")
        lbl_total_days.place(x=10, y=270)
        
        txt_total_days = Entry(left_frame, textvariable=self.var_total_days,
                              font=("Helvetica", 12), bg="#f4f5f7", state='readonly')
        txt_total_days.place(x=160, y=270, width=200)
        
        # Present Days
        lbl_present = Label(left_frame, text="Present Days", font=("Helvetica", 12), bg="white")
        lbl_present.place(x=10, y=300)
        
        txt_present = Entry(left_frame, textvariable=self.var_present_days,
                           font=("Helvetica", 12), bg="#f4f5f7", state='readonly')
        txt_present.place(x=160, y=300, width=200)
        
        # Absent Days
        lbl_absent = Label(left_frame, text="Absent Days", font=("Helvetica", 12), bg="white")
        lbl_absent.place(x=10, y=330)
        
        txt_absent = Entry(left_frame, textvariable=self.var_absent_days,
                          font=("Helvetica", 12), bg="#f4f5f7", state='readonly')
        txt_absent.place(x=160, y=330, width=200)
        
        # Base Salary
        lbl_base = Label(left_frame, text="Base Salary", font=("Helvetica", 12), bg="white")
        lbl_base.place(x=10, y=360)
        
        txt_base = Entry(left_frame, textvariable=self.var_base_salary,
                        font=("Helvetica", 12), bg="#f4f5f7", state='readonly')
        txt_base.place(x=160, y=360, width=200)
        
        # Final Salary
        lbl_final = Label(left_frame, text="Final Salary", font=("Helvetica", 12, "bold"), bg="white")
        lbl_final.place(x=10, y=390)
        
        txt_final = Entry(left_frame, textvariable=self.var_final_salary,
                         font=("Helvetica", 12, "bold"), bg="#f4f5f7", state='readonly')
        txt_final.place(x=160, y=390, width=200)
        
        # Right Frame - Salary Records & Reports
        right_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        right_frame.place(x=420, y=60, width=670, height=430)
        
        # Search Frame
        search_frame = LabelFrame(right_frame, text="Salary Reports", font=("Helvetica", 12, "bold"),
                                 bd=2, relief=RIDGE, bg="white")
        search_frame.place(x=10, y=5, width=650, height=70)
        
        # Export/Print Buttons
        btn_export = Button(search_frame, text="Export Report", command=self.export_report,
                           font=("Helvetica", 12), bg="#FFC107", fg="black", cursor="hand2")
        btn_export.place(x=10, y=9, width=200, height=30)
        
        btn_print = Button(search_frame, text="Print Report", command=self.print_report,
                          font=("Helvetica", 12), bg="#2196F3", fg="white", cursor="hand2")
        btn_print.place(x=220, y=9, width=200, height=30)
        
        btn_clear = Button(search_frame, text="Clear", command=self.clear,
                          font=("Helvetica", 12), bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.place(x=430, y=9, width=200, height=30)
        
        # Salary Report Table Frame
        table_frame = Frame(right_frame, bd=3, relief=RIDGE)
        table_frame.place(x=10, y=80, width=650, height=335)
        
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)
        
        self.SalaryTable = ttk.Treeview(table_frame,
            columns=("emp_id", "name", "month", "year", "days_worked", "base_salary", "final_salary"),
            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SalaryTable.xview)
        scrolly.config(command=self.SalaryTable.yview)
        
        self.SalaryTable.heading("emp_id", text="Emp ID")
        self.SalaryTable.heading("name", text="Name")
        self.SalaryTable.heading("month", text="Month")
        self.SalaryTable.heading("year", text="Year")
        self.SalaryTable.heading("days_worked", text="Days")
        self.SalaryTable.heading("base_salary", text="Base Salary")
        self.SalaryTable.heading("final_salary", text="Final Salary")
        
        self.SalaryTable["show"] = "headings"
        
        self.SalaryTable.column("emp_id", width=80)
        self.SalaryTable.column("name", width=150)
        self.SalaryTable.column("month", width=60)
        self.SalaryTable.column("year", width=60)
        self.SalaryTable.column("days_worked", width=60)
        self.SalaryTable.column("base_salary", width=100)
        self.SalaryTable.column("final_salary", width=100)
        
        self.SalaryTable.pack(fill=BOTH, expand=1)
        self.show_salary_records()
    
    def fill_employees(self):
        """Fill the employee dropdown with available employees"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT eid, name FROM employee")
            employees = cur.fetchall()
            
            self.emp_list = []
            self.emp_dict = {}
            
            for emp in employees:
                self.emp_list.append(f"{emp[0]} - {emp[1]}")
                self.emp_dict[f"{emp[0]} - {emp[1]}"] = emp[0]
            
            self.cmb_emp['values'] = self.emp_list
            if self.emp_list:
                self.cmb_emp.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading employees: {str(e)}", parent=self.root)
        finally:
            con.close()
    
    def generate_report(self):
        """Generate salary report for selected employee, month and year"""
        if not self.var_emp_id.get():
            messagebox.showerror("Error", "Please select an employee", parent=self.root)
            return
        
        try:
            selected = self.var_emp_id.get()
            emp_id = self.emp_dict[selected]
            month = int(self.var_month.get())
            year = int(self.var_year.get())
            
            # Calculate working days in month
            num_days = calendar.monthrange(year, month)[1]
            working_days = 0
            for day in range(1, num_days + 1):
                # Check if day is weekday (0-4 = Monday-Friday)
                if calendar.weekday(year, month, day) < 5:  
                    working_days += 1
            
            self.var_total_days.set(str(working_days))
            
            # Connect to database
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            
            # Get employee base salary
            cur.execute("SELECT salary FROM employee WHERE eid=?", (emp_id,))
            salary_data = cur.fetchone()
            
            if salary_data and salary_data[0]:
                base_salary = float(salary_data[0])
                self.var_base_salary.set(f"{base_salary:.2f}")
            else:
                base_salary = 0
                self.var_base_salary.set("0.00")
            
            # Get attendance data for the month
            start_date = f"{year}-{month:02d}-01"
            
            # Get last day of month
            if month == 12:
                next_month = 1
                next_year = year + 1
            else:
                next_month = month + 1
                next_year = year
                
            end_date = f"{next_year}-{next_month:02d}-01"
            
            cur.execute("""SELECT COUNT(DISTINCT date) FROM attendance 
                        WHERE emp_id=? AND date >= ? AND date < ?""", 
                       (emp_id, start_date, end_date))
            
            days_present = cur.fetchone()[0]
            if not days_present:
                days_present = 0
            
            days_absent = working_days - days_present
            
            self.var_present_days.set(str(days_present))
            self.var_absent_days.set(str(days_absent))
            
            # Calculate salary
            daily_rate = base_salary / working_days
            
            # Final salary calculation (deduct for absences)
            final_salary = base_salary - (days_absent * daily_rate)
            if final_salary < 0:
                final_salary = 0
            
            self.var_final_salary.set(f"{final_salary:.2f}")
            
            # Add to salary records table
            self.add_to_salary_table(emp_id, month, year, days_present, base_salary, final_salary)
            
            con.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}", parent=self.root)
    
    def add_to_salary_table(self, emp_id, month, year, days_worked, base_salary, final_salary):
        """Add the generated salary record to the table view"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Get employee name
            cur.execute("SELECT name FROM employee WHERE eid=?", (emp_id,))
            name = cur.fetchone()[0]
            
            # Add to table view
            self.SalaryTable.insert('', 0, values=(
                emp_id, name, month, year, days_worked, 
                f"{base_salary:.2f}", f"{final_salary:.2f}"
            ))
            
        except Exception as e:
            print(f"Error adding to salary table: {str(e)}")
        finally:
            con.close()
    
    def show_salary_records(self):
        """Show previous salary calculations"""
        # This would typically load from a salary_records table,
        # but we'll just clear the table for now as we're not storing these permanently
        self.SalaryTable.delete(*self.SalaryTable.get_children())
    
    def export_report(self):
        """Export the salary report to a file"""
        if not self.var_emp_id.get() or not self.var_final_salary.get():
            messagebox.showerror("Error", "No data to export", parent=self.root)
            return
        
        try:
            import csv
            from tkinter import filedialog
            
            file_path = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[("CSV files", "*.csv")],
                title="Save Salary Report"
            )
            
            if file_path:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    # Write header
                    writer.writerow(['Employee ID', 'Name', 'Month', 'Year', 'Working Days', 
                                    'Present Days', 'Absent Days', 'Base Salary', 'Final Salary'])
                    
                    # Write data
                    selected = self.var_emp_id.get()
                    emp_id = self.emp_dict[selected]
                    
                    # Get employee name
                    con = sqlite3.connect(database=r'ims.db')
                    cur = con.cursor()
                    cur.execute("SELECT name FROM employee WHERE eid=?", (emp_id,))
                    name = cur.fetchone()[0]
                    con.close()
                    
                    writer.writerow([
                        emp_id, name, self.var_month.get(), self.var_year.get(),
                        self.var_total_days.get(), self.var_present_days.get(),
                        self.var_absent_days.get(), self.var_base_salary.get(),
                        self.var_final_salary.get()
                    ])
                
                messagebox.showinfo("Success", "Report exported successfully", parent=self.root)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting report: {str(e)}", parent=self.root)
    
    def print_report(self):
        """Print the salary report"""
        if not self.var_emp_id.get() or not self.var_final_salary.get():
            messagebox.showerror("Error", "No data to print", parent=self.root)
            return
        
        try:
            # This would normally connect to a printer, but for demo purposes
            # we'll just create a text file with the report
            selected = self.var_emp_id.get()
            emp_id = self.emp_dict[selected]
            
            # Get employee name
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT name FROM employee WHERE eid=?", (emp_id,))
            name = cur.fetchone()[0]
            con.close()
            
            # Format date for filename
            current_time = time.strftime("%Y%m%d_%H%M%S")
            filename = f"salary_report_{emp_id}_{current_time}.txt"
            
            with open(filename, 'w') as f:
                f.write("=" * 50 + "\n")
                f.write(" " * 15 + "SALARY REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Employee ID: {emp_id}\n")
                f.write(f"Name: {name}\n")
                f.write(f"Month/Year: {self.var_month.get()}/{self.var_year.get()}\n\n")
                f.write(f"Total Working Days: {self.var_total_days.get()}\n")
                f.write(f"Present Days: {self.var_present_days.get()}\n")
                f.write(f"Absent Days: {self.var_absent_days.get()}\n\n")
                f.write(f"Base Salary: ${self.var_base_salary.get()}\n")
                f.write(f"FINAL SALARY: ${self.var_final_salary.get()}\n\n")
                f.write("=" * 50 + "\n")
                f.write(" " * 10 + "Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                f.write("=" * 50 + "\n")
            
            messagebox.showinfo("Success", f"Report saved as {filename}", parent=self.root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error printing report: {str(e)}", parent=self.root)
    
    def clear(self):
        """Clear all fields"""
        self.var_total_days.set("")
        self.var_present_days.set("")
        self.var_absent_days.set("")
        self.var_base_salary.set("")
        self.var_final_salary.set("")
        
        # Reset month and year to current
        current_month = datetime.now().month
        self.var_month.set(str(current_month))
        
        current_year = datetime.now().year
        self.var_year.set(str(current_year))
        
        # First employee in list
        if self.emp_list:
            self.cmb_emp.current(0)

if __name__ == "__main__":
    root = Tk()
    obj = SalaryReport(root)
    root.mainloop() 
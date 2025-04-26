from tkinter import*
from PIL import Image,ImageTk
from tkinter import messagebox
import time
import sqlite3
import os
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from attendance import AttendanceSystem
from salary_report import SalaryReport
from qr_generator import QRGenerator
from billing import billClass

class IMS:
    def __init__(self, root, emp_id=None, user_role=None):
        self.root = root
        self.emp_id = emp_id  # Store Employee ID
        self.user_role = user_role  # Store User Role (Admin/Employee)
        self.root.geometry("1350x700+110+80")
        self.root.title(f"Clothing Inventory Management System | {self.user_role}")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # Get Employee Name
        self.emp_name = self.get_employee_name()

        #------------- title --------------
        self.icon_title = PhotoImage(file="images/logo1.png")
        title_text = f"Inventory Management System - {self.emp_name} ({self.user_role})"
        title = Label(self.root, text=title_text, image=self.icon_title, compound=LEFT,
                      font=("times new roman", 30, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        #------------ logout button -----------
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"),
                            bg="yellow", cursor="hand2", command=self.logout)
        btn_logout.place(x=1150, y=10, height=50, width=150)
        #------------ clock -----------------
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #---------------- left menu ---------------
        # Create main left frame
        left_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        left_frame.place(x=0, y=102, width=200, height=565)
        
        # Logo and Menu label
        self.MenuLogo = Image.open("images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((200, 120))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        
        # Smaller logo to make more room for menu
        logo_frame = Frame(left_frame, bg="white", height=120)
        logo_frame.pack(fill=X)
        
        Label(logo_frame, image=self.MenuLogo, bg="white").pack(fill=X)
        Label(left_frame, text="Menu", font=("times new roman", 20), bg="#009688").pack(fill=X)
        
        # Create scrollable frame for menu
        menu_scroll = Frame(left_frame, bg="white")
        menu_scroll.pack(fill=BOTH, expand=True)
        
        # Add canvas and scrollbar
        self.canvas = Canvas(menu_scroll, bg="white")
        scrollbar = Scrollbar(menu_scroll, orient="vertical", command=self.canvas.yview)
        
        # Configure scrollbar
        self.scrollable_frame = Frame(self.canvas, bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        # Create window inside canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=180)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure canvas to scroll with mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Side button icon
        self.icon_side = PhotoImage(file="images/side.png")
        
        # Create all menu buttons - each with fixed height to ensure visibility
        button_height = 50  # Fixed height for each button
        
        # Employee button (admin only)
        if self.user_role == "Admin":
            btn_employee = Button(self.scrollable_frame, text="Employee", command=self.employee,
                               image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                               font=("times new roman", 16, "bold"), bg="white", bd=1, 
                               cursor="hand2", height=button_height)
            btn_employee.pack(fill=X)
        
        # Billing button (accessible to employees)
        btn_billing = Button(self.scrollable_frame, text="Billing", command=self.billing,
                          image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                          font=("times new roman", 16, "bold"), bg="white", bd=1, 
                          cursor="hand2", height=button_height)
        btn_billing.pack(fill=X)
        
        # Other buttons (for all users)
        btn_supplier = Button(self.scrollable_frame, text="Supplier", command=self.supplier,
                           image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                           font=("times new roman", 16, "bold"), bg="white", bd=1, 
                           cursor="hand2", height=button_height)
        btn_supplier.pack(fill=X)
        
        btn_category = Button(self.scrollable_frame, text="Category", command=self.category,
                           image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                           font=("times new roman", 16, "bold"), bg="white", bd=1, 
                           cursor="hand2", height=button_height)
        btn_category.pack(fill=X)
        
        btn_product = Button(self.scrollable_frame, text="Products", command=self.product,
                          image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                          font=("times new roman", 16, "bold"), bg="white", bd=1, 
                          cursor="hand2", height=button_height)
        btn_product.pack(fill=X)
        
        btn_sales = Button(self.scrollable_frame, text="Sales", command=self.sales,
                        image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                        font=("times new roman", 16, "bold"), bg="white", bd=1, 
                        cursor="hand2", height=button_height)
        btn_sales.pack(fill=X)
        
        btn_attendance = Button(self.scrollable_frame, text="Attendance", command=self.attendance,
                             image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                             font=("times new roman", 16, "bold"), bg="white", bd=1, 
                             cursor="hand2", height=button_height)
        btn_attendance.pack(fill=X)
        
        # Salary button (admin only)
        if self.user_role == "Admin":
            btn_salary = Button(self.scrollable_frame, text="Salary", command=self.salary_report,
                            image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                            font=("times new roman", 16, "bold"), bg="white", bd=1, 
                            cursor="hand2", height=button_height)
            btn_salary.pack(fill=X)
            
            # QR Codes button (admin only)
            btn_qr = Button(self.scrollable_frame, text="QR Codes", command=self.qr_generator,
                        image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                        font=("times new roman", 16, "bold"), bg="white", bd=1, 
                        cursor="hand2", height=button_height)
            btn_qr.pack(fill=X)
        
        btn_exit = Button(self.scrollable_frame, text="Exit", command=self.root.destroy,
                       image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                       font=("times new roman", 16, "bold"), bg="white", bd=1, 
                       cursor="hand2", height=button_height)
        btn_exit.pack(fill=X)

        # Add scroll indicator
        Label(left_frame, text="▼ Scroll for more ▼", bg="#e0e0e0", fg="#333333", font=("Arial", 8)).pack(fill=X, side=BOTTOM)

        #----------- content ----------------
        self.lbl_employee=Label(self.root,text="Total Employee\n{ 0 }",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier\n{ 0 }",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category\n{ 0 }",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product\n{ 0 }",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n{ 0 }",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)
        
        # Add attendance stats
        self.lbl_attendance=Label(self.root,text="Today's Attendance\n{ 0 }",bd=5,relief=RIDGE,bg="#8bc34a",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_attendance.place(x=1000,y=300,height=150,width=300)

        #------------ footer -----------------
        lbl_footer=Label(self.root,text="IMS-Inventory Management System | Group 4S\nFor any Technical Issues Contact: 09617965048",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()
    
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)
    def billing(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=billClass(self.new_win)
    def attendance(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=AttendanceSystem(self.new_win)
    def salary_report(self):
        # Additional check to ensure only admin can access this function
        if self.user_role == "Admin":
            self.new_win=Toplevel(self.root)
            self.new_obj=SalaryReport(self.new_win)
        else:
            messagebox.showerror("Access Denied", "Only Admin users can access Salary Reports")
    def qr_generator(self):
        # Additional check to ensure only admin can access this function
        if self.user_role == "Admin":
            self.new_win=Toplevel(self.root)
            self.new_obj=QRGenerator(self.new_win)
        else:
            messagebox.showerror("Access Denied", "Only Admin users can access QR Code Generator")

    def update_content(self):
        if not self.root.winfo_exists():  # Check if window still exists before updating
            return

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[ {len(product)} ]")

            cur.execute("SELECT * FROM category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {len(category)} ]")

            cur.execute("SELECT * FROM employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {len(employee)} ]")

            cur.execute("SELECT * FROM supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {len(supplier)} ]")

            bill = len(os.listdir("bill"))
            self.lbl_sales.config(text=f"Total Sales\n[ {bill} ]")
            
            # Get today's attendance count
            today = time.strftime("%Y-%m-%d")
            cur.execute("SELECT COUNT(*) FROM attendance WHERE date=?", (today,))
            attendance_count = cur.fetchone()[0]
            self.lbl_attendance.config(text=f"Today's Attendance\n[ {attendance_count} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}")

            # Only call after() if window is still open
            if self.root.winfo_exists():
                self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def get_employee_name(self):
        """ Fetch employee name from database using self.emp_id """
        if not self.emp_id:
            return "Unknown"
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM employee WHERE eid=?", (self.emp_id,))
        emp_name = cur.fetchone()
        con.close()
        return emp_name[0] if emp_name else "Unknown"

    def logout(self):
        """ Logout and return to login screen """
        self.root.destroy()
        import subprocess
        subprocess.run(["python", "login.py"])  # This will run login.py as a separate process

    def check_low_stock(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product WHERE qty::integer <= reorder_level")
            low_stock_items = cur.fetchall()
            if low_stock_items:
                messagebox.showwarning("Low Stock Alert", 
                    f"There are {len(low_stock_items)} items below reorder level!")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def show_sales_analytics(self):
        # Add charts for:
        # - Best selling items
        # - Sales by category
        # - Sales by season
        # - Size distribution
        # - Color popularity
        pass

if __name__ == "__main__":
    root = Tk()
    IMS(root, "E001", "Admin")  # Example test
    root.mainloop()
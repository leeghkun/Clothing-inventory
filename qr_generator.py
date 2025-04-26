from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import qrcode
import os

class QRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Employee QR Code Generator")
        self.root.config(bg="#f4f5f7")
        self.root.resizable(False, False)
        self.root.focus_force()
        
        # Variables
        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_department = StringVar()
        self.var_qr_data = StringVar()
        
        # Title
        title = Label(self.root, text="Employee QR Code Generator", 
                     font=("Helvetica", 15, "bold"), bg="#2196F3", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)
        
        # Employee Details Frame
        emp_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        emp_frame.place(x=50, y=70, width=500, height=380)
        
        emp_title = Label(emp_frame, text="Employee Details", 
                         font=("Helvetica", 15), bg="#2196F3", fg="white")
        emp_title.pack(side=TOP, fill=X)
        
        # Employee Selection
        lbl_emp = Label(emp_frame, text="Select Employee", font=("Helvetica", 12), bg="white")
        lbl_emp.place(x=30, y=60)
        
        # Fetch employees from database
        self.cmb_emp = ttk.Combobox(emp_frame, textvariable=self.var_emp_id,
                                   state='readonly', justify=CENTER, font=("Helvetica", 12))
        self.cmb_emp.place(x=170, y=60, width=280)
        self.cmb_emp.bind("<<ComboboxSelected>>", self.get_employee_data)
        self.fill_employees()
        
        # Employee Name (Read-only display)
        lbl_name = Label(emp_frame, text="Employee Name", font=("Helvetica", 12), bg="white")
        lbl_name.place(x=30, y=100)
        
        txt_name = Entry(emp_frame, textvariable=self.var_name,
                        font=("Helvetica", 12), bg="#f4f5f7", state='readonly')
        txt_name.place(x=170, y=100, width=280)
        
        # QR Code Data
        lbl_qr_data = Label(emp_frame, text="QR Code Data", font=("Helvetica", 12), bg="white")
        lbl_qr_data.place(x=30, y=140)
        
        # By default, QR data will be employee ID, but can be customized
        txt_qr_data = Entry(emp_frame, textvariable=self.var_qr_data,
                           font=("Helvetica", 12), bg="white")
        txt_qr_data.place(x=170, y=140, width=280)
        
        # Buttons
        btn_generate = Button(emp_frame, text="Generate QR Code", command=self.generate_qr,
                             font=("Helvetica", 12), bg="#4CAF50", fg="white", cursor="hand2")
        btn_generate.place(x=30, y=180, width=200, height=30)
        
        btn_clear = Button(emp_frame, text="Clear", command=self.clear,
                          font=("Helvetica", 12), bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.place(x=250, y=180, width=200, height=30)
        
        btn_save = Button(emp_frame, text="Save QR Code", command=self.save_qr,
                         font=("Helvetica", 12), bg="#FFC107", fg="black", cursor="hand2")
        btn_save.place(x=140, y=230, width=200, height=30)
        
        # Instructions
        lbl_instructions = Label(emp_frame, text="Instructions:", 
                                font=("Helvetica", 12, "bold"), bg="white")
        lbl_instructions.place(x=30, y=280)
        
        instruction_text = """
1. Select an employee from the dropdown
2. The QR data will be set to the employee ID by default
3. Click 'Generate QR Code' to create the QR code
4. Save the QR code to a file if needed
5. Print the QR code for the employee ID card
        """
        lbl_inst_details = Label(emp_frame, text=instruction_text, 
                                font=("Helvetica", 10), bg="white", justify=LEFT)
        lbl_inst_details.place(x=30, y=310)
        
        # QR Code Display Frame
        qr_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        qr_frame.place(x=600, y=70, width=450, height=380)
        
        qr_title = Label(qr_frame, text="QR Code", 
                        font=("Helvetica", 15), bg="#2196F3", fg="white")
        qr_title.pack(side=TOP, fill=X)
        
        # QR Code Display
        self.qr_code = Label(qr_frame, text="No QR\nCode\nAvailable", 
                            font=("Helvetica", 15), bg="white", fg="#607d8b")
        self.qr_code.place(x=75, y=100, width=300, height=300)
        
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
                self.emp_dict[f"{emp[0]} - {emp[1]}"] = emp
            
            self.cmb_emp['values'] = self.emp_list
            if self.emp_list:
                self.cmb_emp.current(0)
                # Trigger the event to load the first employee
                self.get_employee_data(None)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading employees: {str(e)}", parent=self.root)
        finally:
            con.close()
    
    def get_employee_data(self, event):
        """Get the selected employee's data"""
        try:
            selected = self.var_emp_id.get()
            if selected:
                emp_data = self.emp_dict[selected]
                self.var_name.set(emp_data[1])  # Set name
                self.var_qr_data.set(emp_data[0])  # Set employee ID as default QR data
            else:
                self.clear()
        except Exception as e:
            print(f"Error getting employee data: {str(e)}")
    
    def generate_qr(self):
        """Generate QR code for the employee"""
        if not self.var_qr_data.get():
            messagebox.showerror("Error", "QR Code data cannot be empty", parent=self.root)
            return
        
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            
            # Add data to the QR code
            qr.add_data(self.var_qr_data.get())
            qr.make(fit=True)
            
            # Create an image from the QR code
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Resize the image for display
            qr_img = qr_img.resize((280, 280), Image.LANCZOS)
            
            # Convert PIL image to Tkinter format
            self.qr_img_tk = ImageTk.PhotoImage(qr_img)
            
            # Update display
            self.qr_code.config(image=self.qr_img_tk, text="")
            
            # Store QR image for saving
            self.generated_qr_img = qr_img
            
            messagebox.showinfo("Success", "QR Code generated successfully", parent=self.root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating QR code: {str(e)}", parent=self.root)
    
    def save_qr(self):
        """Save the generated QR code to a file"""
        if not hasattr(self, 'generated_qr_img'):
            messagebox.showerror("Error", "Generate a QR code first", parent=self.root)
            return
        
        try:
            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension='.png',
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=f"QR_{self.var_qr_data.get()}.png"
            )
            
            if file_path:
                # Save the QR code
                self.generated_qr_img.save(file_path)
                messagebox.showinfo("Success", f"QR Code saved as {file_path}", parent=self.root)
                
                # Open the directory
                os.startfile(os.path.dirname(file_path))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error saving QR code: {str(e)}", parent=self.root)
    
    def clear(self):
        """Clear all fields and reset QR display"""
        if self.emp_list:
            self.cmb_emp.current(0)
            self.get_employee_data(None)
        else:
            self.var_name.set("")
            self.var_qr_data.set("")
        
        # Reset QR code display
        self.qr_code.config(image="", text="No QR\nCode\nAvailable")
        
        # Remove reference to generated QR
        if hasattr(self, 'generated_qr_img'):
            del self.generated_qr_img
        if hasattr(self, 'qr_img_tk'):
            del self.qr_img_tk

if __name__ == "__main__":
    root = Tk()
    obj = QRGenerator(root)
    root.mainloop() 
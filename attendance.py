from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import cv2
from datetime import datetime, timedelta
import time
from pyzbar.pyzbar import decode
import numpy as np

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Attendance Management")
        self.root.config(bg="#f4f5f7")
        self.root.resizable(False, False)
        self.root.focus_force()
        
        # Variables
        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_date = StringVar()
        self.var_time_in = StringVar()
        self.var_time_out = StringVar()
        self.var_status = StringVar()
        self.var_search = StringVar()
        self.var_search_txt = StringVar()
        
        self.camera_active = False
        self.qr_detected = False
        self.last_scan_time = 0
        self.webcam = None
        
        # Title
        title = Label(self.root, text="Attendance Management System", 
                     font=("Helvetica", 15, "bold"), bg="#2196F3", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)
        
        # Left Frame - Camera and QR Code
        left_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        left_frame.place(x=10, y=60, width=400, height=430)
        
        left_title = Label(left_frame, text="QR Code Scanner", 
                          font=("Helvetica", 15), bg="#2196F3", fg="white")
        left_title.pack(side=TOP, fill=X)
        
        # Camera Frame
        self.camera_frame = Label(left_frame, bg="black")
        self.camera_frame.place(x=10, y=40, width=380, height=300)
        
        # Camera Controls
        btn_start_camera = Button(left_frame, text="Start Camera", command=self.start_camera,
                                 font=("Helvetica", 12), bg="#4CAF50", fg="white", cursor="hand2")
        btn_start_camera.place(x=10, y=350, width=180, height=30)
        
        btn_stop_camera = Button(left_frame, text="Stop Camera", command=self.stop_camera,
                                font=("Helvetica", 12), bg="#f44336", fg="white", cursor="hand2")
        btn_stop_camera.place(x=200, y=350, width=180, height=30)
        
        # Status Label
        self.scan_status = Label(left_frame, text="Status: Ready", 
                                font=("Helvetica", 12), bg="white")
        self.scan_status.place(x=10, y=390, width=380, height=30)
        
        # Right Frame - Attendance Details & Records
        right_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        right_frame.place(x=420, y=60, width=670, height=430)
        
        # Search Frame
        search_frame = LabelFrame(right_frame, text="Search Attendance", font=("Helvetica", 12, "bold"),
                                 bd=2, relief=RIDGE, bg="white")
        search_frame.place(x=10, y=5, width=650, height=70)
        
        # Search Options
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_search,
                                 values=("Select", "Employee ID", "Date"), 
                                 state='readonly', justify=CENTER, font=("Helvetica", 12))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)
        
        txt_search = Entry(search_frame, textvariable=self.var_search_txt,
                          font=("Helvetica", 12), bg="#f4f5f7")
        txt_search.place(x=200, y=10)
        
        btn_search = Button(search_frame, command=self.search, text="Search",
                           font=("Helvetica", 12), bg="#4CAF50", fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=110, height=30)
        
        btn_clear_search = Button(search_frame, command=self.clear_search, text="Clear",
                                 font=("Helvetica", 12), bg="#607d8b", fg="white", cursor="hand2")
        btn_clear_search.place(x=530, y=9, width=110, height=30)
        
        # Attendance Table Frame
        table_frame = Frame(right_frame, bd=3, relief=RIDGE)
        table_frame.place(x=10, y=80, width=650, height=335)
        
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)
        
        self.AttendanceTable = ttk.Treeview(table_frame,
            columns=("id", "emp_id", "name", "date", "time_in", "time_out", "hours", "status"),
            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.AttendanceTable.xview)
        scrolly.config(command=self.AttendanceTable.yview)
        
        self.AttendanceTable.heading("id", text="ID")
        self.AttendanceTable.heading("emp_id", text="Emp ID")
        self.AttendanceTable.heading("name", text="Name")
        self.AttendanceTable.heading("date", text="Date")
        self.AttendanceTable.heading("time_in", text="Time In")
        self.AttendanceTable.heading("time_out", text="Time Out")
        self.AttendanceTable.heading("hours", text="Hours")
        self.AttendanceTable.heading("status", text="Status")
        
        self.AttendanceTable["show"] = "headings"
        
        self.AttendanceTable.column("id", width=50)
        self.AttendanceTable.column("emp_id", width=100)
        self.AttendanceTable.column("name", width=150)
        self.AttendanceTable.column("date", width=100)
        self.AttendanceTable.column("time_in", width=100)
        self.AttendanceTable.column("time_out", width=100)
        self.AttendanceTable.column("hours", width=100)
        self.AttendanceTable.column("status", width=100)
        
        self.AttendanceTable.pack(fill=BOTH, expand=1)
        self.AttendanceTable.bind("<ButtonRelease-1>", self.get_data)
        
        # Load attendance data
        self.show()
        
    def start_camera(self):
        """Start webcam for QR code scanning"""
        if not self.camera_active:
            try:
                self.webcam = cv2.VideoCapture(0)
                self.camera_active = True
                self.scan_status.config(text="Status: Camera Active - Ready to Scan")
                self.update_camera_feed()
            except Exception as e:
                messagebox.showerror("Error", f"Could not start camera: {str(e)}", parent=self.root)
    
    def stop_camera(self):
        """Stop the webcam"""
        if self.camera_active:
            self.camera_active = False
            if self.webcam:
                self.webcam.release()
                self.webcam = None
            self.camera_frame.config(image="")
            self.scan_status.config(text="Status: Camera Stopped")
    
    def update_camera_feed(self):
        """Update the camera feed and detect QR codes"""
        if self.camera_active and self.webcam:
            ret, frame = self.webcam.read()
            if ret:
                # Process the frame for QR code detection
                detected_codes = self.detect_qr(frame)
                
                # Convert the OpenCV frame to Tkinter format
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update the camera frame
                self.camera_frame.imgtk = imgtk
                self.camera_frame.config(image=imgtk)
            
            # Schedule the next update
            self.root.after(10, self.update_camera_feed)
    
    def detect_qr(self, frame):
        """Detect QR codes in the camera frame"""
        try:
            # Try to decode QR codes from the frame
            decoded_objects = decode(frame)
            
            # Current time to prevent multiple scans
            current_time = time.time()
            
            for obj in decoded_objects:
                # Draw rectangle around QR code
                points = obj.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                    cv2.polylines(frame, [hull], True, (0, 255, 0), 3)
                else:
                    pts = np.array([point for point in points], dtype=np.int32)
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
                
                # Get QR code data
                qr_data = obj.data.decode('utf-8')
                
                # Check if enough time has passed since last scan (3 seconds)
                if current_time - self.last_scan_time > 3:
                    self.scan_status.config(text=f"QR Code Detected: {qr_data}")
                    self.process_attendance(qr_data)
                    self.last_scan_time = current_time
            
            return decoded_objects
        
        except Exception as e:
            print(f"QR detection error: {str(e)}")
            return []
    
    def process_attendance(self, qr_data):
        """Process the scanned QR code for attendance"""
        try:
            # QR code should contain employee ID
            emp_id = qr_data
            
            # Get current date and time
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Check if employee exists
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            
            cur.execute("SELECT * FROM employee WHERE eid=?", (emp_id,))
            emp = cur.fetchone()
            
            if emp:
                # Check if already checked in today
                cur.execute("SELECT * FROM attendance WHERE emp_id=? AND date=? AND time_out IS NULL", 
                           (emp_id, current_date))
                attendance_record = cur.fetchone()
                
                if attendance_record:
                    # Employee already checked in, so this is a check-out
                    att_id = attendance_record[0]
                    time_in = attendance_record[3]
                    
                    # Calculate hours worked
                    time_in_obj = datetime.strptime(time_in, '%H:%M:%S')
                    time_out_obj = datetime.strptime(current_time, '%H:%M:%S')
                    time_diff = time_out_obj - time_in_obj
                    hours_worked = round(time_diff.total_seconds() / 3600, 2)  # Convert to hours
                    
                    # Update attendance record with check-out time
                    cur.execute("UPDATE attendance SET time_out=?, hours_worked=? WHERE id=?", 
                               (current_time, hours_worked, att_id))
                    con.commit()
                    messagebox.showinfo("Success", f"Check-out recorded for {emp[1]}", parent=self.root)
                    self.scan_status.config(text=f"Check-out: {emp[1]} at {current_time}")
                else:
                    # New check-in
                    cur.execute("INSERT INTO attendance (emp_id, date, time_in, status) VALUES (?, ?, ?, ?)",
                               (emp_id, current_date, current_time, "Present"))
                    con.commit()
                    messagebox.showinfo("Success", f"Check-in recorded for {emp[1]}", parent=self.root)
                    self.scan_status.config(text=f"Check-in: {emp[1]} at {current_time}")
                
                self.show()  # Refresh attendance table
            else:
                messagebox.showerror("Error", "Employee not found!", parent=self.root)
                self.scan_status.config(text="Error: Employee not found")
                
            con.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing attendance: {str(e)}", parent=self.root)
    
    def show(self):
        """Display attendance records in the table"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Clear existing items
            self.AttendanceTable.delete(*self.AttendanceTable.get_children())
            
            # Get attendance records with employee names
            cur.execute("""SELECT a.id, a.emp_id, e.name, a.date, a.time_in, a.time_out, 
                        a.hours_worked, a.status FROM attendance a 
                        LEFT JOIN employee e ON a.emp_id = e.eid 
                        ORDER BY a.date DESC, a.time_in DESC""")
            rows = cur.fetchall()
            
            for row in rows:
                self.AttendanceTable.insert('', END, values=row)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching attendance: {str(e)}", parent=self.root)
        
        con.close()
    
    def get_data(self, ev):
        """Get data from selected row"""
        f = self.AttendanceTable.focus()
        content = self.AttendanceTable.item(f)
        row = content['values']
        if row:
            self.var_emp_id.set(row[1])
            self.var_name.set(row[2])
            self.var_date.set(row[3])
            self.var_time_in.set(row[4])
            self.var_time_out.set(row[5] if row[5] else "")
            self.var_status.set(row[7])
    
    def clear_search(self):
        """Clear search fields and refresh table"""
        self.var_search.set("Select")
        self.var_search_txt.set("")
        self.show()
    
    def search(self):
        """Search attendance records"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "Select":
                messagebox.showerror("Error", "Select search criteria", parent=self.root)
            else:
                # Clear existing items
                self.AttendanceTable.delete(*self.AttendanceTable.get_children())
                
                search_column = "a.emp_id" if self.var_search.get() == "Employee ID" else "a.date"
                
                # Get attendance records with employee names based on search
                cur.execute(f"""SELECT a.id, a.emp_id, e.name, a.date, a.time_in, a.time_out, 
                            a.hours_worked, a.status FROM attendance a 
                            LEFT JOIN employee e ON a.emp_id = e.eid 
                            WHERE {search_column} LIKE ?
                            ORDER BY a.date DESC, a.time_in DESC""", 
                            (f"%{self.var_search_txt.get()}%",))
                rows = cur.fetchall()
                
                if rows:
                    for row in rows:
                        self.AttendanceTable.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found", parent=self.root)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error searching attendance: {str(e)}", parent=self.root)
        
        con.close()
    
    def calculate_salary(self, emp_id, month, year):
        """Calculate salary based on attendance for a specific month"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Get employee base salary
            cur.execute("SELECT salary FROM employee WHERE eid=?", (emp_id,))
            salary_data = cur.fetchone()
            
            if not salary_data:
                return 0
            
            try:
                base_salary = float(salary_data[0])
            except:
                base_salary = 0
            
            # Get total hours worked in the month
            start_date = f"{year}-{month:02d}-01"
            
            # Get last day of month
            if month == 12:
                next_month = 1
                next_year = year + 1
            else:
                next_month = month + 1
                next_year = year
                
            end_date = f"{next_year}-{next_month:02d}-01"
            
            cur.execute("""SELECT SUM(hours_worked) FROM attendance 
                        WHERE emp_id=? AND date >= ? AND date < ?""", 
                       (emp_id, start_date, end_date))
            
            total_hours = cur.fetchone()[0]
            if not total_hours:
                total_hours = 0
            
            # Calculate daily rate (assuming 22 working days in a month and 8 hours per day)
            daily_rate = base_salary / 22
            hourly_rate = daily_rate / 8
            
            # Calculate salary based on hours worked
            calculated_salary = total_hours * hourly_rate
            
            return calculated_salary
            
        except Exception as e:
            print(f"Error calculating salary: {str(e)}")
            return 0
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = AttendanceSystem(root)
    root.mainloop() 
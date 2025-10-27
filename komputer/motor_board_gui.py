import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import threading
import time

class MotorBoardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor Board Testing GUI")
        self.root.geometry("900x700")
        
        self.serial_conn = None
        self.is_running = False
        self.recv_buffer = ""
        self.read_thread = None
        self.current_voltage = 0.0
        
        # Motor configuration
        self.UPLOAD_DATA = tk.IntVar(value=3)
        self.MOTOR_TYPE = tk.IntVar(value=1)
        
        self.setup_ui()
        self.refresh_ports()
        
    def setup_ui(self):
        # Serial Port Frame
        port_frame = ttk.LabelFrame(self.root, text="Serial Port Configuration", padding=10)
        port_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        ttk.Label(port_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5)
        self.port_combo = ttk.Combobox(port_frame, width=30, state="readonly")
        self.port_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(port_frame, text="Refresh", command=self.refresh_ports).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(port_frame, text="Baudrate:").grid(row=1, column=0, padx=5, pady=5)
        self.baudrate_combo = ttk.Combobox(port_frame, width=30, values=["9600", "115200", "230400"], state="readonly")
        self.baudrate_combo.set("115200")
        self.baudrate_combo.grid(row=1, column=1, padx=5, pady=5)
        
        self.connect_btn = ttk.Button(port_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=1, column=2, padx=5, pady=5)
        
        self.status_label = ttk.Label(port_frame, text="Status: Disconnected", foreground="red")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")
        
        self.voltage_label = ttk.Label(port_frame, text="Voltage: -- V", foreground="blue", font=("Arial", 10, "bold"))
        self.voltage_label.grid(row=2, column=2, pady=5, sticky="e")
        
        # Motor Configuration Frame
        config_frame = ttk.LabelFrame(self.root, text="Motor Configuration", padding=10)
        config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(config_frame, text="Upload Data Mode:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        upload_modes = [
            ("No Data (0)", 0),
            ("Total Encoder (1)", 1),
            ("Real-time Encoder (2)", 2),
            ("Motor Speed mm/s (3)", 3)
        ]
        for i, (text, value) in enumerate(upload_modes):
            ttk.Radiobutton(config_frame, text=text, variable=self.UPLOAD_DATA, value=value).grid(row=i+1, column=0, padx=20, pady=2, sticky="w")
        
        ttk.Label(config_frame, text="Motor Type:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        motor_types = [
            ("520 Motor", 1),
            ("310 Motor", 2),
            ("Speed Code Disc TT", 3),
            ("TT DC Reduction", 4),
            ("L-type 520", 5)
        ]
        for i, (text, value) in enumerate(motor_types):
            ttk.Radiobutton(config_frame, text=text, variable=self.MOTOR_TYPE, value=value).grid(row=i+6, column=0, padx=20, pady=2, sticky="w")
        
        ttk.Button(config_frame, text="Apply Configuration", command=self.apply_configuration).grid(row=11, column=0, padx=5, pady=10)
        
        # Motor Control Frame
        control_frame = ttk.LabelFrame(self.root, text="Motor Control", padding=10)
        control_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Speed/PWM controls
        self.motor_vars = []
        for i in range(4):
            ttk.Label(control_frame, text=f"Motor {i+1}:").grid(row=i, column=0, padx=5, pady=5)
            var = tk.IntVar(value=0)
            self.motor_vars.append(var)
            scale = ttk.Scale(control_frame, from_=-2000, to=2000, orient="horizontal", variable=var, length=200)
            scale.grid(row=i, column=1, padx=5, pady=5)
            entry = ttk.Entry(control_frame, textvariable=var, width=10)
            entry.grid(row=i, column=2, padx=5, pady=5)
        
        # Control buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        ttk.Button(btn_frame, text="Send Speed", command=self.send_speed).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Send PWM", command=self.send_pwm).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Stop All", command=self.stop_motors).grid(row=0, column=2, padx=5)
        
        # Auto test frame
        auto_frame = ttk.LabelFrame(control_frame, text="Auto Test", padding=5)
        auto_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")
        
        self.auto_running = False
        self.auto_btn = ttk.Button(auto_frame, text="Start Auto Test", command=self.toggle_auto_test)
        self.auto_btn.pack(pady=5)
        
        # Data Display Frame
        data_frame = ttk.LabelFrame(self.root, text="Received Data", padding=10)
        data_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        self.data_text = scrolledtext.ScrolledText(data_frame, width=100, height=15, state='disabled')
        self.data_text.pack(fill='both', expand=True)
        
        ttk.Button(data_frame, text="Clear", command=self.clear_data).pack(pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        
        # Set minimum window size
        self.root.minsize(900, 700)
        
        # Make frames expandable
        port_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        
    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [f"{port.device} - {port.description}" for port in ports]
        self.port_combo['values'] = port_list
        if port_list:
            self.port_combo.current(0)
    
    def toggle_connection(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.disconnect()
        else:
            self.connect()
    
    def connect(self):
        try:
            port_info = self.port_combo.get()
            if not port_info:
                messagebox.showerror("Error", "Please select a port")
                return
            
            port = port_info.split(" - ")[0]
            baudrate = int(self.baudrate_combo.get())
            
            self.serial_conn = serial.Serial(port, baudrate, timeout=0.1)
            self.is_running = True
            
            # Start reading thread
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
            
            self.status_label.config(text=f"Status: Connected to {port}", foreground="green")
            self.connect_btn.config(text="Disconnect")
            
            self.log_data(f"Connected to {port} at {baudrate} baud\n")
            
            # Start periodic voltage request
            threading.Thread(target=self.request_voltage_periodically, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    
    def disconnect(self):
        self.is_running = False
        if self.auto_running:
            self.toggle_auto_test()
        
        if self.serial_conn and self.serial_conn.is_open:
            self.stop_motors()
            time.sleep(0.1)
            self.serial_conn.close()
        
        self.status_label.config(text="Status: Disconnected", foreground="red")
        self.connect_btn.config(text="Connect")
        self.voltage_label.config(text="Voltage: -- V", foreground="blue")
        self.log_data("Disconnected\n")
    
    def send_data(self, data):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(data.encode())
                time.sleep(0.01)
                return True
            except Exception as e:
                self.log_data(f"Send error: {str(e)}\n")
                return False
        else:
            messagebox.showwarning("Warning", "Not connected to serial port")
            return False
    
    def read_serial(self):
        while self.is_running:
            try:
                if self.serial_conn and self.serial_conn.in_waiting > 0:
                    data = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
                    self.recv_buffer += data
                    
                    messages = self.recv_buffer.split("#")
                    self.recv_buffer = messages[-1]
                    
                    for msg in messages[:-1]:
                        if msg:
                            parsed = self.parse_data(msg + "#")
                            if parsed:
                                self.log_data(parsed + "\n")
                
                time.sleep(0.01)
            except Exception as e:
                self.log_data(f"Read error: {str(e)}\n")
                time.sleep(0.1)
    
    def parse_data(self, data):
        data = data.strip()
        
        if data.startswith("$MAll:"):
            values_str = data[6:-1]
            values = list(map(int, values_str.split(',')))
            return "Total Encoder - " + ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        elif data.startswith("$MTEP:"):
            values_str = data[6:-1]
            values = list(map(int, values_str.split(',')))
            return "Real-time Encoder - " + ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        elif data.startswith("$MSPD:"):
            values_str = data[6:-1]
            values = [float(value) if '.' in value else int(value) for value in values_str.split(',')]
            return "Motor Speed (mm/s) - " + ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        elif data.startswith("$Battery:") or data.startswith("$battery:"):
            # Parse voltage data: $Battery:7.40V#
            try:
                voltage_str = data.split(':')[1].replace('V', '').replace('#', '').strip()
                self.current_voltage = float(voltage_str)
                self.update_voltage_display()
                return f"Battery Voltage: {self.current_voltage:.2f} V"
            except (ValueError, IndexError):
                return None
        return None
    
    def log_data(self, text):
        self.data_text.config(state='normal')
        self.data_text.insert(tk.END, text)
        self.data_text.see(tk.END)
        self.data_text.config(state='disabled')
    
    def update_voltage_display(self):
        """Update voltage label in GUI thread-safe way"""
        try:
            voltage_text = f"Voltage: {self.current_voltage:.2f} V"
            # Color coding based on voltage level
            if self.current_voltage >= 11.0:
                color = "green"
            elif self.current_voltage >= 10.5:
                color = "orange"
            else:
                color = "red"
            
            self.voltage_label.config(text=voltage_text, foreground=color)
        except:
            pass
    
    def clear_data(self):
        self.data_text.config(state='normal')
        self.data_text.delete(1.0, tk.END)
        self.data_text.config(state='disabled')
    
    def apply_configuration(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            messagebox.showwarning("Warning", "Please connect to serial port first")
            return
        
        # Send upload mode
        mode = self.UPLOAD_DATA.get()
        if mode == 0:
            self.send_data("$upload:0,0,0#")
        elif mode == 1:
            self.send_data("$upload:1,0,0#")
        elif mode == 2:
            self.send_data("$upload:0,1,0#")
        elif mode == 3:
            self.send_data("$upload:0,0,1#")
        time.sleep(0.1)
        
        # Request voltage reading
        self.send_data("$read_vol#")
        time.sleep(0.1)
        
        # Configure motor parameters based on type
        motor_type = self.MOTOR_TYPE.get()
        self.set_motor_parameters(motor_type)
        
        self.log_data(f"Configuration applied: Upload Mode={mode}, Motor Type={motor_type}\n")
        messagebox.showinfo("Success", "Configuration applied successfully")
    
    def set_motor_parameters(self, motor_type):
        if motor_type == 1:  # 520 motor
            self.send_data("$mtype:1#")
            time.sleep(0.1)
            self.send_data("$mphase:30#")
            time.sleep(0.1)
            self.send_data("$mline:11#")
            time.sleep(0.1)
            self.send_data("$wdiameter:67.00#")
            time.sleep(0.1)
            self.send_data("$deadzone:1600#")
            time.sleep(0.1)
        elif motor_type == 2:  # 310 motor
            self.send_data("$mtype:2#")
            time.sleep(0.1)
            self.send_data("$mphase:20#")
            time.sleep(0.1)
            self.send_data("$mline:13#")
            time.sleep(0.1)
            self.send_data("$wdiameter:48.00#")
            time.sleep(0.1)
            self.send_data("$deadzone:1300#")
            time.sleep(0.1)
        elif motor_type == 3:  # Speed code disc TT
            self.send_data("$mtype:3#")
            time.sleep(0.1)
            self.send_data("$mphase:45#")
            time.sleep(0.1)
            self.send_data("$mline:13#")
            time.sleep(0.1)
            self.send_data("$wdiameter:68.00#")
            time.sleep(0.1)
            self.send_data("$deadzone:1250#")
            time.sleep(0.1)
        elif motor_type == 4:  # TT DC reduction
            self.send_data("$mtype:4#")
            time.sleep(0.1)
            self.send_data("$mphase:48#")
            time.sleep(0.1)
            self.send_data("$deadzone:1000#")
            time.sleep(0.1)
        elif motor_type == 5:  # L-type 520
            self.send_data("$mtype:1#")
            time.sleep(0.1)
            self.send_data("$mphase:40#")
            time.sleep(0.1)
            self.send_data("$mline:11#")
            time.sleep(0.1)
            self.send_data("$wdiameter:67.00#")
            time.sleep(0.1)
            self.send_data("$deadzone:1600#")
            time.sleep(0.1)
    
    def send_speed(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            messagebox.showwarning("Warning", "Please connect to serial port first")
            return
        
        m1, m2, m3, m4 = [var.get() for var in self.motor_vars]
        cmd = f"$spd:{m1},{m2},{m3},{m4}#"
        self.send_data(cmd)
        self.log_data(f"Sent: {cmd}\n")
    
    def send_pwm(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            messagebox.showwarning("Warning", "Please connect to serial port first")
            return
        
        m1, m2, m3, m4 = [var.get() for var in self.motor_vars]
        cmd = f"$pwm:{m1},{m2},{m3},{m4}#"
        self.send_data(cmd)
        self.log_data(f"Sent: {cmd}\n")
    
    def stop_motors(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.send_data("$pwm:0,0,0,0#")
            for var in self.motor_vars:
                var.set(0)
            self.log_data("Motors stopped\n")
    
    def toggle_auto_test(self):
        if self.auto_running:
            self.auto_running = False
            self.auto_btn.config(text="Start Auto Test")
        else:
            if not self.serial_conn or not self.serial_conn.is_open:
                messagebox.showwarning("Warning", "Please connect to serial port first")
                return
            self.auto_running = True
            self.auto_btn.config(text="Stop Auto Test")
            threading.Thread(target=self.run_auto_test, daemon=True).start()
    
    def run_auto_test(self):
        t = 0
        motor_type = self.MOTOR_TYPE.get()
        
        while self.auto_running:
            t += 10
            
            if motor_type == 4:
                self.send_data(f"$pwm:{t*2},{t*2},{t*2},{t*2}#")
            else:
                self.send_data(f"$spd:{t},{t},{t},{t}#")
            
            # Update GUI
            for var in self.motor_vars:
                var.set(t)
            
            if t > 1000 or t < -1000:
                t = 0
            
            time.sleep(0.1)
    
    def request_voltage_periodically(self):
        """Request voltage data every 2 seconds"""
        while self.is_running:
            if self.serial_conn and self.serial_conn.is_open:
                self.send_data("$read_vol#")
            time.sleep(2.0)
    
    def on_closing(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorBoardGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

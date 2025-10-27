import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import serial.tools.list_ports
import threading
import time

class MotorBoardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor Board Testing GUI - Full Configuration")
        self.root.geometry("1200x800")
        
        # Set minimum window size to prevent content from being hidden
        self.root.minsize(1100, 750)
        
        self.serial_conn = None
        self.is_running = False
        self.recv_buffer = ""
        self.read_thread = None
        
        # Motor configuration variables
        self.UPLOAD_DATA = tk.IntVar(value=3)
        self.MOTOR_TYPE = tk.IntVar(value=1)
        
        # Battery monitoring
        self.battery_monitoring = False
        self.battery_timer = None
        
        self.setup_ui()
        self.refresh_ports()
        
    def setup_ui(self):
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_connection_tab()
        self.create_configuration_tab()
        self.create_control_tab()
        self.create_monitor_tab()
        
    def create_connection_tab(self):
        conn_tab = ttk.Frame(self.notebook)
        self.notebook.add(conn_tab, text="Connection")
        
        # Serial Port Frame
        port_frame = ttk.LabelFrame(conn_tab, text="Serial Port Configuration", padding=20)
        port_frame.pack(padx=20, pady=20, fill='x')
        
        ttk.Label(port_frame, text="Port:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=10, sticky='e')
        self.port_combo = ttk.Combobox(port_frame, width=40, state="readonly", font=('Arial', 10))
        self.port_combo.grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Button(port_frame, text="Refresh Ports", command=self.refresh_ports).grid(row=0, column=2, padx=5, pady=10)
        
        ttk.Label(port_frame, text="Baudrate:", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=10, sticky='e')
        self.baudrate_combo = ttk.Combobox(port_frame, width=40, values=["9600", "57600", "115200", "230400"], state="readonly", font=('Arial', 10))
        self.baudrate_combo.set("115200")
        self.baudrate_combo.grid(row=1, column=1, padx=5, pady=10)
        
        self.connect_btn = ttk.Button(port_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=1, column=2, padx=5, pady=10)
        
        self.status_label = ttk.Label(port_frame, text="Status: Disconnected", foreground="red", font=('Arial', 12, 'bold'))
        self.status_label.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Upload Data Mode Frame
        upload_frame = ttk.LabelFrame(conn_tab, text="Upload Data Mode", padding=20)
        upload_frame.pack(padx=20, pady=20, fill='x')
        
        upload_modes = [
            ("0: No data upload", 0),
            ("1: Report total encoder data", 1),
            ("2: Report real-time encoder data", 2),
            ("3: Report current motor speed (mm/s)", 3)
        ]
        for i, (text, value) in enumerate(upload_modes):
            ttk.Radiobutton(upload_frame, text=text, variable=self.UPLOAD_DATA, value=value).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        
        ttk.Button(upload_frame, text="Apply Upload Mode", command=self.apply_upload_mode).grid(row=4, column=0, padx=10, pady=10)
        
    def create_configuration_tab(self):
        config_tab = ttk.Frame(self.notebook)
        self.notebook.add(config_tab, text="Configuration")
        
        # Create scrollable frame
        canvas = tk.Canvas(config_tab)
        scrollbar = ttk.Scrollbar(config_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 1. Motor Type Configuration
        type_frame = ttk.LabelFrame(scrollable_frame, text="1. Configure Motor Type", padding=15)
        type_frame.pack(padx=10, pady=10, fill='x')
        
        motor_types = [
            ("1: 520 Motor", 1),
            ("2: 310 Motor", 2),
            ("3: Speed Code Disc TT Motor", 3),
            ("4: TT DC Reduction Motor", 4),
            ("5: L-type 520 Motor", 5)
        ]
        for i, (text, value) in enumerate(motor_types):
            ttk.Radiobutton(type_frame, text=text, variable=self.MOTOR_TYPE, value=value).grid(row=i, column=0, padx=10, pady=3, sticky='w')
        
        ttk.Button(type_frame, text="Set Motor Type", command=self.set_motor_type).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(type_frame, text="Apply Preset Configuration", command=self.apply_preset_configuration).grid(row=5, column=1, padx=10, pady=10)
        
        # 2. Deadzone Configuration
        deadzone_frame = ttk.LabelFrame(scrollable_frame, text="2. Configure Motor Deadband (Dead Zone)", padding=15)
        deadzone_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(deadzone_frame, text="Dead Zone Value (0-4095):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.deadzone_var = tk.IntVar(value=1600)
        ttk.Entry(deadzone_frame, textvariable=self.deadzone_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(deadzone_frame, text="Set Deadzone", command=self.set_deadzone).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(deadzone_frame, text="(Minimum PWM to overcome static friction)", font=('Arial', 8, 'italic')).grid(row=1, column=0, columnspan=3, padx=5, sticky='w')
        
        # 3. Phase Lines Configuration
        lines_frame = ttk.LabelFrame(scrollable_frame, text="3. Configure Motor Phase Lines (Magnetic Ring)", padding=15)
        lines_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(lines_frame, text="Phase Lines (Encoder Lines):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.lines_var = tk.IntVar(value=11)
        ttk.Entry(lines_frame, textvariable=self.lines_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(lines_frame, text="Set Phase Lines", command=self.set_phase_lines).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(lines_frame, text="(Check motor manual for encoder line count)", font=('Arial', 8, 'italic')).grid(row=1, column=0, columnspan=3, padx=5, sticky='w')
        
        # 4. Reduction Ratio Configuration
        ratio_frame = ttk.LabelFrame(scrollable_frame, text="4. Configure Motor Reduction Ratio", padding=15)
        ratio_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(ratio_frame, text="Reduction Ratio:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ratio_var = tk.IntVar(value=30)
        ttk.Entry(ratio_frame, textvariable=self.ratio_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(ratio_frame, text="Set Reduction Ratio", command=self.set_reduction_ratio).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(ratio_frame, text="(Gear reduction ratio, check motor manual)", font=('Arial', 8, 'italic')).grid(row=1, column=0, columnspan=3, padx=5, sticky='w')
        
        # 5. Wheel Diameter Configuration
        wheel_frame = ttk.LabelFrame(scrollable_frame, text="5. Configure Wheel Diameter (Optional)", padding=15)
        wheel_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(wheel_frame, text="Wheel Diameter (mm):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.wheel_var = tk.DoubleVar(value=67.0)
        ttk.Entry(wheel_frame, textvariable=self.wheel_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(wheel_frame, text="Set Wheel Diameter", command=self.set_wheel_diameter).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(wheel_frame, text="(Used for speed calculation in mm/s)", font=('Arial', 8, 'italic')).grid(row=1, column=0, columnspan=3, padx=5, sticky='w')
        
        # 6. PID Configuration
        pid_frame = ttk.LabelFrame(scrollable_frame, text="6. Configure PID Parameters", padding=15)
        pid_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(pid_frame, text="Motor:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.pid_motor_var = tk.IntVar(value=1)
        ttk.Combobox(pid_frame, textvariable=self.pid_motor_var, values=[1, 2, 3, 4], width=10, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(pid_frame, text="P:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.pid_p_var = tk.DoubleVar(value=0.0)
        ttk.Entry(pid_frame, textvariable=self.pid_p_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(pid_frame, text="I:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.pid_i_var = tk.DoubleVar(value=0.0)
        ttk.Entry(pid_frame, textvariable=self.pid_i_var, width=15).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(pid_frame, text="D:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.pid_d_var = tk.DoubleVar(value=0.0)
        ttk.Entry(pid_frame, textvariable=self.pid_d_var, width=15).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(pid_frame, text="Set PID Parameters", command=self.set_pid).grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        ttk.Label(pid_frame, text="(Fine-tune speed control response)", font=('Arial', 8, 'italic')).grid(row=5, column=0, columnspan=2, padx=5, sticky='w')
        
        # 7. Reset Configuration
        reset_frame = ttk.LabelFrame(scrollable_frame, text="7. Reset All Variables", padding=15)
        reset_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(reset_frame, text="Reset all configuration to default values", foreground="red").pack(pady=5)
        ttk.Button(reset_frame, text="Reset to Defaults", command=self.reset_defaults).pack(pady=5)
        
    def create_control_tab(self):
        control_tab = ttk.Frame(self.notebook)
        self.notebook.add(control_tab, text="Control")
        
        # 8. Speed Control
        speed_frame = ttk.LabelFrame(control_tab, text="8. Control Speed Command (mm/s)", padding=15)
        speed_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.motor_vars = []
        for i in range(4):
            motor_frame = ttk.Frame(speed_frame)
            motor_frame.pack(fill='x', padx=10, pady=5)
            
            ttk.Label(motor_frame, text=f"Motor {i+1}:", width=10).pack(side='left', padx=5)
            var = tk.IntVar(value=0)
            self.motor_vars.append(var)
            
            scale = ttk.Scale(motor_frame, from_=-2000, to=2000, orient="horizontal", variable=var, length=400)
            scale.pack(side='left', padx=5, fill='x', expand=True)
            
            entry = ttk.Entry(motor_frame, textvariable=var, width=10)
            entry.pack(side='left', padx=5)
        
        btn_frame = ttk.Frame(speed_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Send Speed Command", command=self.send_speed).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Stop All Motors", command=self.stop_motors).pack(side='left', padx=5)
        
        # 9. PWM Control
        pwm_frame = ttk.LabelFrame(control_tab, text="9. Direct Control PWM Instruction (-4095 to 4095)", padding=15)
        pwm_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.pwm_vars = []
        for i in range(4):
            motor_frame = ttk.Frame(pwm_frame)
            motor_frame.pack(fill='x', padx=10, pady=5)
            
            ttk.Label(motor_frame, text=f"Motor {i+1} PWM:", width=15).pack(side='left', padx=5)
            var = tk.IntVar(value=0)
            self.pwm_vars.append(var)
            
            scale = ttk.Scale(motor_frame, from_=-4095, to=4095, orient="horizontal", variable=var, length=400)
            scale.pack(side='left', padx=5, fill='x', expand=True)
            
            entry = ttk.Entry(motor_frame, textvariable=var, width=10)
            entry.pack(side='left', padx=5)
        
        btn_frame2 = ttk.Frame(pwm_frame)
        btn_frame2.pack(pady=10)
        
        ttk.Button(btn_frame2, text="Send PWM Command", command=self.send_pwm).pack(side='left', padx=5)
        ttk.Button(btn_frame2, text="Stop All Motors (PWM)", command=self.stop_motors_pwm).pack(side='left', padx=5)
        
        # Auto Test
        auto_frame = ttk.LabelFrame(control_tab, text="Auto Test Mode", padding=15)
        auto_frame.pack(padx=10, pady=10, fill='x')
        
        self.auto_running = False
        self.auto_btn = ttk.Button(auto_frame, text="Start Auto Test", command=self.toggle_auto_test)
        self.auto_btn.pack(pady=10)
        
    def create_monitor_tab(self):
        monitor_tab = ttk.Frame(self.notebook)
        self.notebook.add(monitor_tab, text="Monitor & Query")
        
        # 10. Encoder Data
        encoder_frame = ttk.LabelFrame(monitor_tab, text="10. Report Encoder Data", padding=15)
        encoder_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(encoder_frame, text="Request encoder data (only for motors with encoder)").pack(pady=5)
        btn_frame = ttk.Frame(encoder_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Request Total Encoder", command=lambda: self.request_encoder(1)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Request Real-time Encoder", command=lambda: self.request_encoder(2)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Request Motor Speed", command=lambda: self.request_encoder(3)).pack(side='left', padx=5)
        
        # STOP Query Button
        stop_btn = ttk.Button(encoder_frame, text="⏹ STOP Data Streaming", command=self.stop_query)
        stop_btn.pack(pady=10)
        
        # 11. Query Flash Variables
        query_frame = ttk.LabelFrame(monitor_tab, text="11. Query Flash Variables", padding=15)
        query_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(query_frame, text="Query configuration stored in flash memory").pack(pady=5)
        ttk.Button(query_frame, text="Query Flash Variables", command=self.query_flash).pack(pady=5)
        
        # 12. Battery Level with Real-time Monitor
        battery_frame = ttk.LabelFrame(monitor_tab, text="12. Battery Level Monitor", padding=15)
        battery_frame.pack(padx=10, pady=10, fill='x')
        
        # Control buttons
        btn_battery_frame = ttk.Frame(battery_frame)
        btn_battery_frame.pack(pady=5)
        ttk.Button(btn_battery_frame, text="🔋 Check Battery", command=self.check_battery).pack(side='left', padx=5)
        self.battery_monitor_btn = ttk.Button(btn_battery_frame, text="▶ Start Auto-Monitor (5s)", command=self.toggle_battery_monitor)
        self.battery_monitor_btn.pack(side='left', padx=5)
        
        # Large battery display
        self.battery_label = ttk.Label(battery_frame, text="Battery: -- V", font=('Arial', 14, 'bold'), foreground='green')
        self.battery_label.pack(pady=10)
        
        # Battery history textbox
        ttk.Label(battery_frame, text="Battery Voltage History:", font=('Arial', 9)).pack(anchor='w', padx=5)
        self.battery_history = scrolledtext.ScrolledText(battery_frame, width=80, height=5, state='disabled', bg='#2c3e50', fg='#ecf0f1')
        self.battery_history.pack(pady=5, padx=5, fill='x')
        
        # Data Display
        data_frame = ttk.LabelFrame(monitor_tab, text="Received Data Log", padding=10)
        data_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.data_text = scrolledtext.ScrolledText(data_frame, width=100, height=20, state='disabled')
        self.data_text.pack(fill='both', expand=True)
        
        ttk.Button(data_frame, text="Clear Log", command=self.clear_data).pack(pady=5)
        
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
            
            self.log_data(f"=== Connected to {port} at {baudrate} baud ===\n")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    
    def disconnect(self):
        self.is_running = False
        if self.auto_running:
            self.toggle_auto_test()
        
        # Stop battery monitoring if running
        if self.battery_monitoring:
            self.toggle_battery_monitor()
        
        if self.serial_conn and self.serial_conn.is_open:
            self.stop_motors_pwm()
            time.sleep(0.1)
            self.serial_conn.close()
        
        self.status_label.config(text="Status: Disconnected", foreground="red")
        self.connect_btn.config(text="Connect")
        self.log_data("=== Disconnected ===\n")
    
    def send_data(self, data):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(data.encode())
                time.sleep(0.01)
                self.log_data(f"TX: {data}")
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
                            full_msg = msg + "#"
                            parsed = self.parse_data(full_msg)
                            if parsed:
                                self.log_data(f"RX: {parsed}\n")
                            else:
                                self.log_data(f"RX: {full_msg}\n")
                
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
            voltage = data[9:-1]
            self.battery_label.config(text=f"Battery: {voltage}")
            
            # Add to battery history
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"[{timestamp}] {voltage}\n"
            
            self.battery_history.config(state='normal')
            self.battery_history.insert('end', history_entry)
            self.battery_history.see('end')  # Auto-scroll to bottom
            self.battery_history.config(state='disabled')
            
            # Update color based on voltage
            try:
                v = float(voltage.replace('V', '').replace('v', ''))
                if v < 6.5:
                    self.battery_label.config(foreground='red')  # Critical
                elif v < 7.0:
                    self.battery_label.config(foreground='orange')  # Low
                else:
                    self.battery_label.config(foreground='green')  # OK
            except:
                pass
            
            return f"Battery Level: {voltage}"
        return None
    
    def log_data(self, text):
        self.data_text.config(state='normal')
        self.data_text.insert(tk.END, text)
        self.data_text.see(tk.END)
        self.data_text.config(state='disabled')
    
    def clear_data(self):
        self.data_text.config(state='normal')
        self.data_text.delete(1.0, tk.END)
        self.data_text.config(state='disabled')
    
    # Configuration Commands
    def apply_upload_mode(self):
        mode = self.UPLOAD_DATA.get()
        if mode == 0:
            self.send_data("$upload:0,0,0#")
        elif mode == 1:
            self.send_data("$upload:1,0,0#")
        elif mode == 2:
            self.send_data("$upload:0,1,0#")
        elif mode == 3:
            self.send_data("$upload:0,0,1#")
    
    def set_motor_type(self):
        motor_type = self.MOTOR_TYPE.get()
        self.send_data(f"$mtype:{motor_type}#")
    
    def set_deadzone(self):
        deadzone = self.deadzone_var.get()
        self.send_data(f"$deadzone:{deadzone}#")
    
    def set_phase_lines(self):
        lines = self.lines_var.get()
        self.send_data(f"$mline:{lines}#")
    
    def set_reduction_ratio(self):
        ratio = self.ratio_var.get()
        self.send_data(f"$mphase:{ratio}#")
    
    def set_wheel_diameter(self):
        diameter = self.wheel_var.get()
        self.send_data(f"$wdiameter:{diameter:.2f}#")
    
    def set_pid(self):
        motor = self.pid_motor_var.get()
        p = self.pid_p_var.get()
        i = self.pid_i_var.get()
        d = self.pid_d_var.get()
        self.send_data(f"$pid:{motor},{p},{i},{d}#")
    
    def reset_defaults(self):
        result = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all variables to default values?")
        if result:
            self.send_data("$reset#")
            self.log_data("RESET: All variables reset to defaults\n")
    
    def apply_preset_configuration(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            messagebox.showwarning("Warning", "Please connect to serial port first")
            return
        
        motor_type = self.MOTOR_TYPE.get()
        
        self.log_data(f"\n=== Applying Preset Configuration for Motor Type {motor_type} ===\n")
        
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
            
            # Update UI values
            self.ratio_var.set(30)
            self.lines_var.set(11)
            self.wheel_var.set(67.0)
            self.deadzone_var.set(1600)
            
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
            
            self.ratio_var.set(20)
            self.lines_var.set(13)
            self.wheel_var.set(48.0)
            self.deadzone_var.set(1300)
            
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
            
            self.ratio_var.set(45)
            self.lines_var.set(13)
            self.wheel_var.set(68.0)
            self.deadzone_var.set(1250)
            
        elif motor_type == 4:  # TT DC reduction
            self.send_data("$mtype:4#")
            time.sleep(0.1)
            self.send_data("$mphase:48#")
            time.sleep(0.1)
            self.send_data("$deadzone:1000#")
            
            self.ratio_var.set(48)
            self.deadzone_var.set(1000)
            
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
            
            self.ratio_var.set(40)
            self.lines_var.set(11)
            self.wheel_var.set(67.0)
            self.deadzone_var.set(1600)
        
        time.sleep(0.1)
        messagebox.showinfo("Success", f"Preset configuration for Motor Type {motor_type} applied successfully")
    
    # Control Commands
    def send_speed(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            messagebox.showwarning("Warning", "Please connect to serial port first")
            return
        
        m1, m2, m3, m4 = [var.get() for var in self.motor_vars]
        self.send_data(f"$spd:{m1},{m2},{m3},{m4}#")
    
    def send_pwm(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            messagebox.showwarning("Warning", "Please connect to serial port first")
            return
        
        m1, m2, m3, m4 = [var.get() for var in self.pwm_vars]
        self.send_data(f"$pwm:{m1},{m2},{m3},{m4}#")
    
    def stop_motors(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.send_data("$spd:0,0,0,0#")
            for var in self.motor_vars:
                var.set(0)
    
    def stop_motors_pwm(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.send_data("$pwm:0,0,0,0#")
            for var in self.pwm_vars:
                var.set(0)
    
    # Query Commands
    def request_encoder(self, mode):
        if mode == 1:
            self.send_data("$upload:1,0,0#")
        elif mode == 2:
            self.send_data("$upload:0,1,0#")
        elif mode == 3:
            self.send_data("$upload:0,0,1#")
    
    def stop_query(self):
        """Stop all data streaming"""
        self.send_data("$upload:0,0,0#")
        self.log_data("⏹ STOP: All data streaming stopped\n")
        messagebox.showinfo("Stopped", "✅ Data streaming stopped!\n\nNo more encoder/speed data will be sent.")
    
    def query_flash(self):
        self.send_data("$query#")
        self.log_data("Query: Requesting flash variables...\n")
    
    def check_battery(self):
        self.send_data("$read_vol#")
        self.log_data("Query: Requesting battery level...\n")
    
    def toggle_battery_monitor(self):
        """Toggle auto battery monitoring"""
        if self.battery_monitoring:
            # Stop monitoring
            self.battery_monitoring = False
            if self.battery_timer:
                self.root.after_cancel(self.battery_timer)
                self.battery_timer = None
            self.battery_monitor_btn.config(text="▶ Start Auto-Monitor (5s)")
            self.log_data("⏹ Battery auto-monitor stopped\n")
        else:
            # Start monitoring
            if not self.serial_conn or not self.serial_conn.is_open:
                messagebox.showwarning("Warning", "⚠️ Please connect to serial port first!")
                return
            
            self.battery_monitoring = True
            self.battery_monitor_btn.config(text="⏹ Stop Auto-Monitor")
            self.log_data("▶ Battery auto-monitor started (checking every 5 seconds)\n")
            # Check immediately then schedule
            self.auto_check_battery()
    
    def auto_check_battery(self):
        """Auto check battery - called by timer"""
        if self.serial_conn and self.serial_conn.is_open and self.battery_monitoring:
            self.send_data("$read_vol#")
            # Schedule next check
            self.battery_timer = self.root.after(5000, self.auto_check_battery)
    
    # Auto Test
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
        
        self.log_data("\n=== Auto Test Started ===\n")
        
        while self.auto_running:
            t += 10
            
            if motor_type == 4:
                self.send_data(f"$pwm:{t*2},{t*2},{t*2},{t*2}#")
            else:
                self.send_data(f"$spd:{t},{t},{t},{t}#")
            
            # Update GUI
            for var in self.motor_vars:
                var.set(t)
            
            if t >= 1000:
                t = 0
            
            time.sleep(0.1)
        
        self.log_data("=== Auto Test Stopped ===\n")
    
    def on_closing(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorBoardGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

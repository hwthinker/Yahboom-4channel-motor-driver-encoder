"""
Motor Board Testing GUI - PyQt5 Version
Modern, professional interface with complete 12 configuration options
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QLabel, QComboBox, 
                             QPushButton, QLineEdit, QSlider, QTextEdit,
                             QGroupBox, QRadioButton, QButtonGroup, QSpinBox,
                             QDoubleSpinBox, QMessageBox, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
import serial
import serial.tools.list_ports
import time

class SerialReaderThread(QThread):
    """Thread untuk membaca data serial tanpa freeze GUI"""
    data_received = pyqtSignal(str)
    
    def __init__(self, serial_conn):
        super().__init__()
        self.serial_conn = serial_conn
        self.running = True
        self.recv_buffer = ""
        
    def run(self):
        while self.running:
            try:
                if self.serial_conn and self.serial_conn.is_open and self.serial_conn.in_waiting > 0:
                    data = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
                    self.recv_buffer += data
                    
                    messages = self.recv_buffer.split("#")
                    self.recv_buffer = messages[-1]
                    
                    for msg in messages[:-1]:
                        if msg:
                            self.data_received.emit(msg + "#")
                
                time.sleep(0.01)
            except Exception as e:
                self.data_received.emit(f"ERROR: {str(e)}")
                time.sleep(0.1)
    
    def stop(self):
        self.running = False

class MotorBoardGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motor Board Testing GUI - Professional Edition")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set minimum size to prevent content from being hidden
        self.setMinimumSize(1200, 800)
        
        # Variables
        self.serial_conn = None
        self.reader_thread = None
        self.motor_type = 1
        self.upload_mode = 3
        
        # Setup UI
        self.setup_ui()
        self.apply_modern_style()
        self.refresh_ports()
        
    def setup_ui(self):
        """Setup main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel("🚀 Motor Board Testing & Configuration System")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", 10))
        
        # Create tabs
        self.create_connection_tab()
        self.create_configuration_tab()
        self.create_control_tab()
        self.create_monitor_tab()
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready - Please connect to serial port")
        self.statusBar().setFont(QFont("Arial", 9))
        
    def create_connection_tab(self):
        """Tab 1: Connection"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Serial Port Group
        port_group = QGroupBox("Serial Port Configuration")
        port_group.setFont(QFont("Arial", 11, QFont.Bold))
        port_layout = QVBoxLayout()
        
        # Port selection
        port_row = QHBoxLayout()
        port_row.addWidget(QLabel("Port:"))
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(300)
        port_row.addWidget(self.port_combo)
        
        self.refresh_btn = QPushButton("🔄 Refresh Ports")
        self.refresh_btn.clicked.connect(self.refresh_ports)
        port_row.addWidget(self.refresh_btn)
        port_row.addStretch()
        port_layout.addLayout(port_row)
        
        # Baudrate selection
        baud_row = QHBoxLayout()
        baud_row.addWidget(QLabel("Baudrate:"))
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "57600", "115200", "230400"])
        self.baud_combo.setCurrentText("115200")
        self.baud_combo.setMinimumWidth(300)
        baud_row.addWidget(self.baud_combo)
        
        self.connect_btn = QPushButton("🔌 Connect")
        self.connect_btn.setMinimumHeight(35)
        self.connect_btn.clicked.connect(self.toggle_connection)
        baud_row.addWidget(self.connect_btn)
        baud_row.addStretch()
        port_layout.addLayout(baud_row)
        
        # Status
        self.status_label = QLabel("● Status: Disconnected")
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.status_label.setStyleSheet("color: #e74c3c;")
        port_layout.addWidget(self.status_label)
        
        port_group.setLayout(port_layout)
        layout.addWidget(port_group)
        
        # Upload Data Mode Group
        upload_group = QGroupBox("Upload Data Mode")
        upload_group.setFont(QFont("Arial", 11, QFont.Bold))
        upload_layout = QVBoxLayout()
        
        self.upload_btn_group = QButtonGroup()
        upload_modes = [
            ("0: No data upload", 0),
            ("1: Report total encoder data", 1),
            ("2: Report real-time encoder data", 2),
            ("3: Report current motor speed (mm/s)", 3)
        ]
        
        for text, value in upload_modes:
            rb = QRadioButton(text)
            rb.setFont(QFont("Arial", 10))
            if value == 3:
                rb.setChecked(True)
            self.upload_btn_group.addButton(rb, value)
            upload_layout.addWidget(rb)
        
        apply_upload_btn = QPushButton("✅ Apply Upload Mode")
        apply_upload_btn.setMinimumHeight(35)
        apply_upload_btn.clicked.connect(self.apply_upload_mode)
        upload_layout.addWidget(apply_upload_btn)
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        layout.addStretch()
        self.tabs.addTab(tab, "🔌 Connection")
        
    def create_configuration_tab(self):
        """Tab 2: Configuration"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # 1. Motor Type
        type_group = QGroupBox("1️⃣ Configure Motor Type")
        type_group.setFont(QFont("Arial", 11, QFont.Bold))
        type_layout = QVBoxLayout()
        
        self.motor_type_group = QButtonGroup()
        motor_types = [
            ("520 Motor", 1),
            ("310 Motor", 2),
            ("Speed Code Disc TT Motor", 3),
            ("TT DC Reduction Motor", 4),
            ("L-type 520 Motor", 5)
        ]
        
        for text, value in motor_types:
            rb = QRadioButton(f"{value}: {text}")
            rb.setFont(QFont("Arial", 10))
            if value == 1:
                rb.setChecked(True)
            self.motor_type_group.addButton(rb, value)
            type_layout.addWidget(rb)
        
        btn_row = QHBoxLayout()
        set_type_btn = QPushButton("Set Motor Type")
        set_type_btn.clicked.connect(self.set_motor_type)
        btn_row.addWidget(set_type_btn)
        
        preset_btn = QPushButton("⚡ Apply Preset Configuration")
        preset_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        preset_btn.clicked.connect(self.apply_preset_configuration)
        btn_row.addWidget(preset_btn)
        type_layout.addLayout(btn_row)
        
        type_group.setLayout(type_layout)
        scroll_layout.addWidget(type_group)
        
        # 2. Deadzone
        deadzone_group = QGroupBox("2️⃣ Configure Motor Deadband (Dead Zone)")
        deadzone_group.setFont(QFont("Arial", 11, QFont.Bold))
        deadzone_layout = QHBoxLayout()
        deadzone_layout.addWidget(QLabel("Dead Zone Value (0-4095):"))
        self.deadzone_spin = QSpinBox()
        self.deadzone_spin.setRange(0, 4095)
        self.deadzone_spin.setValue(1600)
        self.deadzone_spin.setMinimumWidth(100)
        deadzone_layout.addWidget(self.deadzone_spin)
        set_dz_btn = QPushButton("Set Deadzone")
        set_dz_btn.clicked.connect(self.set_deadzone)
        deadzone_layout.addWidget(set_dz_btn)
        deadzone_layout.addStretch()
        deadzone_group.setLayout(deadzone_layout)
        scroll_layout.addWidget(deadzone_group)
        
        # 3. Phase Lines
        lines_group = QGroupBox("3️⃣ Configure Motor Phase Lines")
        lines_group.setFont(QFont("Arial", 11, QFont.Bold))
        lines_layout = QHBoxLayout()
        lines_layout.addWidget(QLabel("Phase Lines (Encoder Lines):"))
        self.lines_spin = QSpinBox()
        self.lines_spin.setRange(1, 100)
        self.lines_spin.setValue(11)
        self.lines_spin.setMinimumWidth(100)
        lines_layout.addWidget(self.lines_spin)
        set_lines_btn = QPushButton("Set Phase Lines")
        set_lines_btn.clicked.connect(self.set_phase_lines)
        lines_layout.addWidget(set_lines_btn)
        lines_layout.addStretch()
        lines_group.setLayout(lines_layout)
        scroll_layout.addWidget(lines_group)
        
        # 4. Reduction Ratio
        ratio_group = QGroupBox("4️⃣ Configure Motor Reduction Ratio")
        ratio_group.setFont(QFont("Arial", 11, QFont.Bold))
        ratio_layout = QHBoxLayout()
        ratio_layout.addWidget(QLabel("Reduction Ratio:"))
        self.ratio_spin = QSpinBox()
        self.ratio_spin.setRange(1, 200)
        self.ratio_spin.setValue(30)
        self.ratio_spin.setMinimumWidth(100)
        ratio_layout.addWidget(self.ratio_spin)
        set_ratio_btn = QPushButton("Set Reduction Ratio")
        set_ratio_btn.clicked.connect(self.set_reduction_ratio)
        ratio_layout.addWidget(set_ratio_btn)
        ratio_layout.addStretch()
        ratio_group.setLayout(ratio_layout)
        scroll_layout.addWidget(ratio_group)
        
        # 5. Wheel Diameter
        wheel_group = QGroupBox("5️⃣ Configure Wheel Diameter (Optional)")
        wheel_group.setFont(QFont("Arial", 11, QFont.Bold))
        wheel_layout = QHBoxLayout()
        wheel_layout.addWidget(QLabel("Wheel Diameter (mm):"))
        self.wheel_spin = QDoubleSpinBox()
        self.wheel_spin.setRange(10.0, 200.0)
        self.wheel_spin.setValue(67.0)
        self.wheel_spin.setDecimals(2)
        self.wheel_spin.setMinimumWidth(100)
        wheel_layout.addWidget(self.wheel_spin)
        set_wheel_btn = QPushButton("Set Wheel Diameter")
        set_wheel_btn.clicked.connect(self.set_wheel_diameter)
        wheel_layout.addWidget(set_wheel_btn)
        wheel_layout.addStretch()
        wheel_group.setLayout(wheel_layout)
        scroll_layout.addWidget(wheel_group)
        
        # 6. PID Configuration
        pid_group = QGroupBox("6️⃣ Configure PID Parameters")
        pid_group.setFont(QFont("Arial", 11, QFont.Bold))
        pid_layout = QVBoxLayout()
        
        motor_row = QHBoxLayout()
        motor_row.addWidget(QLabel("Motor:"))
        self.pid_motor_combo = QComboBox()
        self.pid_motor_combo.addItems(["1", "2", "3", "4"])
        motor_row.addWidget(self.pid_motor_combo)
        motor_row.addStretch()
        pid_layout.addLayout(motor_row)
        
        pid_values_layout = QHBoxLayout()
        pid_values_layout.addWidget(QLabel("P:"))
        self.pid_p_spin = QDoubleSpinBox()
        self.pid_p_spin.setRange(0, 100)
        self.pid_p_spin.setDecimals(3)
        self.pid_p_spin.setSingleStep(0.1)
        pid_values_layout.addWidget(self.pid_p_spin)
        
        pid_values_layout.addWidget(QLabel("I:"))
        self.pid_i_spin = QDoubleSpinBox()
        self.pid_i_spin.setRange(0, 100)
        self.pid_i_spin.setDecimals(3)
        self.pid_i_spin.setSingleStep(0.01)
        pid_values_layout.addWidget(self.pid_i_spin)
        
        pid_values_layout.addWidget(QLabel("D:"))
        self.pid_d_spin = QDoubleSpinBox()
        self.pid_d_spin.setRange(0, 100)
        self.pid_d_spin.setDecimals(3)
        self.pid_d_spin.setSingleStep(0.01)
        pid_values_layout.addWidget(self.pid_d_spin)
        
        set_pid_btn = QPushButton("Set PID Parameters")
        set_pid_btn.clicked.connect(self.set_pid)
        pid_values_layout.addWidget(set_pid_btn)
        pid_values_layout.addStretch()
        
        pid_layout.addLayout(pid_values_layout)
        pid_group.setLayout(pid_layout)
        scroll_layout.addWidget(pid_group)
        
        # 7. Reset
        reset_group = QGroupBox("7️⃣ Reset All Variables")
        reset_group.setFont(QFont("Arial", 11, QFont.Bold))
        reset_layout = QVBoxLayout()
        reset_label = QLabel("⚠️ Reset all configuration to default values")
        reset_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        reset_layout.addWidget(reset_label)
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        reset_btn.clicked.connect(self.reset_defaults)
        reset_layout.addWidget(reset_btn)
        reset_group.setLayout(reset_layout)
        scroll_layout.addWidget(reset_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        self.tabs.addTab(tab, "⚙️ Configuration")
        
    def create_control_tab(self):
        """Tab 3: Control"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # 8. Speed Control
        speed_group = QGroupBox("8️⃣ Control Speed Command (mm/s)")
        speed_group.setFont(QFont("Arial", 11, QFont.Bold))
        speed_layout = QVBoxLayout()
        
        self.speed_sliders = []
        self.speed_spins = []
        
        for i in range(4):
            motor_layout = QHBoxLayout()
            motor_layout.addWidget(QLabel(f"Motor {i+1}:"))
            
            slider = QSlider(Qt.Horizontal)
            slider.setRange(-2000, 2000)
            slider.setValue(0)
            slider.setMinimumWidth(400)
            motor_layout.addWidget(slider)
            
            spin = QSpinBox()
            spin.setRange(-2000, 2000)
            spin.setValue(0)
            spin.setMinimumWidth(80)
            motor_layout.addWidget(spin)
            
            # Connect slider and spinbox
            slider.valueChanged.connect(spin.setValue)
            spin.valueChanged.connect(slider.setValue)
            
            self.speed_sliders.append(slider)
            self.speed_spins.append(spin)
            
            speed_layout.addLayout(motor_layout)
        
        btn_layout = QHBoxLayout()
        send_speed_btn = QPushButton("▶️ Send Speed Command")
        send_speed_btn.setMinimumHeight(40)
        send_speed_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        send_speed_btn.clicked.connect(self.send_speed)
        btn_layout.addWidget(send_speed_btn)
        
        stop_btn = QPushButton("⏹️ Stop All Motors")
        stop_btn.setMinimumHeight(40)
        stop_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        stop_btn.clicked.connect(self.stop_motors)
        btn_layout.addWidget(stop_btn)
        
        speed_layout.addLayout(btn_layout)
        speed_group.setLayout(speed_layout)
        layout.addWidget(speed_group)
        
        # 9. PWM Control
        pwm_group = QGroupBox("9️⃣ Direct Control PWM Instruction (-4095 to 4095)")
        pwm_group.setFont(QFont("Arial", 11, QFont.Bold))
        pwm_layout = QVBoxLayout()
        
        self.pwm_sliders = []
        self.pwm_spins = []
        
        for i in range(4):
            motor_layout = QHBoxLayout()
            motor_layout.addWidget(QLabel(f"Motor {i+1} PWM:"))
            
            slider = QSlider(Qt.Horizontal)
            slider.setRange(-4095, 4095)
            slider.setValue(0)
            slider.setMinimumWidth(400)
            motor_layout.addWidget(slider)
            
            spin = QSpinBox()
            spin.setRange(-4095, 4095)
            spin.setValue(0)
            spin.setMinimumWidth(80)
            motor_layout.addWidget(spin)
            
            slider.valueChanged.connect(spin.setValue)
            spin.valueChanged.connect(slider.setValue)
            
            self.pwm_sliders.append(slider)
            self.pwm_spins.append(spin)
            
            pwm_layout.addLayout(motor_layout)
        
        btn_layout2 = QHBoxLayout()
        send_pwm_btn = QPushButton("▶️ Send PWM Command")
        send_pwm_btn.setMinimumHeight(40)
        send_pwm_btn.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold;")
        send_pwm_btn.clicked.connect(self.send_pwm)
        btn_layout2.addWidget(send_pwm_btn)
        
        stop_pwm_btn = QPushButton("⏹️ Stop All Motors (PWM)")
        stop_pwm_btn.setMinimumHeight(40)
        stop_pwm_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        stop_pwm_btn.clicked.connect(self.stop_motors_pwm)
        btn_layout2.addWidget(stop_pwm_btn)
        
        pwm_layout.addLayout(btn_layout2)
        pwm_group.setLayout(pwm_layout)
        layout.addWidget(pwm_group)
        
        # Auto Test
        auto_group = QGroupBox("🔄 Auto Test Mode")
        auto_group.setFont(QFont("Arial", 11, QFont.Bold))
        auto_layout = QVBoxLayout()
        self.auto_test_btn = QPushButton("▶️ Start Auto Test")
        self.auto_test_btn.setMinimumHeight(40)
        self.auto_test_btn.clicked.connect(self.toggle_auto_test)
        auto_layout.addWidget(self.auto_test_btn)
        auto_group.setLayout(auto_layout)
        layout.addWidget(auto_group)
        
        self.auto_test_running = False
        self.auto_test_timer = QTimer()
        self.auto_test_timer.timeout.connect(self.auto_test_step)
        self.auto_test_value = 0
        
        layout.addStretch()
        self.tabs.addTab(tab, "🎮 Control")
        
    def create_monitor_tab(self):
        """Tab 4: Monitor & Query"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # 10. Encoder Data with STOP button
        encoder_group = QGroupBox("🔟 Report Encoder Data")
        encoder_group.setFont(QFont("Arial", 11, QFont.Bold))
        encoder_layout = QVBoxLayout()
        encoder_layout.addWidget(QLabel("Request encoder data (only for motors with encoder)"))
        
        btn_layout = QHBoxLayout()
        req_total_btn = QPushButton("📊 Request Total Encoder")
        req_total_btn.clicked.connect(lambda: self.request_encoder(1))
        btn_layout.addWidget(req_total_btn)
        
        req_realtime_btn = QPushButton("📈 Request Real-time Encoder")
        req_realtime_btn.clicked.connect(lambda: self.request_encoder(2))
        btn_layout.addWidget(req_realtime_btn)
        
        req_speed_btn = QPushButton("🚀 Request Motor Speed")
        req_speed_btn.clicked.connect(lambda: self.request_encoder(3))
        btn_layout.addWidget(req_speed_btn)
        
        encoder_layout.addLayout(btn_layout)
        
        # STOP Query Button
        stop_query_btn = QPushButton("⏹️ STOP Data Streaming")
        stop_query_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        stop_query_btn.setMinimumHeight(40)
        stop_query_btn.clicked.connect(self.stop_query)
        encoder_layout.addWidget(stop_query_btn)
        
        encoder_group.setLayout(encoder_layout)
        layout.addWidget(encoder_group)
        
        # 11. Query Flash
        query_group = QGroupBox("1️⃣1️⃣ Query Flash Variables")
        query_group.setFont(QFont("Arial", 11, QFont.Bold))
        query_layout = QVBoxLayout()
        query_layout.addWidget(QLabel("Query configuration stored in flash memory"))
        query_btn = QPushButton("🔍 Query Flash Variables")
        query_btn.clicked.connect(self.query_flash)
        query_layout.addWidget(query_btn)
        query_group.setLayout(query_layout)
        layout.addWidget(query_group)
        
        # 12. Battery Level with Real-time Monitor
        battery_group = QGroupBox("1️⃣2️⃣ Battery Level Monitor")
        battery_group.setFont(QFont("Arial", 11, QFont.Bold))
        battery_layout = QVBoxLayout()
        
        # Manual check button
        battery_btn_layout = QHBoxLayout()
        battery_btn = QPushButton("🔋 Check Battery Level")
        battery_btn.clicked.connect(self.check_battery)
        battery_btn_layout.addWidget(battery_btn)
        
        # Auto-monitor toggle
        self.battery_auto_check = QPushButton("▶️ Start Auto-Monitor (5s)")
        self.battery_auto_check.clicked.connect(self.toggle_battery_monitor)
        self.battery_auto_check.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        battery_btn_layout.addWidget(self.battery_auto_check)
        
        battery_layout.addLayout(battery_btn_layout)
        
        # Large battery display
        self.battery_label = QLabel("Battery: -- V")
        self.battery_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.battery_label.setStyleSheet("color: #27ae60; background-color: #ecf0f1; padding: 15px; border-radius: 8px;")
        self.battery_label.setAlignment(Qt.AlignCenter)
        self.battery_label.setMinimumHeight(60)
        battery_layout.addWidget(self.battery_label)
        
        # Battery history textbox
        battery_layout.addWidget(QLabel("Battery Voltage History:"))
        self.battery_history = QTextEdit()
        self.battery_history.setReadOnly(True)
        self.battery_history.setFont(QFont("Consolas", 9))
        self.battery_history.setMaximumHeight(100)
        self.battery_history.setStyleSheet("background-color: #2c3e50; color: #ecf0f1;")
        battery_layout.addWidget(self.battery_history)
        
        battery_group.setLayout(battery_layout)
        layout.addWidget(battery_group)
        
        # Battery auto-monitor timer
        self.battery_monitor_timer = QTimer()
        self.battery_monitor_timer.timeout.connect(self.auto_check_battery)
        self.battery_monitoring = False
        
        # Data Display
        data_group = QGroupBox("📊 Received Data Log")
        data_group.setFont(QFont("Arial", 11, QFont.Bold))
        data_layout = QVBoxLayout()
        
        self.data_text = QTextEdit()
        self.data_text.setReadOnly(True)
        self.data_text.setFont(QFont("Consolas", 9))
        self.data_text.setMinimumHeight(200)
        data_layout.addWidget(self.data_text)
        
        clear_btn = QPushButton("🗑️ Clear Log")
        clear_btn.clicked.connect(self.data_text.clear)
        data_layout.addWidget(clear_btn)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        self.tabs.addTab(tab, "📊 Monitor & Query")
        
    def apply_modern_style(self):
        """Apply modern Qt stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding: 15px;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2c3e50;
            }
            QLabel {
                color: #2c3e50;
                background-color: transparent;
            }
            QRadioButton {
                color: #2c3e50;
                background-color: transparent;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QComboBox, QSpinBox, QDoubleSpinBox {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
                color: #2c3e50;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2c3e50;
                margin-right: 5px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #bdc3c7;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #95a5a6;
                color: white;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
            }
        """)
    
    def refresh_ports(self):
        """Refresh available serial ports"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}")
        
        if self.port_combo.count() == 0:
            self.port_combo.addItem("No ports found")
            self.log_data("⚠️ No serial ports detected. Please check connections.\n")
        else:
            self.log_data(f"✅ Found {self.port_combo.count()} serial port(s)\n")
    
    def toggle_connection(self):
        """Connect or disconnect from serial port"""
        if self.serial_conn and self.serial_conn.is_open:
            self.disconnect()
        else:
            self.connect()
    
    def connect(self):
        """Connect to serial port with better error handling"""
        try:
            port_text = self.port_combo.currentText()
            if "No ports found" in port_text or not port_text:
                QMessageBox.warning(self, "Error", "❌ No serial port selected!\n\nPlease:\n1. Connect your board\n2. Click 'Refresh Ports'\n3. Select the correct port")
                return
            
            port = port_text.split(" - ")[0]
            baudrate = int(self.baud_combo.currentText())
            
            # Try to open serial port
            self.serial_conn = serial.Serial(port, baudrate, timeout=0.1)
            
            # Start reader thread
            self.reader_thread = SerialReaderThread(self.serial_conn)
            self.reader_thread.data_received.connect(self.handle_received_data)
            self.reader_thread.start()
            
            # Update UI
            self.status_label.setText(f"● Status: Connected to {port}")
            self.status_label.setStyleSheet("color: #27ae60;")
            self.connect_btn.setText("🔌 Disconnect")
            self.connect_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
            self.statusBar().showMessage(f"✅ Connected to {port} at {baudrate} baud")
            
            self.log_data(f"\n{'='*60}\n✅ Connected to {port} at {baudrate} baud\n{'='*60}\n")
            
            QMessageBox.information(self, "Success", f"✅ Successfully connected to {port}!")
            
        except serial.SerialException as e:
            error_msg = str(e)
            
            # Better error messages
            if "PermissionError" in error_msg or "Access denied" in error_msg:
                msg = "❌ Port is already in use!\n\n"
                msg += "Please close other programs using this port:\n"
                msg += "• Arduino IDE\n• PuTTY\n• Other serial monitors\n\n"
                msg += "Then try again."
            elif "FileNotFoundError" in error_msg or "could not open port" in error_msg:
                msg = "❌ Port not available!\n\n"
                msg += "The port may have been disconnected.\n"
                msg += "Please:\n1. Check USB connection\n2. Click 'Refresh Ports'\n3. Try again"
            else:
                msg = f"❌ Connection failed!\n\n{error_msg}"
            
            QMessageBox.critical(self, "Connection Error", msg)
            self.log_data(f"❌ Connection Error: {error_msg}\n")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Unexpected error:\n{str(e)}")
            self.log_data(f"❌ Error: {str(e)}\n")
    
    def disconnect(self):
        """Disconnect from serial port"""
        try:
            if self.auto_test_running:
                self.toggle_auto_test()
            
            # Stop battery monitoring if running
            if self.battery_monitoring:
                self.toggle_battery_monitor()
            
            if self.reader_thread:
                self.reader_thread.stop()
                self.reader_thread.wait()
            
            if self.serial_conn and self.serial_conn.is_open:
                self.stop_motors_pwm()
                time.sleep(0.1)
                self.serial_conn.close()
            
            self.status_label.setText("● Status: Disconnected")
            self.status_label.setStyleSheet("color: #e74c3c;")
            self.connect_btn.setText("🔌 Connect")
            self.connect_btn.setStyleSheet("")
            self.statusBar().showMessage("Disconnected")
            
            self.log_data(f"\n{'='*60}\n❌ Disconnected\n{'='*60}\n")
            
        except Exception as e:
            self.log_data(f"Error during disconnect: {str(e)}\n")
    
    def send_data(self, data):
        """Send data to serial port"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(data.encode())
                self.log_data(f"TX: {data}")
                time.sleep(0.01)
                return True
            except Exception as e:
                self.log_data(f"❌ Send error: {str(e)}\n")
                QMessageBox.warning(self, "Error", f"Failed to send data:\n{str(e)}")
                return False
        else:
            QMessageBox.warning(self, "Warning", "⚠️ Not connected to serial port!\n\nPlease connect first.")
            return False
    
    def handle_received_data(self, data):
        """Handle received data from serial"""
        parsed = self.parse_data(data)
        if parsed:
            self.log_data(f"RX: {parsed}\n")
        else:
            self.log_data(f"RX: {data}\n")
    
    def parse_data(self, data):
        """Parse received data"""
        data = data.strip()
        
        if data.startswith("$MAll:"):
            values_str = data[6:-1]
            values = list(map(int, values_str.split(',')))
            return "📊 Total Encoder - " + ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        elif data.startswith("$MTEP:"):
            values_str = data[6:-1]
            values = list(map(int, values_str.split(',')))
            return "📈 Real-time Encoder - " + ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        elif data.startswith("$MSPD:"):
            values_str = data[6:-1]
            values = [float(value) if '.' in value else int(value) for value in values_str.split(',')]
            return "🚀 Motor Speed (mm/s) - " + ', '.join([f"M{i+1}:{value}" for i, value in enumerate(values)])
        elif data.startswith("$battery:") or data.startswith("$Battery:"):
            voltage = data[9:-1]
            self.battery_label.setText(f"Battery: {voltage}")
            
            # Add to battery history
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"[{timestamp}] {voltage}"
            self.battery_history.append(history_entry)
            
            # Auto-scroll to bottom
            self.battery_history.verticalScrollBar().setValue(
                self.battery_history.verticalScrollBar().maximum()
            )
            
            # Update color based on voltage
            try:
                v = float(voltage.replace('V', '').replace('v', ''))
                if v < 6.5:
                    self.battery_label.setStyleSheet("color: #e74c3c; background-color: #ecf0f1; padding: 15px; border-radius: 8px;")  # Red - Critical
                elif v < 7.0:
                    self.battery_label.setStyleSheet("color: #f39c12; background-color: #ecf0f1; padding: 15px; border-radius: 8px;")  # Orange - Low
                else:
                    self.battery_label.setStyleSheet("color: #27ae60; background-color: #ecf0f1; padding: 15px; border-radius: 8px;")  # Green - OK
            except:
                pass
            
            return f"🔋 Battery Level: {voltage}"
        return None
    
    def log_data(self, text):
        """Log data to text widget"""
        self.data_text.append(text)
        # Auto scroll to bottom
        self.data_text.verticalScrollBar().setValue(
            self.data_text.verticalScrollBar().maximum()
        )
    
    # Configuration commands
    def apply_upload_mode(self):
        mode = self.upload_btn_group.checkedId()
        if mode == 0:
            self.send_data("$upload:0,0,0#")
        elif mode == 1:
            self.send_data("$upload:1,0,0#")
        elif mode == 2:
            self.send_data("$upload:0,1,0#")
        elif mode == 3:
            self.send_data("$upload:0,0,1#")
    
    def set_motor_type(self):
        motor_type = self.motor_type_group.checkedId()
        self.motor_type = motor_type
        self.send_data(f"$mtype:{motor_type}#")
    
    def set_deadzone(self):
        deadzone = self.deadzone_spin.value()
        self.send_data(f"$deadzone:{deadzone}#")
    
    def set_phase_lines(self):
        lines = self.lines_spin.value()
        self.send_data(f"$mline:{lines}#")
    
    def set_reduction_ratio(self):
        ratio = self.ratio_spin.value()
        self.send_data(f"$mphase:{ratio}#")
    
    def set_wheel_diameter(self):
        diameter = self.wheel_spin.value()
        self.send_data(f"$wdiameter:{diameter:.2f}#")
    
    def set_pid(self):
        motor = int(self.pid_motor_combo.currentText())
        p = self.pid_p_spin.value()
        i = self.pid_i_spin.value()
        d = self.pid_d_spin.value()
        self.send_data(f"$pid:{motor},{p},{i},{d}#")
    
    def reset_defaults(self):
        reply = QMessageBox.question(self, "Confirm Reset",
                                     "⚠️ Are you sure you want to reset all variables to default values?\n\nThis cannot be undone!",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.send_data("$reset#")
            self.log_data("🔄 RESET: All variables reset to defaults\n")
            QMessageBox.information(self, "Reset Complete", "✅ All variables have been reset to defaults")
    
    def apply_preset_configuration(self):
        """Apply preset configuration based on motor type"""
        if not self.serial_conn or not self.serial_conn.is_open:
            QMessageBox.warning(self, "Warning", "⚠️ Please connect to serial port first!")
            return
        
        motor_type = self.motor_type_group.checkedId()
        
        self.log_data(f"\n⚙️ Applying Preset Configuration for Motor Type {motor_type}...\n")
        
        presets = {
            1: {"mphase": 30, "mline": 11, "wdiameter": 67.0, "deadzone": 1600},
            2: {"mphase": 20, "mline": 13, "wdiameter": 48.0, "deadzone": 1300},
            3: {"mphase": 45, "mline": 13, "wdiameter": 68.0, "deadzone": 1250},
            4: {"mphase": 48, "deadzone": 1000},
            5: {"mphase": 40, "mline": 11, "wdiameter": 67.0, "deadzone": 1600}
        }
        
        if motor_type in presets:
            preset = presets[motor_type]
            
            self.send_data(f"$mtype:{motor_type}#")
            time.sleep(0.1)
            
            if "mphase" in preset:
                self.send_data(f"$mphase:{preset['mphase']}#")
                self.ratio_spin.setValue(preset['mphase'])
                time.sleep(0.1)
            
            if "mline" in preset:
                self.send_data(f"$mline:{preset['mline']}#")
                self.lines_spin.setValue(preset['mline'])
                time.sleep(0.1)
            
            if "wdiameter" in preset:
                self.send_data(f"$wdiameter:{preset['wdiameter']:.2f}#")
                self.wheel_spin.setValue(preset['wdiameter'])
                time.sleep(0.1)
            
            if "deadzone" in preset:
                self.send_data(f"$deadzone:{preset['deadzone']}#")
                self.deadzone_spin.setValue(preset['deadzone'])
                time.sleep(0.1)
            
            self.log_data(f"✅ Preset configuration applied successfully!\n")
            QMessageBox.information(self, "Success", 
                                   f"✅ Preset configuration for Motor Type {motor_type} applied successfully!\n\nConfiguration has been saved to flash memory.")
    
    # Control commands
    def send_speed(self):
        values = [spin.value() for spin in self.speed_spins]
        self.send_data(f"$spd:{values[0]},{values[1]},{values[2]},{values[3]}#")
    
    def send_pwm(self):
        values = [spin.value() for spin in self.pwm_spins]
        self.send_data(f"$pwm:{values[0]},{values[1]},{values[2]},{values[3]}#")
    
    def stop_motors(self):
        self.send_data("$spd:0,0,0,0#")
        for spin in self.speed_spins:
            spin.setValue(0)
    
    def stop_motors_pwm(self):
        self.send_data("$pwm:0,0,0,0#")
        for spin in self.pwm_spins:
            spin.setValue(0)
    
    # Monitor commands
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
        self.log_data("⏹️ STOP: All data streaming stopped\n")
        QMessageBox.information(self, "Stopped", "✅ Data streaming stopped!\n\nNo more encoder/speed data will be sent.")
    
    def query_flash(self):
        self.send_data("$query#")
        self.log_data("🔍 Query: Requesting flash variables...\n")
    
    def check_battery(self):
        self.send_data("$read_vol#")
        self.log_data("🔋 Query: Requesting battery level...\n")
    
    def toggle_battery_monitor(self):
        """Toggle auto battery monitoring"""
        if self.battery_monitoring:
            # Stop monitoring
            self.battery_monitoring = False
            self.battery_monitor_timer.stop()
            self.battery_auto_check.setText("▶️ Start Auto-Monitor (5s)")
            self.battery_auto_check.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
            self.log_data("⏹️ Battery auto-monitor stopped\n")
        else:
            # Start monitoring
            if not self.serial_conn or not self.serial_conn.is_open:
                QMessageBox.warning(self, "Warning", "⚠️ Please connect to serial port first!")
                return
            
            self.battery_monitoring = True
            self.battery_monitor_timer.start(5000)  # Every 5 seconds
            self.battery_auto_check.setText("⏹️ Stop Auto-Monitor")
            self.battery_auto_check.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
            self.log_data("▶️ Battery auto-monitor started (checking every 5 seconds)\n")
            # Check immediately
            self.auto_check_battery()
    
    def auto_check_battery(self):
        """Auto check battery - called by timer"""
        if self.serial_conn and self.serial_conn.is_open:
            self.send_data("$read_vol#")
            # Don't log to main log to avoid spam

    
    # Auto test
    def toggle_auto_test(self):
        if self.auto_test_running:
            self.auto_test_running = False
            self.auto_test_timer.stop()
            self.auto_test_btn.setText("▶️ Start Auto Test")
            self.auto_test_btn.setStyleSheet("")
            self.log_data("⏹️ Auto Test Stopped\n")
        else:
            if not self.serial_conn or not self.serial_conn.is_open:
                QMessageBox.warning(self, "Warning", "⚠️ Please connect to serial port first!")
                return
            
            self.auto_test_running = True
            self.auto_test_value = 0
            self.auto_test_timer.start(100)
            self.auto_test_btn.setText("⏹️ Stop Auto Test")
            self.auto_test_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
            self.log_data("▶️ Auto Test Started\n")
    
    def auto_test_step(self):
        if self.motor_type == 4:
            self.send_data(f"$pwm:{self.auto_test_value*2},{self.auto_test_value*2},{self.auto_test_value*2},{self.auto_test_value*2}#")
        else:
            self.send_data(f"$spd:{self.auto_test_value},{self.auto_test_value},{self.auto_test_value},{self.auto_test_value}#")
        
        for spin in self.speed_spins:
            spin.setValue(self.auto_test_value)
        
        self.auto_test_value += 10
        if self.auto_test_value > 1000:
            self.auto_test_value = 0
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.serial_conn and self.serial_conn.is_open:
            reply = QMessageBox.question(self, "Confirm Exit",
                                        "Still connected to serial port.\n\nDisconnect and exit?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.disconnect()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    # Set app icon if available
    # app.setWindowIcon(QIcon('icon.png'))
    
    window = MotorBoardGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
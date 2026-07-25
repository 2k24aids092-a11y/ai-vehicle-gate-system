-- ============================================================
-- AI SMART VEHICLE GATE ACCESS SYSTEM - DATABASE SCHEMA
-- ============================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS vehicle_gate_system;
USE vehicle_gate_system;

-- ============================================================
-- USERS TABLE
-- ============================================================
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role ENUM('admin', 'manager', 'security') NOT NULL DEFAULT 'manager',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_created_at (created_at)
);

-- ============================================================
-- VEHICLES TABLE
-- ============================================================
CREATE TABLE vehicles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plate_number VARCHAR(50) UNIQUE NOT NULL,
    owner_name VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    phone VARCHAR(20),
    vehicle_type ENUM('Car', 'Bike', 'Bus', 'Truck', 'Van') NOT NULL,
    access_level ENUM('full', 'restricted', 'temporary', 'none') DEFAULT 'full',
    status ENUM('active', 'inactive', 'blacklisted', 'pending') DEFAULT 'active',
    photo_url VARCHAR(500),
    notes TEXT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_plate_number (plate_number),
    INDEX idx_status (status),
    INDEX idx_access_level (access_level),
    INDEX idx_created_at (created_at),
    UNIQUE KEY unique_plate (plate_number)
);

-- ============================================================
-- PARKING SLOTS TABLE
-- ============================================================
CREATE TABLE parking_slots (
    id INT PRIMARY KEY AUTO_INCREMENT,
    slot_number VARCHAR(10) UNIQUE NOT NULL,
    floor INT DEFAULT 1,
    section VARCHAR(5),
    status ENUM('available', 'occupied', 'reserved', 'maintenance') DEFAULT 'available',
    vehicle_id INT,
    reserved_until DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    INDEX idx_status (status),
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_slot_number (slot_number)
);

-- ============================================================
-- ENTRY LOGS TABLE
-- ============================================================
CREATE TABLE entry_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_id INT NOT NULL,
    plate_number VARCHAR(50) NOT NULL,
    entry_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_time TIMESTAMP NULL,
    duration_minutes INT NULL,
    parking_slot VARCHAR(10),
    gate_number INT DEFAULT 1,
    detection_confidence FLOAT,
    access_status ENUM('granted', 'denied', 'pending') DEFAULT 'granted',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_plate_number (plate_number),
    INDEX idx_entry_time (entry_time),
    INDEX idx_access_status (access_status),
    INDEX idx_created_at (created_at)
);

-- ============================================================
-- VISITORS TABLE
-- ============================================================
CREATE TABLE visitors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    visitor_name VARCHAR(255) NOT NULL,
    visitor_phone VARCHAR(20),
    vehicle_number VARCHAR(50) NOT NULL,
    vehicle_type ENUM('Car', 'Bike', 'Bus', 'Truck', 'Van'),
    purpose VARCHAR(500),
    approval_status ENUM('pending', 'approved', 'rejected', 'expired') DEFAULT 'pending',
    approved_by INT,
    approved_at TIMESTAMP NULL,
    valid_from TIMESTAMP,
    valid_until TIMESTAMP,
    photo_url VARCHAR(500),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (approved_by) REFERENCES users(id),
    INDEX idx_approval_status (approval_status),
    INDEX idx_vehicle_number (vehicle_number),
    INDEX idx_created_at (created_at)
);

-- ============================================================
-- UNAUTHORIZED ATTEMPTS TABLE
-- ============================================================
CREATE TABLE unauthorized_attempts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plate_number VARCHAR(50),
    vehicle_type VARCHAR(50),
    detection_confidence FLOAT,
    gate_number INT DEFAULT 1,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_url VARCHAR(500),
    status VARCHAR(50),
    resolved_by INT,
    resolved_at TIMESTAMP NULL,
    notes TEXT,
    FOREIGN KEY (resolved_by) REFERENCES users(id),
    INDEX idx_plate_number (plate_number),
    INDEX idx_attempt_time (attempt_time),
    INDEX idx_status (status)
);

-- ============================================================
-- ALERTS TABLE
-- ============================================================
CREATE TABLE alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    alert_type ENUM('unauthorized_vehicle', 'blacklisted_vehicle', 'camera_offline', 'parking_full', 'gate_error', 'custom') DEFAULT 'custom',
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    related_vehicle_id INT,
    related_attempt_id INT,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_by INT,
    resolved_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (related_vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (related_attempt_id) REFERENCES unauthorized_attempts(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_severity (severity),
    INDEX idx_is_resolved (is_resolved),
    INDEX idx_created_at (created_at)
);

-- ============================================================
-- SYSTEM SETTINGS TABLE
-- ============================================================
CREATE TABLE system_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    setting_key VARCHAR(255) UNIQUE NOT NULL,
    setting_value TEXT,
    data_type ENUM('string', 'integer', 'boolean', 'json') DEFAULT 'string',
    description TEXT,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id),
    INDEX idx_setting_key (setting_key)
);

-- ============================================================
-- AUDIT LOG TABLE
-- ============================================================
CREATE TABLE audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100),
    entity_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
);

-- ============================================================
-- REPORTS TABLE
-- ============================================================
CREATE TABLE reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_type ENUM('daily', 'weekly', 'monthly', 'custom') NOT NULL,
    report_date DATE NOT NULL,
    total_entries INT DEFAULT 0,
    total_exits INT DEFAULT 0,
    vehicles_inside INT DEFAULT 0,
    parking_occupancy_percentage FLOAT DEFAULT 0,
    unauthorized_attempts INT DEFAULT 0,
    blacklisted_attempts INT DEFAULT 0,
    generated_by INT,
    data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (generated_by) REFERENCES users(id),
    INDEX idx_report_type (report_type),
    INDEX idx_report_date (report_date),
    INDEX idx_created_at (created_at)
);

-- ============================================================
-- INSERT DEFAULT DATA
-- ============================================================

-- Insert default users
INSERT INTO users (email, password_hash, name, role, is_active) VALUES
('admin@example.com', '$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUm', 'Admin User', 'admin', TRUE),
('manager@example.com', '$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUm', 'Transport Manager', 'manager', TRUE),
('security@example.com', '$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUm', 'Security Officer', 'security', TRUE);

-- Insert sample vehicles
INSERT INTO vehicles (plate_number, owner_name, department, phone, vehicle_type, access_level, status) VALUES
('TN37AB1234', 'John Doe', 'Engineering', '9876543210', 'Car', 'full', 'active'),
('DL01CD5678', 'Jane Smith', 'HR', '9876543211', 'Car', 'full', 'active'),
('MH02EF9012', 'Mike Johnson', 'Sales', '9876543212', 'Bike', 'restricted', 'active'),
('KA03GH3456', 'Sarah Williams', 'Finance', '9876543213', 'Car', 'full', 'active'),
('TN37AB9999', 'Blacklisted Vehicle', 'Unknown', '0000000000', 'Car', 'none', 'blacklisted');

-- Insert parking slots (50 slots total)
INSERT INTO parking_slots (slot_number, floor, section, status) VALUES
('A1', 1, 'A', 'available'),
('A2', 1, 'A', 'available'),
('A3', 1, 'A', 'available'),
('A4', 1, 'A', 'available'),
('A5', 1, 'A', 'available'),
('B1', 1, 'B', 'available'),
('B2', 1, 'B', 'available'),
('B3', 1, 'B', 'available'),
('B4', 1, 'B', 'available'),
('B5', 1, 'B', 'available'),
('C1', 2, 'C', 'available'),
('C2', 2, 'C', 'available'),
('C3', 2, 'C', 'available'),
('C4', 2, 'C', 'available'),
('C5', 2, 'C', 'available'),
('D1', 2, 'D', 'available'),
('D2', 2, 'D', 'available'),
('D3', 2, 'D', 'available'),
('D4', 2, 'D', 'available'),
('D5', 2, 'D', 'available'),
('E1', 3, 'E', 'available'),
('E2', 3, 'E', 'available'),
('E3', 3, 'E', 'available'),
('E4', 3, 'E', 'available'),
('E5', 3, 'E', 'available'),
('F1', 3, 'F', 'available'),
('F2', 3, 'F', 'available'),
('F3', 3, 'F', 'available'),
('F4', 3, 'F', 'available'),
('F5', 3, 'F', 'available'),
('G1', 4, 'G', 'available'),
('G2', 4, 'G', 'available'),
('G3', 4, 'G', 'available'),
('G4', 4, 'G', 'available'),
('G5', 4, 'G', 'available'),
('H1', 4, 'H', 'available'),
('H2', 4, 'H', 'available'),
('H3', 4, 'H', 'available'),
('H4', 4, 'H', 'available'),
('H5', 4, 'H', 'available'),
('I1', 5, 'I', 'available'),
('I2', 5, 'I', 'available'),
('I3', 5, 'I', 'available'),
('I4', 5, 'I', 'available'),
('I5', 5, 'I', 'available'),
('J1', 5, 'J', 'available'),
('J2', 5, 'J', 'available'),
('J3', 5, 'J', 'available'),
('J4', 5, 'J', 'available'),
('J5', 5, 'J', 'available');

-- Insert default system settings
INSERT INTO system_settings (setting_key, setting_value, data_type, description) VALUES
('parking_capacity', '50', 'integer', 'Total parking capacity'),
('gate_opening_delay', '2', 'integer', 'Gate opening delay in seconds'),
('gate_closing_delay', '5', 'integer', 'Gate closing delay in seconds'),
('yolo_confidence_threshold', '0.5', 'string', 'YOLOv8 detection confidence threshold'),
('ocr_confidence_threshold', '0.5', 'string', 'EasyOCR confidence threshold'),
('alert_unauthorized_attempts', 'true', 'boolean', 'Enable alerts for unauthorized attempts'),
('camera_resolution', '1280x720', 'string', 'Camera resolution'),
('camera_fps', '30', 'integer', 'Camera FPS');

-- ============================================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================================
CREATE INDEX idx_vehicles_plate ON vehicles(plate_number);
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_entry_logs_date ON entry_logs(entry_time);
CREATE INDEX idx_entry_logs_vehicle ON entry_logs(vehicle_id);
CREATE INDEX idx_parking_status ON parking_slots(status);
CREATE INDEX idx_alerts_type ON alerts(alert_type);
CREATE INDEX idx_unauthorized_time ON unauthorized_attempts(attempt_time);

-- ============================================================
-- VIEWS FOR DASHBOARD
-- ============================================================

-- Today's entries count
CREATE VIEW v_today_entries AS
SELECT COUNT(*) as count FROM entry_logs WHERE DATE(entry_time) = CURDATE() AND access_status = 'granted';

-- Today's exits count
CREATE VIEW v_today_exits AS
SELECT COUNT(*) as count FROM entry_logs WHERE DATE(exit_time) = CURDATE();

-- Currently parked vehicles
CREATE VIEW v_vehicles_inside AS
SELECT COUNT(*) as count FROM entry_logs 
WHERE DATE(entry_time) = CURDATE() AND exit_time IS NULL AND access_status = 'granted';

-- Parking occupancy
CREATE VIEW v_parking_occupancy AS
SELECT 
    COUNT(*) as total_slots,
    SUM(CASE WHEN status = 'occupied' THEN 1 ELSE 0 END) as occupied,
    SUM(CASE WHEN status = 'available' THEN 1 ELSE 0 END) as available,
    SUM(CASE WHEN status = 'reserved' THEN 1 ELSE 0 END) as reserved,
    ROUND((SUM(CASE WHEN status = 'occupied' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as occupancy_percentage
FROM parking_slots;

-- Unauthorized attempts today
CREATE VIEW v_unauthorized_today AS
SELECT COUNT(*) as count FROM unauthorized_attempts WHERE DATE(attempt_time) = CURDATE();

-- Active visitors
CREATE VIEW v_active_visitors AS
SELECT COUNT(*) as count FROM visitors 
WHERE approval_status = 'approved' AND NOW() BETWEEN valid_from AND valid_until;

-- Blacklisted vehicles
CREATE VIEW v_blacklisted_vehicles AS
SELECT COUNT(*) as count FROM vehicles WHERE status = 'blacklisted';

-- ============================================================
-- END OF SCHEMA
-- ============================================================

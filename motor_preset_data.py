
power_groups = {
    "🔧 小功率电机 (≤1kW)": ["🔧 小功率电机 (100W)", "🔋 直流伺服电机 (400W)", "💧 水泵电机 (415W)", "🎯 伺服电机 (750W)"],
    "⚙️ 中功率电机 (1-100kW)": ["⚙️ 工业电机 (5kW)", "🚗 汽车电机 (50kW)", "🚗 北汽EU5电机 (80kW)", "🏭 西安电机 (83kW)"],
    "🏭 大功率电机 (≥100kW)": ["🚀 高速电机 (200kW)", "🏭 大功率工业 (200kW)", "💨 高速空压机电机", "🌊 船舶推进 (500kW)", "🚄 牵引电机 (1MW)"]
}

motors = {
    "🚀 高速电机 (200kW)": {
        "pole_pairs": "2",
        "rated_speed_rpm": "45000",
        "stator_resistance": "0.008",
        "stator_inductance": "0.00035",
        "flux_linkage": "0.0386",
        "rated_current": "460",
        "rated_line_back_emf": "445.7",
        "rated_line_voltage": "480",
        "rated_torque": "42.44",
        "motor_mass": "10.0",
        "rated_power": "200",
        "power_factor": "0.8",
        "efficiency": "94.5"
    },
    "⚙️ 工业电机 (5kW)": {
        "pole_pairs": "4",
        "rated_speed_rpm": "1500",
        "rated_power": "5",
        "rated_torque": "32",
        "rated_line_voltage": "380",
        "power_factor": "0.85",
        "efficiency": "92",
        "stator_resistance": "0.18",
        "stator_inductance": "0.0025"
    },
    "🎯 伺服电机 (750W)": {
        "pole_pairs": "3",
        "rated_speed_rpm": "3000",
        "rated_power": "0.75",
        "rated_torque": "2.39",
        "rated_current": "3.2",
        "rated_line_voltage": "220",
        "stator_resistance": "1.2",
        "stator_inductance": "0.008",
        "flux_linkage": "0.075",
        "power_factor": "0.9",
        "efficiency": "88",
        "moment_of_inertia": "0.00032"
    },
    "🚗 汽车电机 (50kW)": {
        "pole_pairs": "4",
        "rated_speed_rpm": "8000",
        "rated_power": "50",
        "rated_torque": "60",
        "rated_current": "150",
        "rated_line_voltage": "400",
        "bus_voltage": "650",
        "stator_resistance": "0.025",
        "stator_inductance": "0.0008",
        "power_factor": "0.85",
        "efficiency": "95",
        "motor_mass": "25"
    },
    "🏭 大功率工业 (200kW)": {
        "pole_pairs": "6",
        "rated_speed_rpm": "1000",
        "rated_power": "200",
        "rated_torque": "1910",
        "rated_current": "350",
        "rated_line_voltage": "690",
        "stator_resistance": "0.012",
        "stator_inductance": "0.0018",
        "power_factor": "0.88",
        "efficiency": "96"
    },
    "🚄 牵引电机 (1MW)": {
        "pole_pairs": "2",
        "rated_speed_rpm": "4500",
        "rated_power": "1000",
        "rated_torque": "2122",
        "rated_current": "1200",
        "rated_line_voltage": "1500",
        "bus_voltage": "2500",
        "stator_resistance": "0.003",
        "stator_inductance": "0.00015",
        "power_factor": "0.9",
        "efficiency": "97",
        "motor_mass": "450"
    },
    "🔧 小功率电机 (100W)": {
        "pole_pairs": "2",
        "rated_speed_rpm": "2800",
        "rated_power": "0.1",
        "rated_torque": "0.34",
        "rated_current": "0.8",
        "rated_line_voltage": "110",
        "power_factor": "0.75",
        "efficiency": "80",
        "stator_resistance": "8.5",
        "stator_inductance": "0.025",
        "motor_mass": "0.8"
    },
    "🔋 直流伺服电机 (400W)": {
        "pole_pairs": "4",
        "rated_speed_rpm": "3100",
        "rated_power": "0.4",
        "rated_torque": "1.27",
        "rated_current": "11",
        "rated_line_voltage": "",
        "bus_voltage": "48",
        "power_factor": "0.85",
        "efficiency": "85",
        "stator_resistance": "0.15",
        "stator_inductance": "0.000708",
        "flux_linkage": "",
        "moment_of_inertia": "0.00029",
        "motor_mass": "1.2"
    },
    "💧 水泵电机 (415W)": {
        "pole_pairs": "5",
        "rated_speed_rpm": "5000",
        "rated_power": "0.415",
        "rated_current": "66",
        "rated_line_voltage": "",
        "bus_voltage": "12",
        "power_factor": "0.8",
        "efficiency": "82",
        "stator_resistance": "0.04029",
        "stator_inductance_d": "0.000156",
        "stator_inductance": "0.000205",
        "flux_linkage": "0.001676",
        "motor_mass": ""
    },
    "🌊 船舶推进 (500kW)": {
        "pole_pairs": "8",
        "rated_speed_rpm": "750",
        "rated_power": "500",
        "rated_torque": "6366",
        "rated_current": "650",
        "rated_line_voltage": "690",
        "stator_resistance": "0.005",
        "stator_inductance": "0.0012",
        "power_factor": "0.87",
        "efficiency": "96",
        "motor_mass": "180"
    },
    "🚗 北汽EU5电机 (80kW)": {
        "pole_pairs": "4",
        "rated_power": "80",
        "rated_speed_rpm": "5100",
        "stator_resistance": "0.00736",
        "stator_inductance": "0.000273",
        "flux_linkage": "0.0190"
    },
    "💨 高速空压机电机": {
        "pole_pairs": "1",
        "rated_speed_rpm": "50000",
        "stator_resistance": "0.0538",
        "stator_inductance": "0.000127",
        "flux_linkage": "0.05",
        "bus_voltage": "500"
    },
    "🏭 西安电机 (83kW)": {
        "pole_pairs": "2",
        "rated_power": "83",
        "rated_speed_rpm": "25000",
        "rated_torque": "32",
        "rated_current": "153",
        "stator_resistance": "0.0098",
        "stator_inductance": "0.000153",
        "flux_linkage": "0.05",
        "bus_voltage": "540",
        "moment_of_inertia": "0.003"
    }
}
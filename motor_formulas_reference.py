#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电机计算公式参考表
严谨的变量定义和单位说明
"""

class MotorFormulas:
    """
    电机计算公式参考类
    提供严谨的变量定义和单位说明
    """
    
    @staticmethod
    def get_variable_definitions():
        """
        获取所有变量的严谨定义
        返回: dict - 变量名: (符号, 单位, 描述)
        """
        return {
            # 基本参数
            'pole_pairs': ('p', '对', '极对数'),
            'rated_power': ('P_rated', 'KW', '额定功率'),
            'rated_speed': ('n_rated', 'r/min', '额定转速'),
            'rated_torque': ('T_rated', 'N·m', '额定转矩'),
            'rated_frequency': ('f_rated', 'Hz', '额定频率'),
            
            # 电气参数 - 星型连接
            'stator_resistance': ('R_s', 'Ω', '定子电阻'),
            'stator_inductance': ('L_s', 'H', '定子电感'),
            'flux_linkage': ('Ψ', 'Wb', '磁链'),
            'back_emf_constant': ('Ke', 'V·s/rad', '反电动势常数'),
            'torque_constant': ('Kt', 'N·m/A', '转矩常数'),
            
            # 反电动势参数 - 星型连接
            'rated_line_back_emf': ('E_line_rated', 'V', '额定线反电动势(有效值)'),
            'rated_phase_back_emf': ('E_phase_rated', 'V', '额定相反电动势(有效值)'),
            'peak_line_back_emf': ('E_line_peak', 'V', '峰值线反电动势'),
            'peak_phase_back_emf': ('E_phase_peak', 'V', '峰值相反电动势'),
            
            # 电压参数 - 星型连接
            'rated_line_voltage': ('U_line_rated', 'V', '额定线电压(有效值)'),
            'rated_phase_voltage': ('U_phase_rated', 'V', '额定相电压(有效值)'),
            'peak_line_voltage': ('U_line_peak', 'V', '峰值线电压'),
            'peak_phase_voltage': ('U_phase_peak', 'V', '峰值相电压'),
            
            # 电流参数 - 星型连接(线电流=相电流)
            'rated_current': ('I_rated', 'A', '额定电流(有效值)'),
            'peak_current': ('I_peak', 'A', '峰值电流'),
            
            'power_factor': ('cosφ', '无量纲', '功率因数'),
            'apparent_power': ('S', 'VA', '视在功率'),
            'reactive_power': ('Q', 'VAR', '无功功率'),
            'reactance': ('XL', 'Ω', '感抗'),
            'impedance': ('Z', 'Ω', '阻抗'),
            'frequency': ('f', 'Hz', '频率'),
            'electrical_frequency': ('f_e', 'Hz', '电气频率'),
            
            # 机械参数
            'rated_torque': ('T_rated', 'N·m', '额定转矩'),
            'startup_torque': ('T_startup', 'N·m', '启动转矩'),
            'max_torque': ('T_max', 'N·m', '最大转矩'),
            'load_torque': ('T_load', 'N·m', '负载转矩'),
            'speed_rpm': ('n', 'r/min', '转速'),
            'angular_velocity': ('ω', 'rad/s', '角速度'),
            'moment_of_inertia': ('J', 'kg·m²', '转动惯量'),
            'slip': ('s', '无量纲', '转差率'),
            'synchronous_speed': ('n_s', 'r/min', '同步转速'),
            'mechanical_power': ('P_mech', 'KW', '机械功率'),
            'electrical_power': ('P_elec', 'KW', '电气功率'),
            
            # 电机常数
            'back_emf_constant': ('Ke', 'V·s/rad', '反电动势常数'),
            'torque_constant': ('Kt', 'N·m/A', '转矩常数'),
            'flux_linkage': ('Ψ', 'Wb', '磁链'),
            
            # 频率参数
            'electrical_frequency': ('f_e', 'Hz', '电气频率'),
            'mechanical_frequency': ('f_m', 'Hz', '机械频率'),
            
            # 效率和损耗
            'efficiency': ('η', '%', '效率'),
            'copper_losses': ('P_cu', 'KW', '铜损'),
            'P_cu_rated': ('P_cu_rated', 'KW', '额定铜损'),
            'P_cu_overload': ('P_cu_overload', 'KW', '过载铜损'),
            'iron_losses': ('P_fe', 'KW', '铁损'),
            'total_losses': ('P_loss', 'KW', '总损耗'),
            
            # 时间常数和热参数
            'thermal_time_constant': ('τ_th', 's', '热时间常数'),
            'electrical_time_constant': ('τ_e', 's', '电气时间常数'),
            'mechanical_time_constant': ('τ_m', 's', '机械时间常数'),
            'C_th': ('C_th', 'J/K', '热容'),
            'G_th': ('G_th', 'W/K', '热导'),
            
            # 过载相关参数
            'k_overload': ('k_overload', '无量纲', '过载倍数'),
            'I_overload': ('I_overload', 'A', '过载电流'),
            'T_overload': ('T_overload', 'N·m', '过载转矩'),
            'P_overload': ('P_overload', 'KW', '过载功率'),
            'U_phase_overload': ('U_phase_overload', 'V', '过载相电压'),
            'U_line_overload': ('U_line_overload', 'V', '过载线电压'),
            'U_bus_overload': ('U_bus_overload', 'V', '过载母线电压'),
            'overload_duration': ('t_overload', 's', '过载持续时间'),
            
            # 经验常数
            'k': ('k', '无量纲', '经验常数'),
            'k_L': ('k_L', '无量纲', '电感经验常数'),
            
            # 数学常数和函数
            'pi': ('π', '无量纲', '圆周率'),
            'sqrt': ('√', '无量纲', '平方根函数'),
            
            # 符号形式的变量（用于公式显示）
            'p': ('p', '对', '极对数'),
            'P_rated': ('P_rated', 'W', '额定功率'),
            'P_mech': ('P_mech', 'W', '机械功率'),
            'P_elec': ('P_elec', 'W', '电气功率'),
            'T': ('T', 'N·m', '转矩'),
            'n': ('n', 'r/min', '转速'),
            'ω': ('ω', 'rad/s', '角速度'),
            'K_e': ('K_e', 'V·s/rad', '反电动势常数'),
            'K_t': ('K_t', 'N·m/A', '转矩常数'),
            'Ψ': ('Ψ', 'Wb', '磁链'),
            'π': ('π', '无量纲', '圆周率'),
            
            # 添加更多常用符号
            'm_rotor': ('m_rotor', 'kg', '转子质量'),
            'r': ('r', 'm', '半径'),
            'r²': ('r²', 'm²', '半径平方'),
            'ω²': ('ω²', '(rad/s)²', '角速度平方'),
            'cos': ('cos', '无量纲', '余弦函数'),
            'φ': ('φ', 'rad', '功率因数角'),
            'μ₀': ('μ₀', 'H/m', '真空磁导率'),
            'D': ('D', 'm', '直径'),
            'l': ('l', 'm', '铁心长度'),
            'L': ('L', 'H', '电感'),

            'E_line_rated': ('E_line_rated', 'V', '额定线反电动势'),
            'E_phase_rated': ('E_phase_rated', 'V', '额定相反电动势'),
            'E_phase': ('E_phase', 'V', '相反电动势'),
            'Z': ('Z', 'Ω', '阻抗'),
            'XL': ('XL', 'Ω', '感抗'),
            'S': ('S', 'VA', '视在功率'),
            'Q': ('Q', 'VAR', '无功功率'),
            'I_q': ('I_q', 'A', 'q轴电流'),
            'I_d': ('I_d', 'A', 'd轴电流'),
            'L_base': ('L_base', 'H', '基准电感'),
            'P_base': ('P_base', 'W', '基准功率'),
            'k_R': ('k_R', '无量纲', '电阻经验常数'),
            
            # 添加常用符号的直接定义
            'I': ('I', 'A', '电流'),
            'R': ('R', 'Ω', '电阻'),
            'L': ('L', 'H', '电感'),
            'U': ('U', 'V', '电压'),
            'P': ('P', 'W', '功率'),
            'η': ('η', '%', '效率'),
            'α': ('α', 'rad/s²', '角加速度'),
            'f': ('f', 'Hz', '频率'),
            's': ('s', '无量纲', '转差率'),
            'cosφ': ('cosφ', '无量纲', '功率因数'),
            'sinφ': ('sinφ', '无量纲', '功率因数正弦值'),

            'μ': ('μ', '无量纲', '摩擦系数'),
            'μ₀': ('μ₀', 'H/m', '真空磁导率'),
            'ρ': ('ρ', 'kg/m³', '密度'),
            'λ': ('λ', 'Wb', '磁链'),
            'θ': ('θ', 'rad', '角度'),
            'δ': ('δ', 'rad', '功率角'),
            'σ': ('σ', 'S/m', '电导率'),
            'm': ('m', 'kg', '质量'),
            'v': ('v', 'm/s', '速度'),
            'a': ('a', 'm/s²', '加速度'),
            'F': ('F', 'N', '力'),
            'W': ('W', 'J', '能量'),
            'C': ('C', 'F', '电容'),
            'B': ('B', 'T', '磁感应强度'),
            'H': ('H', 'A/m', '磁场强度'),
            'A': ('A', 'm²', '面积'),
            'V': ('V', 'm³', '体积'),
            't': ('t', 's', '时间'),
            
            # 添加复合符号和下标符号的定义
            'Ke': ('Ke', 'V·s/rad', '反电动势常数'),
            'Kt': ('Kt', 'N·m/A', '转矩常数'),
            'f_e': ('f_e', 'Hz', '电气频率'),
            'P_cu': ('P_cu', 'W', '铜损'),
            'I_rated': ('I_rated', 'A', '额定电流(有效值)'),
            'U_line_rated': ('U_line_rated', 'V', '额定线电压'),
            'U_phase_rated': ('U_phase_rated', 'V', '额定相电压'),
            'P_overload': ('P_overload', 'W', '过载功率'),
            'th': ('th', 's', '热时间常数下标'),
            'e': ('e', 's', '电气时间常数下标'),
            'T_rated': ('T_rated', 'N·m', '额定转矩'),
            'T_startup': ('T_startup', 'N·m', '启动转矩'),
            'T_overload': ('T_overload', 'N·m', '过载转矩'),
            'T_start': ('T_start', 'N·m', '启动转矩'),
            'T_max': ('T_max', 'N·m', '最大转矩'),
            'T_breakdown': ('T_breakdown', 'N·m', '临界转矩'),
            'T_load': ('T_load', 'N·m', '负载转矩'),
            'n_rated': ('n_rated', 'r/min', '额定转速'),
            'n_s': ('n_s', 'r/min', '同步转速'),
            's_rated': ('s_rated', '无量纲', '额定转差率'),
            'P_mech': ('P_mech', 'W', '机械功率'),
            'P_elec': ('P_elec', 'W', '电气功率'),
            'P_rated': ('P_rated', 'W', '额定功率'),
            'P_fe': ('P_fe', 'W', '铁损'),
            'P_loss': ('P_loss', 'W', '总损耗'),
            'P_cu_rated': ('P_cu_rated', 'W', '额定铜损'),
            'P_cu_overload': ('P_cu_overload', 'W', '过载铜损'),
            'f_rated': ('f_rated', 'Hz', '额定频率'),
            'f_m': ('f_m', 'Hz', '机械频率'),
            'R_s': ('R_s', 'Ω', '定子电阻'),
            'L_s': ('L_s', 'H', '定子电感'),
            'R_est': ('R_est', 'Ω', '估算电阻'),
            'I_est': ('I_est', 'A', '估算电流'),
            'I_overload': ('I_overload', 'A', '过载电流'),
            'E_line_rated': ('E_line_rated', 'V', '额定线反电动势'),
            'E_phase_rated': ('E_phase_rated', 'V', '额定相反电动势'),
            'U_line_rated': ('U_line_rated', 'V', '额定线电压'),
            'U_phase_rated': ('U_phase_rated', 'V', '额定相电压'),
            'I_peak': ('I_peak', 'A', '峰值电流'),
            'E_phase_peak': ('E_phase_peak', 'V', '相反电动势峰值'),
            'τ_th': ('τ_th', 's', '热时间常数'),
            'τ_e': ('τ_e', 's', '电气时间常数'),
            'τ_m': ('τ_m', 's', '机械时间常数'),
        }
    
    @staticmethod
    def get_formula_definitions():
        """
        获取所有公式的严谨定义
        返回: dict - 公式名: (公式, 说明, 适用条件)
        """
        return {
            # 基本关系式
            'angular_velocity': (
                'ω = 2π × n / 60',
                '角速度与转速的关系',
                '适用于所有旋转电机'
            ),
            
            'electrical_frequency': (
                'f_e = p × n / 60',
                '电气频率计算，p为极对数，n为转速(r/min)',
                '适用于同步电机和异步电机'
            ),
            
            # 磁链相关公式
            'flux_linkage_from_voltage': (
                'Ψ = E_phase_peak / (p × ω)',
                '基于相反电动势峰值计算磁链，p为极对数，ω为角速度',
                '需要准确的相反电动势峰值测量值，适用于星型连接电机'
            ),
            
            'flux_linkage_from_torque': (
                'Ψ = (2/3) × T / (p × I_rated)',
                '基于转矩和电流的精确计算，p为极对数',
                '基于完整三相电机模型的精确公式'
            ),
            
            'flux_linkage_from_power': (
                'Ψ = (2/3) × P_rated / (p × I_est × ω)',
                '基于额定功率的精确计算，p为极对数',
                '基于完整三相电机模型，精度较高'
            ),
            
            # 电机常数公式
            'back_emf_constant_phase': (
                'Ke = Ψ × p',
                '相反电动势常数，Ψ为磁链，p为极对数',
                '基于相电压的反电动势常数'
            ),
            
            'back_emf_constant_from_voltage': (
                'Ke = E_phase_peak / ω',
                '基于相反电动势峰值的反电动势常数',
                '需要准确的相反电动势峰值和角速度测量值'
            ),
            
            'torque_constant': (
                'Kt = (3/2) × p × Ψ',
                '转矩常数，p为极对数，Ψ为磁链',
                '完整三相电机模型'
            ),
            
            'torque_constant_from_measurement': (
                'Kt = T / I',
                '基于测量的转矩常数',
                '需要准确的转矩和电流测量值'
            ),
            
            'kt_ke_relationship': (
                'Kt = 1.5 × Ke',
                '转矩常数与反电动势常数的理论关系',
                '理想三相电机模型'
            ),
            
            # 功率公式
            'mechanical_power': (
                'P_mech = T × ω',
                '机械功率，T为转矩，ω为角速度',
                '适用于所有旋转电机'
            ),
            
            'power_from_torque': (
                'P = T × ω',
                '基于转矩的功率计算',
                '机械功率基本公式'
            ),
            
            'electrical_power_3phase': (
                'P_elec = √3 × U_line_rated × I_rated × cos φ',
                '三相电气功率，U_line_rated为额定线电压，I_rated为额定电流',
                '三相对称系统'
            ),
            
            'electrical_power_from_efficiency': (
                'P_elec = P_mech / η',
                '基于效率的电气功率计算',
                '需要已知效率值'
            ),
            
            'current_from_power': (
                'I_line = P / (√3 × U_line_rated × cosφ)',
                '基于功率的线电流计算',
                '三相系统，需要功率因数'
            ),
            
            'apparent_power': (
                'S = √3 × U_line_rated × I_rated',
                '三相视在功率',
                '三相对称系统'
            ),
            
            'reactive_power': (
                'Q = √(S² - P_elec²)',
                '无功功率计算',
                '基于功率三角形关系'
            ),
            
            # 电阻和电感公式
            'resistance_from_losses': (
                'R = P_cu / (3 × I²)',
                '基于铜损的电阻计算，P_cu为铜损',
                '假设三相对称'
            ),
            
            'resistance_empirical': (
                'R ≈ k / P^0.7',
                '基于功率等级的电阻经验估算',
                '经验公式，k为经验常数'
            ),
            
            'resistance_from_power': (
                'R ≈ k_R × P_rated^(-0.5)',
                '基于额定功率的电阻经验估算',
                '经验公式，k_R为电阻经验常数'
            ),
            
            'inductance_geometric': (
                'L_s ≈ μ₀ × D × l × k',
                '基于几何参数的电感估算',
                '简化模型，k为几何常数，l为铁心长度'
            ),
            
            'inductance_empirical': (
                'L ≈ L_base × (P_base/P)^0.5',
                '基于功率等级的电感经验估算',
                '经验公式，需要基准值'
            ),
            
            'inductance_from_power': (
                'L ≈ k_L × P_rated^(-0.3)',
                '基于功率等级的电感经验估算',
                '经验公式，k_L为经验常数'
            ),
            
            # 电压公式
            'phase_voltage_relationship': (
                'U_phase = U_line / √3',
                '星形连接的相电压与线电压关系（通用公式）',
                '仅适用于星形连接，U_phase和U_line可为任意对应的相电压和线电压'
            ),
            
            'line_voltage_relationship': (
                'U_line = U_phase × √3',
                '星形连接的线电压与相电压关系（通用公式）',
                '仅适用于星形连接，U_phase和U_line可为任意对应的相电压和线电压'
            ),
            
            'phase_voltage_from_flux': (
                'U_phase_back_emf = Ψ × p × ω / √2',
                '基于磁链的相反电动势计算',
                '理论计算，基于反电动势，输出为相反电动势'
            ),
            
            'rated_voltage_complex': (
                'U_phase_rated = √[(E_phase_rated+I×Z×cosφ)² + (I×Z×sinφ)²]',
                '考虑阻抗和功率因数的额定相电压',
                '精确计算，需要阻抗和功率因数，然后U_line_rated = U_phase_rated × √3'
            ),
            
            'rated_line_voltage_from_phase': (
                'U_line_rated = U_phase_rated × √3',
                '基于相电压的额定线电压计算',
                '星形连接三相系统的标准关系'
            ),
            
            'rated_voltage_simple': (
                'U_line_rated = E_line_rated + I_rated × R_est',
                '简化的额定线电压计算',
                '忽略电感，仅考虑电阻压降，端电压=反电动势+电阻压降'
            ),
            
            'rated_voltage_estimate': (
                'U_line_rated ≈ E_line_rated × 0.85',
                '额定线电压的经验估算',
                '粗略估算，0.85系数为经验值，适用范围有限，建议谨慎使用'
            ),
            
            'rated_voltage_from_current': (
                'U_line_rated = I_rated × √(R² + (ω × L)²)',
                '基于额定电流的线电压计算',
                '基于欧姆定律U=IZ，忽略反电动势，需要准确的电阻和电感值'
            ),
            
            # 电流公式
            'current_peak': (
                'I_peak = I_rated × √2',
                '峰值电流与有效值电流的关系',
                '正弦波电流'
            ),
            
            # 转动惯量公式
            'inertia_geometric': (
                'J = 0.5 × m_rotor × r²',
                '基于几何的转动惯量计算',
                '简化为实心圆柱体模型'
            ),
            
            'inertia_from_power': (
                'J = k × P_rated / ω²',
                '基于功率的转动惯量优化估算，k根据功率等级调整',
                '小功率(<1kW): k=0.015, 中功率(1-10kW): k=0.020, 大功率(>10kW): k=0.025'
            ),
            
            'inertia_from_torque': (
                'J = T_startup / α',
                '基于启动转矩的转动惯量计算，α为角加速度',
                '需要启动特性数据'
            ),
            
            # 频率和阻抗公式
            'frequency': (
                'f_e = p × n / 60',
                '电气频率计算',
                '基于极对数和转速'
            ),
            
            'reactance': (
                'XL = 2π × f_e × L',
                '感抗计算',
                '基于频率和电感'
            ),
            
            'impedance': (
                'Z = √(R² + XL²)',
                '总阻抗计算',
                '基于电阻和感抗'
            ),
            
            # 损耗和效率公式
            'copper_losses': (
                'P_cu = 3 × I² × R',
                '三相铜损计算',
                '基于电流和电阻'
            ),
            
            'total_losses_from_efficiency': (
                'P_loss = P_mech × (100-η) / η',
                '基于效率的总损耗计算',
                '需要已知效率值'
            ),
            
            'total_losses_estimate': (
                'P_loss ≈ P_cu × 1.5',
                '总损耗的经验估算',
                '假设铜损占总损耗的67%'
            ),
            
            'efficiency': (
                'η = P_mech / P_elec × 100%',
                '效率计算',
                '机械功率与电气功率的比值'
            ),
            
            # 时间常数公式
            'electrical_time_constant': (
                'τ_e = L / R',
                '电气时间常数',
                '一阶电路模型'
            ),
            
            'thermal_time_constant': (
                'τ_th ≈ C_th / G_th',
                '热时间常数，C_th为热容，G_th为热导',
                '简化热模型'
            ),
            
            # 过载公式
            'overload_current': (
                'I_overload = I_rated × k_overload',
                '过载电流，k_overload为过载倍数',
                '短时过载条件'
            ),
            
            'overload_torque': (
                'T_overload = T_rated × k_overload',
                '过载转矩，假设转矩与电流成正比',
                '短时过载条件'
            ),
            
            'overload_power': (
                'P_overload = P_rated × k_overload',
                '过载功率，假设功率与转矩成正比',
                '短时过载条件'
            ),
            
            'overload_losses': (
                'P_cu_overload = P_cu_rated × k_overload²',
                '过载铜损，与电流平方成正比',
                '主要考虑铜损增加'
            ),
            
            'overload_phase_voltage': (
                'U_phase_overload = √[(E_phase+I_overload×Z×cosφ)² + (I_overload×Z×sinφ)²]',
                '过载相电压，考虑完整阻抗压降',
                '需要阻抗和功率因数参数'
            ),
            
            'overload_line_voltage': (
                'U_line_overload = U_phase_overload × √3',
                '过载线电压，基于相电压计算',
                '星型连接三相系统'
            ),
            
            'overload_bus_voltage': (
                'U_bus_overload = (U_line_overload × √2) / 0.577',
                '过载母线电压，基于SVPWM调制',
                '考虑逆变器调制比和峰值因子'
            ),
        }
    
    @staticmethod
    def print_variable_reference():
        """
        打印变量参考表
        """
        print("电机计算变量参考表")
        print("=" * 80)
        print(f"{'变量名':<25} {'描述':<20} {'单位':<10} {'符号':<10}")
        print("-" * 80)
        
        definitions = MotorFormulas.get_variable_definitions()
        for var_name, (desc, unit, symbol) in definitions.items():
            print(f"{var_name:<25} {desc:<20} {unit:<10} {symbol:<10}")
    
    @staticmethod
    def print_formula_reference():
        """
        打印公式参考表
        """
        print("\n电机计算公式参考表")
        print("=" * 80)
        
        formulas = MotorFormulas.get_formula_definitions()
        for formula_name, (formula, description, condition) in formulas.items():
            print(f"\n【{formula_name}】")
            print(f"公式: {formula}")
            print(f"说明: {description}")
            print(f"适用条件: {condition}")
    



def main():
    """
    主函数 - 显示完整的公式参考
    """
    print("电机计算公式参考手册")
    print("=" * 80)
    print("本手册提供严谨的变量定义和公式说明，避免符号歧义")
    
    # 打印变量参考表
    MotorFormulas.print_variable_reference()
    
    # 打印公式参考表
    MotorFormulas.print_formula_reference()
    
    # 打印符号澄清说明
    MotorFormulas.print_symbol_clarification()
    
    print("\n" + "=" * 80)
    print("使用建议:")
    print("1. 在所有计算中严格按照本参考表使用变量符号")
    print("2. 功率用大写P，极对数用小写p，避免混淆")
    print("3. 电流、电压的有效值用大写，瞬时值用小写")
    print("4. 在公式显示中明确标注变量含义和单位")
    print("5. 对于容易混淆的参数，在界面中提供完整描述")

if __name__ == "__main__":
    main()
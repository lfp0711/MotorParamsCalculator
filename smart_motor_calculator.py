#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math
from flask import Request
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
import logging
from enum import StrEnum

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CalculationMethod(StrEnum):
    """计算方法枚举"""
    EMPIRICAL = "empirical"  # 经验公式
    THEORETICAL = "theoretical"  # 理论计算
    ESTIMATION = "estimation"  # 估算方法
    USER_INPUT = "user_input"  # 用户输入

class ParameterImportance(StrEnum):
    """参数重要性等级枚举"""
    CRITICAL = "critical"      # 关键参数：必须输入，无法估算
    IMPORTANT = "important"    # 重要参数：强烈建议输入，影响计算精度
    USEFUL = "useful"          # 有用参数：建议输入，提高计算可靠性
    OPTIONAL = "optional"      # 可选参数：辅助参数，用于特殊计算或验证

@dataclass
class SmartMotorParameters:
    """智能电机参数类 - 支持参数重要性分级"""
    
    # ========== 关键参数 (CRITICAL) - 必须输入 ==========
    pole_pairs: int  # 极对数 P
    rated_speed_rpm: float  # 额定转速 (r/min)
    
    # ========== 重要参数 (IMPORTANT) - 强烈建议输入 ==========
    # 至少需要以下参数中的2-3个来确保计算精度
    rated_power: Optional[float] = None  # 额定功率 (W) - 核心性能指标，GUI传入时已转换为瓦特
    rated_torque: Optional[float] = None  # 额定转矩 (Nm) - 核心性能指标
    rated_current: Optional[float] = None  # 额定电流有效值 (A) - 核心电气参数
    flux_linkage: Optional[float] = None  # 磁链 Ψ (Wb) - 核心磁路参数
    
    # ========== 有用参数 (USEFUL) - 建议输入 ==========
    # 这些参数显著影响计算精度和可靠性
    stator_resistance: Optional[float] = None  # 定子电阻 R (Ω)
    stator_inductance: Optional[float] = None  # 定子电感 L (H)
    rated_line_back_emf: Optional[float] = None  # 额定线反电动势 (V)
    rated_line_voltage: Optional[float] = None  # 额定线电压 (V)
    bus_voltage: Optional[float] = None  # 母线电压 (V)
    efficiency: Optional[float] = None  # 效率 (%)
    power_factor: Optional[float] = 0.8  # 功率因数
    
    # ========== 可选参数 (OPTIONAL) - 辅助计算 ==========
    # 机械参数
    moment_of_inertia: Optional[float] = None  # 转动惯量 (kg·m²)
    motor_mass: Optional[float] = None  # 电机质量 (kg)
    
    # 过载参数
    overload_factor: Optional[float] = None  # 过载倍数
    overload_duration: Optional[float] = None  # 过载持续时间 (s)
    
    # 几何参数（用于估算）
    stator_outer_diameter: Optional[float] = None  # 定子外径 (m)
    rotor_diameter: Optional[float] = None  # 转子直径 (m)
    stack_length: Optional[float] = None  # 铁心长度 (m)
    air_gap: Optional[float] = None  # 气隙长度 (m)
    
    # 计算方法选择
    calculation_methods: Dict[str, CalculationMethod] = field(default_factory=dict)
    
    def __init__(self, request: Request):
        data = request.get_json()
        self.rated_current = data.get('rated_current')
        # 验证必需参数
        pole_pairs_str = data.get('pole_pairs').strip()
        rated_speed_str = data.get('rated_speed_rpm').strip()
        
        if not pole_pairs_str:
            raise ValueError("极对数为必需参数，请输入有效值")
        if not rated_speed_str:
            raise ValueError("额定转速为必需参数，请输入有效值")
        
        try:
            pole_pairs = int(pole_pairs_str)
            if pole_pairs <= 0:
                raise ValueError("极对数必须为正整数")
        except ValueError:
            raise ValueError("极对数必须为有效的正整数")
        
        try:
            rated_speed_rpm = float(rated_speed_str)
            if rated_speed_rpm <= 0:
                raise ValueError("额定转速必须为正数")
        except ValueError:
            raise ValueError("额定转速必须为有效的正数")
        
        # 可选参数
        def get_optional_float(key):
            if key not in data:
                return None
            value = data.get(key).strip()
            if not value:
                return None
            try:
                result = float(value)
                if result < 0 and key in ['overload_factor', 'overload_duration', 'efficiency']:
                    raise ValueError(f"{key} 不能为负数")
                return result
            except ValueError as e:
                if "不能为负数" in str(e):
                    raise e
                raise ValueError(f"参数 {key} 的值 '{value}' 不是有效数字")
        
        # 处理功率单位转换：用户输入KW，内部计算使用W
        rated_power_kw = get_optional_float('rated_power')
        rated_power_w = rated_power_kw * 1000 if rated_power_kw is not None else None
        
        self.pole_pairs=pole_pairs
        self.rated_speed_rpm=rated_speed_rpm
        self.stator_resistance=get_optional_float('stator_resistance')
        self.stator_inductance=get_optional_float('stator_inductance')
        self.flux_linkage=get_optional_float('flux_linkage')
        self.rated_current=get_optional_float('rated_current')
        self.rated_line_back_emf=get_optional_float('rated_line_back_emf')
        self.rated_line_voltage=get_optional_float('rated_line_voltage')
        self.bus_voltage=get_optional_float('bus_voltage')
        self.rated_torque=get_optional_float('rated_torque')
        self.overload_factor=get_optional_float('overload_factor')
        self.overload_duration=get_optional_float('overload_duration')
        self.moment_of_inertia=get_optional_float('moment_of_inertia')
        self.motor_mass=get_optional_float('motor_mass')
        self.rated_power=rated_power_w
        self.power_factor=get_optional_float('power_factor')
        self.efficiency=get_optional_float('efficiency')
        self.stator_outer_diameter=get_optional_float('stator_outer_diameter')
        self.rotor_diameter=get_optional_float('rotor_diameter')
        self.stack_length=get_optional_float('stack_length')
        self.air_gap=get_optional_float('air_gap')
        
        logger.info("乾勤电机参数类初始化完成")

    @classmethod
    def get_parameter_importance(cls) -> Dict[str, ParameterImportance]:
        """获取参数重要性分级映射"""
        return {
            # 关键参数
            'pole_pairs': ParameterImportance.CRITICAL,
            'rated_speed_rpm': ParameterImportance.CRITICAL,
            
            # 重要参数
            'rated_power': ParameterImportance.IMPORTANT,
            'rated_torque': ParameterImportance.IMPORTANT,
            'rated_current': ParameterImportance.IMPORTANT,
            'flux_linkage': ParameterImportance.IMPORTANT,
            
            # 有用参数
    'stator_resistance': ParameterImportance.USEFUL,
    'stator_inductance': ParameterImportance.USEFUL,
    'rated_line_back_emf': ParameterImportance.USEFUL,
    'rated_line_voltage': ParameterImportance.USEFUL,
    'bus_voltage': ParameterImportance.USEFUL,
    'efficiency': ParameterImportance.USEFUL,
    'power_factor': ParameterImportance.USEFUL,
            
            # 可选参数
            'moment_of_inertia': ParameterImportance.OPTIONAL,
            'motor_mass': ParameterImportance.OPTIONAL,
            'overload_factor': ParameterImportance.OPTIONAL,
            'overload_duration': ParameterImportance.OPTIONAL,
            'stator_outer_diameter': ParameterImportance.OPTIONAL,
            'rotor_diameter': ParameterImportance.OPTIONAL,
            'stack_length': ParameterImportance.OPTIONAL,
            'air_gap': ParameterImportance.OPTIONAL,
        }
    
    @classmethod
    def get_parameter_groups(cls) -> Dict[str, Dict[str, str]]:
        """获取参数分组信息"""
        return {
            '🔴 关键参数': {
                'description': '必须输入的核心参数，无法通过其他参数估算',
                'recommendation': '必须提供准确值',
                'params': ['pole_pairs', 'rated_speed_rpm']
            },
            '🟠 重要参数': {
                'description': '强烈建议输入，至少需要2-3个来确保计算精度',
                'recommendation': '建议提供至少2-3个参数的准确测量值',
                'params': ['rated_power', 'rated_torque', 'rated_current', 'flux_linkage']
            },
            '🟡 有用参数': {
                'description': '显著影响计算精度和可靠性的参数',
                'recommendation': '建议提供实测值，可提高计算精度',
                'params': ['stator_resistance', 'stator_inductance', 'rated_line_back_emf', 
                          'rated_line_voltage', 'bus_voltage', 'efficiency', 'power_factor']
            },
            '🟢 可选参数': {
                'description': '辅助计算参数，用于特殊分析或验证',
                'recommendation': '根据具体需求选择性提供',
                'params': ['moment_of_inertia', 'motor_mass', 'overload_factor', 
                          'overload_duration', 'stator_outer_diameter', 'rotor_diameter', 
                          'stack_length', 'air_gap']
            }
        }

@dataclass
class CalculationResult:
    """单个参数的计算结果"""
    value: float
    method: CalculationMethod
    confidence: float  # 置信度 (0-1)
    formula: str  # 使用的公式
    notes: str = ""  # 备注

@dataclass
class SmartCalculatedResults:
    """智能计算结果类"""
    # 基本电气参数
    rated_angular_velocity: CalculationResult
    back_emf_constant: CalculationResult
    torque_constant: CalculationResult
    flux_linkage: CalculationResult
    
    # 电阻电感参数
    stator_resistance: CalculationResult
    stator_inductance: CalculationResult
    
    # 反电动势参数
    rated_phase_back_emf: CalculationResult
    rated_line_back_emf: CalculationResult
    peak_phase_back_emf: CalculationResult
    peak_line_back_emf: CalculationResult
    
    # 电压参数
    rated_line_voltage: CalculationResult
    rated_phase_voltage: CalculationResult
    peak_line_voltage: CalculationResult
    peak_phase_voltage: CalculationResult
    bus_voltage: CalculationResult
    
    # 电流参数
    rated_current: CalculationResult
    peak_current: CalculationResult
    
    # 转矩和功率参数
    rated_torque: CalculationResult
    rated_power: CalculationResult
    mechanical_power: CalculationResult
    electrical_power: CalculationResult
    
    # 转动惯量
    moment_of_inertia: CalculationResult
    
    # 频率和阻抗参数
    electrical_frequency: CalculationResult
    reactance: CalculationResult
    impedance: CalculationResult
    
    # 效率和损耗
    efficiency: CalculationResult
    total_losses: CalculationResult
    copper_losses: CalculationResult
    
    # 其他参数
    inductance_time_constant: CalculationResult
    
    # 过载参数（可选，放在最后）
    overload_current: Optional[CalculationResult] = None
    overload_torque: Optional[CalculationResult] = None
    overload_power: Optional[CalculationResult] = None
    overload_losses: Optional[CalculationResult] = None
    thermal_time_constant: Optional[CalculationResult] = None
    overload_phase_voltage: Optional[CalculationResult] = None
    overload_line_voltage: Optional[CalculationResult] = None
    overload_bus_voltage: Optional[CalculationResult] = None

class SmartMotorCalculator:
    """乾勤电机参数计算器类"""
    
    def __init__(self, motor_params: SmartMotorParameters):
        self.motor_params = motor_params
        self.results = {}
        logger.info("乾勤电机参数计算器初始化完成")
    
    def calculate_all_parameters(self) -> SmartCalculatedResults:
        """智能计算所有电机参数"""
        logger.info("开始智能计算电机参数...")
        
        # 1. 计算基本角速度（必需参数）
        angular_velocity = self._calculate_angular_velocity()
        
        # 2. 智能计算磁链
        flux_linkage = self._smart_calculate_flux_linkage(angular_velocity)
        
        # 3. 智能计算电阻和电感
        resistance = self._smart_calculate_resistance()
        inductance = self._smart_calculate_inductance()
        
        # 保存电阻和电感值用于后续计算
        self._last_resistance = resistance
        self._last_inductance = inductance
        
        # 4. 智能计算电压参数
        voltage_results = self._smart_calculate_voltages(angular_velocity, flux_linkage)
        
        # 保存电压结果用于过载计算
        self._last_voltage_results = voltage_results
        
        # 5. 智能计算电流参数
        current_results = self._smart_calculate_currents(voltage_results, resistance, inductance)
        
        # 6. 智能计算转矩和功率
        torque_power_results = self._smart_calculate_torque_power(angular_velocity, current_results)
        
        # 6.5. 补充计算电气功率（如果之前未计算）
        if torque_power_results['electrical'] is None:
            torque_power_results['electrical'] = self._calculate_electrical_power_from_voltage_current(
                voltage_results, current_results)
        
        # 7. 智能计算转动惯量
        inertia = self._smart_calculate_moment_of_inertia(torque_power_results)
        
        # 8. 计算频率和阻抗参数
        frequency_impedance_results = self._calculate_frequency_impedance(inductance, resistance)
        
        # 9. 计算效率和损耗
        efficiency_results = self._calculate_efficiency_losses(torque_power_results, current_results, resistance)
        
        # 10. 计算过载参数
        overload_results = self._calculate_overload_parameters(current_results, torque_power_results, resistance, inductance)
        
        # 11. 计算其他参数
        other_results = self._calculate_other_parameters(inductance, resistance, current_results)
        
        # 组装结果
        results = SmartCalculatedResults(
            rated_angular_velocity=angular_velocity,
            back_emf_constant=self._calculate_back_emf_constant(voltage_results, angular_velocity, flux_linkage),
            torque_constant=self._calculate_torque_constant(torque_power_results, current_results, flux_linkage),
            flux_linkage=flux_linkage,
            stator_resistance=resistance,
            stator_inductance=inductance,
            rated_phase_back_emf=voltage_results['phase_back_emf'],
            rated_line_back_emf=voltage_results['line_back_emf'],
            peak_phase_back_emf=voltage_results.get('peak_phase', CalculationResult(0, CalculationMethod.ESTIMATION, 0.0, "未计算")),
            peak_line_back_emf=voltage_results.get('peak_line', CalculationResult(0, CalculationMethod.ESTIMATION, 0.0, "未计算")),
            rated_line_voltage=voltage_results['rated_line_voltage'],
            rated_phase_voltage=voltage_results['rated_phase_voltage'],
            peak_line_voltage=voltage_results.get('peak_line_voltage', CalculationResult(0, CalculationMethod.ESTIMATION, 0.0, "未计算")),
            peak_phase_voltage=voltage_results.get('peak_phase_voltage', CalculationResult(0, CalculationMethod.ESTIMATION, 0.0, "未计算")),
            bus_voltage=voltage_results['bus'],
            rated_current=current_results['rms'],
            peak_current=current_results['peak'],
            rated_torque=torque_power_results['torque'],
            rated_power=torque_power_results['rated_power'],
            mechanical_power=torque_power_results['mechanical'],
            electrical_power=torque_power_results['electrical'],
            overload_current=overload_results.get('current'),
            overload_torque=overload_results.get('torque'),
            overload_power=overload_results.get('power'),
            overload_losses=overload_results.get('losses'),
            thermal_time_constant=overload_results.get('thermal_time_constant'),
            overload_phase_voltage=overload_results.get('overload_phase_voltage'),
            overload_line_voltage=overload_results.get('overload_line_voltage'),
            overload_bus_voltage=overload_results.get('overload_bus_voltage'),
            moment_of_inertia=inertia,
            electrical_frequency=frequency_impedance_results['frequency'],
            reactance=frequency_impedance_results['reactance'],
            impedance=frequency_impedance_results['impedance'],
            efficiency=efficiency_results['efficiency'],
            total_losses=efficiency_results['total_losses'],
            copper_losses=efficiency_results['copper_losses'],
            inductance_time_constant=other_results['time_constant']
        )
        
        logger.info("智能电机参数计算完成")
        return results
    
    def _calculate_angular_velocity(self) -> CalculationResult:
        """计算角速度"""
        value = 2 * math.pi * self.motor_params.rated_speed_rpm / 60
        return CalculationResult(
            value=value,
            method=CalculationMethod.THEORETICAL,
            confidence=1.0,
            formula="ω = 2π × n / 60",
            notes="基于额定转速的理论计算"
        )
    
    def _smart_calculate_flux_linkage(self, angular_velocity: CalculationResult) -> CalculationResult:
        """智能计算磁链"""
        if self.motor_params.flux_linkage is not None:
            return CalculationResult(
                value=self.motor_params.flux_linkage,
                method=CalculationMethod.USER_INPUT,
                confidence=1.0,
                formula="用户输入",
                notes="用户直接提供的磁链值"
            )
        
        # 方法1：基于额定线反电动势计算
        if self.motor_params.rated_line_back_emf is not None:
            phase_voltage = self.motor_params.rated_line_back_emf / math.sqrt(3)
            peak_voltage = phase_voltage * math.sqrt(2)
            flux_linkage = peak_voltage / (self.motor_params.pole_pairs * angular_velocity.value)
            return CalculationResult(
                value=flux_linkage,
                method=CalculationMethod.THEORETICAL,
                confidence=0.9,
                formula="Ψ = E_phase_peak / (p × ω)",
                notes="基于额定线反电动势的理论计算"
            )
        
        # 方法2：基于额定转矩和电流的精确计算
        if (self.motor_params.rated_torque is not None and 
            self.motor_params.rated_current is not None):
            # 完整三相电机模型：T = (3/2) × p × Ψ × I_rated
            # 解出磁链：Ψ = T / [(3/2) × p × I_rated] = (2/3) × T / (p × I_rated)
            flux_linkage = (2.0/3.0) * self.motor_params.rated_torque / (self.motor_params.pole_pairs * self.motor_params.rated_current)
            return CalculationResult(
                value=flux_linkage,
                method=CalculationMethod.THEORETICAL,
                confidence=0.8,
                formula="Ψ = (2/3) × T / (p × I_rated)",
                notes="基于完整三相电机模型的精确计算，T为电磁转矩，p为极对数，I_rated为额定电流"
            )
        
        # 方法3：基于功率和智能电流获取的改进计算
        if self.motor_params.rated_power is not None:
            # 完整三相电机模型推导：
            # T = (3/2) × p × Ψ × I_rated
            # P_rated = T × ω = (3/2) × p × Ψ × I_rated × ω
            # 解出磁链：Ψ = (2/3) × P_rated / (p × I_rated × ω)
            
            # 智能获取电流：优先使用用户输入，其次计算得出
            current_value, current_method, current_confidence, current_notes = self._get_smart_current_for_flux_calculation()
            
            if current_value is not None:
                # 使用获取到的电流计算磁链
                flux_linkage = (2.0/3.0) * self.motor_params.rated_power / (self.motor_params.pole_pairs * current_value * angular_velocity.value)
                
                return CalculationResult(
                    value=flux_linkage,
                    method=CalculationMethod.THEORETICAL,
                    confidence=current_confidence,
                    formula="Ψ = (2/3) × P_rated / (p × I_smart × ω)",
                    notes=f"使用智能电流获取策略：{current_notes}"
                )
            else:
                # 如果无法获取电流，使用传统估算方法
                # 使用用户提供的实际效率和功率因数
                pf = self.motor_params.power_factor or 0.85
                eff = (self.motor_params.efficiency or 85) / 100 if self.motor_params.efficiency else 0.85
                
                # 根据功率等级选择合适的电压等级（将KW转换为W进行判断）
                power_w = self.motor_params.rated_power  # 已经是瓦特单位
                if power_w > 50000:  # 大功率电机（>50kW）
                    typical_voltage = 690  # 高压电机
                elif power_w > 10000:  # 中功率电机（10-50kW）
                    typical_voltage = 400  # 中压电机
                else:
                    typical_voltage = 380  # 低压电机（<10kW）
                
                # 计算改进的估算电流（使用瓦特进行计算）
                estimated_current = power_w / (math.sqrt(3) * typical_voltage * eff * pf)
                
                # 计算磁链
                flux_linkage = (2.0/3.0) * self.motor_params.rated_power / (self.motor_params.pole_pairs * estimated_current * angular_velocity.value)
                
                # 提高置信度并记录使用的实际参数
                confidence = 0.75 if (self.motor_params.efficiency and self.motor_params.power_factor) else 0.6
                notes = f"基于改进估算电流计算，效率={eff:.2f}，功率因数={pf:.2f}，估算电压={typical_voltage}V"
                
                return CalculationResult(
                    value=flux_linkage,
                    method=CalculationMethod.THEORETICAL,
                    confidence=confidence,
                    formula="Ψ = (2/3) × P_rated / (p × I_improved × ω)",
                    notes=notes
                )
        
        # 基于母线电压的智能估算
        if self.motor_params.bus_voltage is not None:
            # 根据母线电压估算合理的磁链值
            # 对于低压电机，反电动势通常不超过母线电压的80%
            max_back_emf = self.motor_params.bus_voltage * 0.8
            # 相反电动势 = 磁链 × 极对数 × 角速度
            # 磁链 = 相反电动势 / (极对数 × 角速度)
            flux_linkage = max_back_emf / (self.motor_params.pole_pairs * angular_velocity.value)
            
            logger.info(f"基于母线电压{self.motor_params.bus_voltage}V估算磁链: {flux_linkage:.6f} Wb")
            return CalculationResult(
                value=flux_linkage,
                method=CalculationMethod.ESTIMATION,
                confidence=0.6,
                formula="Ψ = (U_bus × 0.8) / (p × ω)",
                notes=f"基于母线电压{self.motor_params.bus_voltage}V的智能估算，假设反电动势不超过母线电压80%"
            )
        
        # 默认估算值（仅在没有任何电压信息时使用）
        logger.warning("磁链参数不足，使用默认估算值")
        flux_linkage = 0.01  # 降低默认值，适用于小功率电机
        return CalculationResult(
            value=flux_linkage,
            method=CalculationMethod.ESTIMATION,
            confidence=0.3,
            formula="默认典型值",
            notes="缺乏足够信息，使用小功率电机典型估算值"
        )
    
    def _smart_calculate_resistance(self) -> CalculationResult:
        """智能计算定子电阻"""
        if self.motor_params.stator_resistance is not None:
            return CalculationResult(
                value=self.motor_params.stator_resistance,
                method=CalculationMethod.USER_INPUT,
                confidence=1.0,
                formula="用户输入",
                notes="用户直接提供的电阻值"
            )
        
        # 方法1：基于功率和电流估算铜损
        if (self.motor_params.rated_power is not None and 
            self.motor_params.rated_current is not None and
            self.motor_params.efficiency is not None):
            total_losses = self.motor_params.rated_power * (100 - self.motor_params.efficiency) / self.motor_params.efficiency
            copper_losses = total_losses * 0.6  # 假设铜损占总损耗的60%
            resistance = copper_losses / (3 * self.motor_params.rated_current**2)
            return CalculationResult(
                value=resistance,
                method=CalculationMethod.ESTIMATION,
                confidence=0.6,
                formula="R = P_cu / (3 × I_rated²)",
                notes="基于损耗分析的估算"
            )
        
        # 方法2：基于电机功率等级的经验公式
        if self.motor_params.rated_power is not None:
            # 经验公式：R ≈ k / P^0.7，其中k是经验常数
            k = 0.1  # 经验常数
            resistance = k / (self.motor_params.rated_power / 1000)**0.7
            return CalculationResult(
                value=resistance,
                method=CalculationMethod.EMPIRICAL,
                confidence=0.5,
                formula="R ≈ k / P^0.7",
                notes="基于功率等级的经验估算"
            )
        
        # 默认估算
        logger.warning("电阻参数不足，使用默认估算值")
        resistance = 0.002  # 典型值
        return CalculationResult(
            value=resistance,
            method=CalculationMethod.ESTIMATION,
            confidence=0.3,
            formula="默认典型值",
            notes="缺乏足够信息，使用典型估算值"
        )
    
    def _smart_calculate_inductance(self) -> CalculationResult:
        """智能计算定子电感"""
        if self.motor_params.stator_inductance is not None:
            return CalculationResult(
                value=self.motor_params.stator_inductance,
                method=CalculationMethod.USER_INPUT,
                confidence=1.0,
                formula="用户输入",
                notes="用户直接提供的电感值"
            )
        
        # 方法1：基于几何参数估算
        if (self.motor_params.stator_outer_diameter is not None and 
            self.motor_params.stack_length is not None):
            # 简化的电感估算公式
            mu0 = 4 * math.pi * 1e-7  # 真空磁导率
            D = self.motor_params.stator_outer_diameter
            L = self.motor_params.stack_length
            # 经验公式：L ≈ μ₀ × N² × A / l_mag
            # 这里使用简化估算
            inductance = mu0 * (D * L) * 1000  # 简化估算
            return CalculationResult(
                value=inductance,
                method=CalculationMethod.THEORETICAL,
                confidence=0.6,
                formula="L_s ≈ μ₀ × D × l × k",
                notes="基于几何参数的理论估算"
            )
        
        # 方法2：基于电机功率和频率的经验关系
        if self.motor_params.rated_power is not None:
            # 经验关系：电感与功率成反比
            base_inductance = 0.001  # 1kW电机的典型电感
            base_power = 1000  # 1kW
            inductance = base_inductance * (base_power / self.motor_params.rated_power)**0.5
            return CalculationResult(
                value=inductance,
                method=CalculationMethod.EMPIRICAL,
                confidence=0.5,
                formula="L ≈ L_base × (P_base/P)^0.5",
                notes="基于功率等级的经验估算"
            )
        
        # 默认估算
        logger.warning("电感参数不足，使用默认估算值")
        inductance = 0.0001  # 典型值
        return CalculationResult(
            value=inductance,
            method=CalculationMethod.ESTIMATION,
            confidence=0.3,
            formula="默认典型值",
            notes="缺乏足够信息，使用典型估算值"
        )
    
    def _smart_calculate_voltages(self, angular_velocity: CalculationResult, 
                                flux_linkage: CalculationResult) -> Dict[str, CalculationResult]:
        """智能计算电压参数"""
        results = {}
        
        # 调试信息：检查用户输入的额定线电压
        logger.info(f"用户输入的额定线电压: {self.motor_params.rated_line_voltage}")
        
        # 使用智能电压获取策略
        voltage_result = self._get_smart_voltage_for_calculation()
        if voltage_result[0] is not None:
            line_voltage = voltage_result[0]
            phase_voltage = line_voltage / math.sqrt(3)
            logger.info(f"智能获取到线电压: {line_voltage}V")
            
            results['rated_line_voltage'] = CalculationResult(
                value=line_voltage,
                method=voltage_result[1],
                confidence=voltage_result[2],
                formula="智能电压获取",
                notes=voltage_result[3]
            )
            
            results['rated_phase_voltage'] = CalculationResult(
                value=phase_voltage,
                method=CalculationMethod.THEORETICAL,
                confidence=voltage_result[2],
                formula="U_phase = U_line / √3",
                notes="基于智能获取线电压的相电压计算"
            )
            
        else:
            # 智能获取失败，基于磁链和角速度计算
            if flux_linkage.value is not None and angular_velocity.value is not None:
                peak_voltage = flux_linkage.value * self.motor_params.pole_pairs * angular_velocity.value
                phase_voltage = peak_voltage / math.sqrt(2)
                line_voltage = phase_voltage * math.sqrt(3)
                
                results['rated_line_voltage'] = CalculationResult(
                    value=line_voltage,
                    method=CalculationMethod.THEORETICAL,
                    confidence=flux_linkage.confidence * 0.8,
                    formula="U_line = Ψ × p × ω × √3 / √2",
                    notes="基于磁链和角速度的线电压计算"
                )
                
                results['rated_phase_voltage'] = CalculationResult(
                    value=phase_voltage,
                    method=CalculationMethod.THEORETICAL,
                    confidence=flux_linkage.confidence * 0.8,
                    formula="U_phase = Ψ × p × ω / √2",
                    notes="基于磁链和角速度的相电压计算"
                )
            else:
                # 如果磁链或角速度无效，使用默认估算值
                logger.warning("智能电压获取和磁链计算都失败，使用默认电压估算值")
                default_line_voltage = 400.0  # 默认线电压
                default_phase_voltage = default_line_voltage / math.sqrt(3)
                
                results['rated_line_voltage'] = CalculationResult(
                    value=default_line_voltage,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.3,
                    formula="默认典型值",
                    notes="所有计算方法失败，使用典型工业电压值"
                )
                
                results['rated_phase_voltage'] = CalculationResult(
                    value=default_phase_voltage,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.3,
                    formula="U_phase = U_line / √3",
                    notes="基于默认线电压的相电压计算"
                )
        
        # 计算反电动势（优先级：用户输入 > 基于磁链和角速度的基础物理公式 > 母线电压估算）
        # 首先检查用户是否直接输入了反电动势
        if self.motor_params.rated_line_back_emf is not None:
            # 用户直接输入了线反电动势
            rated_line_back_emf = self.motor_params.rated_line_back_emf
            rated_phase_back_emf = rated_line_back_emf / math.sqrt(3)
            
            results['line_back_emf'] = CalculationResult(
                value=rated_line_back_emf,
                method=CalculationMethod.USER_INPUT,
                confidence=1.0,
                formula="用户输入",
                notes="用户直接提供的线反电动势"
            )
            
            results['phase_back_emf'] = CalculationResult(
                value=rated_phase_back_emf,
                method=CalculationMethod.THEORETICAL,
                confidence=1.0,
                formula="E_phase = E_line / √3",
                notes="基于用户输入线反电动势计算的相反电动势"
            )
        else:
            # 检查磁链是否是基于母线电压估算的
            flux_is_bus_voltage_based = (flux_linkage.method == CalculationMethod.ESTIMATION and 
                                       "母线电压" in flux_linkage.notes)
            
            if (flux_linkage.value is not None and angular_velocity.value is not None and 
                not flux_is_bus_voltage_based):
                # 相反电动势有效值
                rated_phase_back_emf = flux_linkage.value * angular_velocity.value
                # 线反电动势有效值 = 相反电动势有效值 × √3
                rated_line_back_emf = rated_phase_back_emf * math.sqrt(3)
                
                results['phase_back_emf'] = CalculationResult(
                    value=rated_phase_back_emf,
                    method=CalculationMethod.THEORETICAL,
                    confidence=0.95,
                    formula="E_phase = Ψ × ω",
                    notes="基于磁链和角速度的理论计算（磁链非母线电压估算）"
                )
                
                results['line_back_emf'] = CalculationResult(
                    value=rated_line_back_emf,
                    method=CalculationMethod.THEORETICAL,
                    confidence=0.95,
                    formula="E_line = E_phase × √3",
                    notes="基于相反电动势的线反电动势（磁链非母线电压估算）"
                )
            elif self.motor_params.bus_voltage is not None:
                # 基于母线电压估算反电动势（作为最后的备选方案）
                estimated_line_voltage = self.motor_params.bus_voltage * 0.8
                rated_line_back_emf = estimated_line_voltage * 0.89
                rated_phase_back_emf = rated_line_back_emf / math.sqrt(3)
                
                results['phase_back_emf'] = CalculationResult(
                    value=rated_phase_back_emf,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.6,
                    formula="E_phase = (U_bus × 0.8 × 0.89) / √3",
                    notes=f"基于母线电压{self.motor_params.bus_voltage}V的估算（备选方案）"
                )
                
                results['line_back_emf'] = CalculationResult(
                    value=rated_line_back_emf,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.6,
                    formula="E_line = U_bus × 0.8 × 0.89",
                    notes=f"基于母线电压{self.motor_params.bus_voltage}V的估算（备选方案）"
                )
            else:
                # 使用默认估算值
                default_phase_emf = 100.0
                default_line_emf = default_phase_emf * math.sqrt(3)
                
                results['phase_back_emf'] = CalculationResult(
                    value=default_phase_emf,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.3,
                    formula="默认估算值",
                    notes="磁链或角速度无效时的默认估算"
                )
                
                results['line_back_emf'] = CalculationResult(
                    value=default_line_emf,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.3,
                    formula="E_line = E_phase × √3",
                    notes="基于默认相反电动势的估算"
                )
        
        # 基于额定电流计算额定线电压（仅在用户未输入额定线电压时使用）
        if (hasattr(self.motor_params, 'rated_current') and self.motor_params.rated_current is not None and 
            self.motor_params.rated_line_voltage is None):
            # 方法1：基于额定电流和阻抗计算
            rated_current = self.motor_params.rated_current
            back_emf_voltage = results['phase_back_emf'].value
            
            # 获取电阻和电感参数
            resistance_value = self.motor_params.stator_resistance if self.motor_params.stator_resistance is not None else 0.1
            inductance_value = self.motor_params.stator_inductance if self.motor_params.stator_inductance is not None else 0.001
            angular_velocity_value = angular_velocity.value
                
            # 计算阻抗
            reactance = angular_velocity_value * inductance_value
            impedance = math.sqrt(resistance_value**2 + reactance**2)
            
            # 考虑功率因数的额定相电压
            power_factor = getattr(self.motor_params, 'power_factor', 0.85)
            # 确保power_factor不为None
            if power_factor is None:
                power_factor = 0.85
            voltage_drop = rated_current * impedance
            
            # 使用向量关系计算额定线电压
            # 对于电机，端电压 = 反电动势 + 电压降（向量和）
            rated_phase = math.sqrt((back_emf_voltage + voltage_drop * power_factor)**2 + 
                                  (voltage_drop * math.sqrt(1 - power_factor**2))**2)
            
            rated_line = rated_phase * math.sqrt(3)
            
            results['rated_phase_voltage'] = CalculationResult(
                value=rated_phase,
                method=CalculationMethod.THEORETICAL,
                confidence=0.85,
                formula="U_phase_rated = √[(E_phase_rated+I_rated×Z×cosφ)² + (I_rated×Z×sinφ)²]",
                notes="基于额定电流和阻抗的相电压理论计算"
            )
            
            results['rated_line_voltage'] = CalculationResult(
                value=rated_line,
                method=CalculationMethod.THEORETICAL,
                confidence=0.85,
                formula="U_line_rated = U_phase_rated × √3",
                notes="基于额定相电压计算"
            )
        elif (self.motor_params.rated_line_voltage is None and 
              'rated_line_voltage' not in results):
            # 当没有额定电流且用户未输入额定线电压，且之前智能获取策略未得到线电压时，使用反电动势作为额定线电压的基础值
            if ('line_back_emf' in results and 'phase_back_emf' in results and 
                results['line_back_emf'].value is not None and results['phase_back_emf'].value is not None):
                # 对于永磁同步电机，额定电压应该大于反电动势以克服阻抗压降
                # 估算压降约为反电动势的10-15%
                voltage_margin = 1.12  # 考虑阻抗压降的裕量
                rated_line = results['line_back_emf'].value * voltage_margin
                rated_phase = results['phase_back_emf'].value * voltage_margin
                
                results['rated_line_voltage'] = CalculationResult(
                    value=rated_line,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.7,
                    formula="U_rated_line ≈ E_line × 1.12",
                    notes="无额定电流时基于反电动势的估算，考虑阻抗压降"
                )
                
                results['rated_phase_voltage'] = CalculationResult(
                    value=rated_phase,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.7,
                    formula="U_rated_phase ≈ E_phase × 1.12",
                    notes="无额定电流时基于反电动势的估算，考虑阻抗压降"
                )
            else:
                # 如果反电动势计算失败，使用默认估算值
                logger.warning("反电动势计算失败，使用默认电压估算值")
                default_line_voltage = 400.0  # 默认线电压
                default_phase_voltage = default_line_voltage / math.sqrt(3)
                
                results['rated_line_voltage'] = CalculationResult(
                    value=default_line_voltage,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.3,
                    formula="默认典型值",
                    notes="反电动势计算失败，使用典型工业电压值"
                )
                
                results['rated_phase_voltage'] = CalculationResult(
                    value=default_phase_voltage,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.3,
                    formula="U_phase = U_line / √3",
                    notes="基于默认线电压的相电压计算"
                )
        
        # 计算母线电压
        if self.motor_params.bus_voltage is not None:
            # 用户提供母线电压
            results['bus'] = CalculationResult(
                value=self.motor_params.bus_voltage,
                method=CalculationMethod.USER_INPUT,
                confidence=1.0,
                formula="用户输入",
                notes="用户提供的母线电压"
            )
        else:
            # 基于额定线电压估算母线电压（使用峰值）
            if 'rated_line_voltage' in results:
                # 母线电压 = 线电压峰值 / 调制比
                # 线电压峰值 = 线电压有效值 × √2
                line_voltage_peak = results['rated_line_voltage'].value * math.sqrt(2)
                estimated_bus_voltage = line_voltage_peak / 0.577  # SVPWM调制比
                results['bus'] = CalculationResult(
                    value=estimated_bus_voltage,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.7,
                    formula="U_bus ≈ (U_line × √2) / 0.577",
                    notes="基于线电压峰值估算母线电压，考虑SVPWM调制比"
                )
        
        return results
    
    def _smart_calculate_currents(self, voltage_results: Dict[str, CalculationResult],
                                resistance: CalculationResult, 
                                inductance: CalculationResult) -> Dict[str, CalculationResult]:
        """智能计算电流参数"""
        results = {}
        
        # 使用新的智能电流获取方法
        current_value, method, confidence, notes = self._get_smart_current_for_flux_calculation()
        
        if current_value is not None:
            results['rms'] = CalculationResult(
                value=current_value,
                method=method,
                confidence=confidence,
                formula="智能参数检查",
                notes=notes
            )
        else:
            # 如果智能方法无法获取电流，尝试基于电压和功率计算
            if (self.motor_params.rated_power is not None and 
                'rated_line_voltage' in voltage_results and 
                voltage_results['rated_line_voltage'].value is not None):
                
                pf = self.motor_params.power_factor or 0.8
                eff = self.motor_params.efficiency or 90
                electrical_power = self.motor_params.rated_power / (eff / 100)
                
                current_rms = electrical_power / (math.sqrt(3) * voltage_results['rated_line_voltage'].value * pf)
                results['rms'] = CalculationResult(
                    value=current_rms,
                    method=CalculationMethod.THEORETICAL,
                    confidence=0.7,
                    formula="I_rated = P_rated / (√3 × U_line_rated × cosφ)",
                    notes="基于功率和电压的电流计算"
                )
            else:
                # 默认估算
                current_rms = 100  # 典型值
                results['rms'] = CalculationResult(
                    value=current_rms,
                    method=CalculationMethod.ESTIMATION,
                    confidence=0.3,
                    formula="默认估算",
                    notes="缺乏信息，使用典型值"
                )
        
        # 计算峰值电流
        current_peak = results['rms'].value * math.sqrt(2)
        results['peak'] = CalculationResult(
            value=current_peak,
            method=CalculationMethod.THEORETICAL,
            confidence=results['rms'].confidence,
            formula="I_peak = I_rated × √2",
            notes="基于有效值的峰值电流"
        )
        
        return results
    
    def _get_smart_current_for_flux_calculation(self) -> tuple:
        """智能获取电流用于磁链计算
        
        返回: (current_value, method, confidence, notes)
        按优先级检查：
        1. 用户直接输入的额定电流
        2. 通过额定线电压和功率计算的电流
        3. 通过额定线反电动势和功率计算的电流
        4. 通过母线电压和功率计算的电流
        """
        
        # 优先级1：用户直接输入的额定电流
        if self.motor_params.rated_current is not None:
            return (
                self.motor_params.rated_current,
                CalculationMethod.USER_INPUT,
                1.0,
                "用户直接输入的额定电流"
            )
        
        # 如果没有直接输入电流，检查是否可以通过电压和功率计算
        if self.motor_params.rated_power is not None:
            pf = self.motor_params.power_factor or 0.85
            eff = (self.motor_params.efficiency or 85) / 100 if self.motor_params.efficiency else 0.85
            power_w = self.motor_params.rated_power  # 已经是瓦特单位
            
            # 优先级2：通过用户输入的额定线电压计算电流
            if self.motor_params.rated_line_voltage is not None:
                current = power_w / (math.sqrt(3) * self.motor_params.rated_line_voltage * eff * pf)
                return (
                    current,
                    CalculationMethod.THEORETICAL,
                    0.9,
                    f"通过用户输入的额定线电压{self.motor_params.rated_line_voltage}V计算得出"
                )
            
            # 优先级3：通过用户输入的母线电压计算电流
            if self.motor_params.bus_voltage is not None:
                # 使用SVPWM调制比：线电压峰值 = 母线电压 × 0.577，线电压有效值 = 峰值 / √2
                estimated_voltage = self.motor_params.bus_voltage * 0.577 / math.sqrt(2)
                current = power_w / (math.sqrt(3) * estimated_voltage * eff * pf)
                return (
                    current,
                    CalculationMethod.THEORETICAL,
                    0.7,
                    f"通过用户输入的母线电压{self.motor_params.bus_voltage}V推算线电压后计算得出"
                )

            # 优先级4：通过用户输入的额定线反电动势计算电流
            if self.motor_params.rated_line_back_emf is not None:
                # 假设反电动势约为额定电压的89%
                estimated_voltage = self.motor_params.rated_line_back_emf / 0.89
                current = power_w / (math.sqrt(3) * estimated_voltage * eff * pf)
                return (
                    current,
                    CalculationMethod.THEORETICAL,
                    0.8,
                    f"通过用户输入的额定线反电动势{self.motor_params.rated_line_back_emf}V推算电压后计算得出"
                )
            

        
        # 如果都无法获取，返回None
        return (None, None, 0.0, "无法获取有效的电流信息")
    
    def _get_smart_voltage_for_calculation(self) -> tuple:
        """智能获取电压用于计算
        
        返回: (voltage_value, method, confidence, notes)
        按优先级检查：
        1. 用户直接输入的额定线电压
        2. 通过额定线反电动势推算的线电压
        3. 通过母线电压推算的线电压
        4. 通过磁链和角速度计算的电压
        """
        
        # 优先级1：用户直接输入的额定线电压
        if self.motor_params.rated_line_voltage is not None:
            return (
                self.motor_params.rated_line_voltage,
                CalculationMethod.USER_INPUT,
                1.0,
                "用户直接输入的额定线电压"
            )
        
        # 优先级2：通过用户输入的额定线反电动势推算电压
        if self.motor_params.rated_line_back_emf is not None:
            # 假设反电动势约为额定电压的89%
            estimated_voltage = self.motor_params.rated_line_back_emf / 0.89
            return (
                estimated_voltage,
                CalculationMethod.THEORETICAL,
                0.9,
                f"通过用户输入的额定线反电动势{self.motor_params.rated_line_back_emf}V推算得出"
            )
        
        # 优先级3：通过用户输入的母线电压推算线电压
        if self.motor_params.bus_voltage is not None:
            # 使用SVPWM调制比：线电压峰值 = 母线电压 × 0.577，线电压有效值 = 峰值 / √2
            estimated_voltage = self.motor_params.bus_voltage * 0.577 / math.sqrt(2)
            return (
                estimated_voltage,
                CalculationMethod.THEORETICAL,
                0.8,
                f"通过用户输入的母线电压{self.motor_params.bus_voltage}V推算得出"
            )
        
        # 优先级4：通过磁链和角速度计算电压（需要这些参数可用）
        if (self.motor_params.flux_linkage is not None and 
            self.motor_params.rated_speed_rpm is not None):
            
            angular_velocity = (self.motor_params.rated_speed_rpm * 2 * math.pi) / 60
            peak_voltage = self.motor_params.flux_linkage * self.motor_params.pole_pairs * angular_velocity
            phase_voltage = peak_voltage / math.sqrt(2)
            line_voltage = phase_voltage * math.sqrt(3)
            
            return (
                line_voltage,
                CalculationMethod.THEORETICAL,
                0.7,
                f"通过磁链{self.motor_params.flux_linkage}Wb和转速计算得出"
            )
        
        # 如果都无法获取，返回None
        return (None, None, 0.0, "无法获取有效的电压信息")
    
    def _get_smart_parameter(self, param_name: str, calculation_strategies: List[callable]) -> tuple:
        """通用的智能参数获取机制
        
        Args:
            param_name: 参数名称
            calculation_strategies: 计算策略列表，按优先级排序
            
        返回: (value, method, confidence, notes)
        """
        for strategy in calculation_strategies:
            try:
                result = strategy()
                if result[0] is not None:
                    return result
            except Exception as e:
                logger.warning(f"参数{param_name}的计算策略失败: {e}")
                continue
        
        return (None, None, 0.0, f"无法获取有效的{param_name}信息")
    
    def _get_smart_power_for_calculation(self) -> tuple:
        """智能获取功率用于计算
        
        返回: (power_value, method, confidence, notes)
        按优先级检查：
        1. 用户直接输入的额定功率
        2. 通过转矩和转速计算的功率
        3. 通过电压、电流和功率因数计算的功率
        """
        
        # 优先级1：用户直接输入的额定功率
        if self.motor_params.rated_power is not None:
            return (
                self.motor_params.rated_power,
                CalculationMethod.USER_INPUT,
                1.0,
                "用户直接输入的额定功率"
            )
        
        # 优先级2：通过转矩和转速计算功率
        if (self.motor_params.rated_torque is not None and 
            self.motor_params.rated_speed_rpm is not None):
            
            angular_velocity = (self.motor_params.rated_speed_rpm * 2 * math.pi) / 60
            power = (self.motor_params.rated_torque * angular_velocity) / 1000  # 转换为kW
            
            return (
                power,
                CalculationMethod.THEORETICAL,
                0.9,
                f"通过转矩{self.motor_params.rated_torque}Nm和转速计算得出"
            )
        
        # 优先级3：通过电压、电流和功率因数计算功率
        if (self.motor_params.rated_current is not None and 
            self.motor_params.rated_line_voltage is not None):
            
            pf = self.motor_params.power_factor or 0.85
            eff = (self.motor_params.efficiency or 85) / 100 if self.motor_params.efficiency else 0.85
            
            electrical_power = (math.sqrt(3) * self.motor_params.rated_line_voltage * 
                              self.motor_params.rated_current * pf) / 1000  # 转换为kW
            mechanical_power = electrical_power * eff
            
            return (
                mechanical_power,
                CalculationMethod.THEORETICAL,
                0.8,
                f"通过电压{self.motor_params.rated_line_voltage}V和电流{self.motor_params.rated_current}A计算得出"
            )
        
        # 如果都无法获取，返回None
        return (None, None, 0.0, "无法获取有效的功率信息")
    
    def _get_smart_torque_for_calculation(self) -> tuple:
        """智能获取转矩用于计算
        
        返回: (torque_value, method, confidence, notes)
        按优先级检查：
        1. 用户直接输入的额定转矩
        2. 通过功率和转速计算的转矩
        3. 通过磁链、极对数和电流计算的转矩
        """
        
        # 优先级1：用户直接输入的额定转矩
        if self.motor_params.rated_torque is not None:
            return (
                self.motor_params.rated_torque,
                CalculationMethod.USER_INPUT,
                1.0,
                "用户直接输入的额定转矩"
            )
        
        # 优先级2：通过功率和转速计算转矩
        if (self.motor_params.rated_power is not None and 
            self.motor_params.rated_speed_rpm is not None):
            
            angular_velocity = (self.motor_params.rated_speed_rpm * 2 * math.pi) / 60
            torque = self.motor_params.rated_power / angular_velocity  # 功率已经是瓦特单位
            
            return (
                torque,
                CalculationMethod.THEORETICAL,
                0.9,
                f"通过功率{self.motor_params.rated_power}kW和转速计算得出"
            )
        
        # 优先级3：通过磁链、极对数和电流计算转矩
        if (self.motor_params.flux_linkage is not None and 
            self.motor_params.rated_current is not None):
            
            # T = (3/2) × p × Ψ × I
            torque = (3.0/2.0) * self.motor_params.pole_pairs * self.motor_params.flux_linkage * self.motor_params.rated_current
            
            return (
                torque,
                CalculationMethod.THEORETICAL,
                0.8,
                f"通过磁链{self.motor_params.flux_linkage}Wb和电流{self.motor_params.rated_current}A计算得出"
            )
        
        # 如果都无法获取，返回None
        return (None, None, 0.0, "无法获取有效的转矩信息")
    
    def _smart_calculate_torque_power(self, angular_velocity: CalculationResult,
                                    current_results: Dict[str, CalculationResult]) -> Dict[str, CalculationResult]:
        """智能计算转矩和功率参数"""
        results = {}
        
        # 使用智能转矩获取策略
        torque_value, torque_method, torque_confidence, torque_notes = self._get_smart_torque_for_calculation()
        
        if torque_value is not None:
            results['torque'] = CalculationResult(
                value=torque_value,
                method=torque_method,
                confidence=torque_confidence,
                formula="智能参数检查",
                notes=torque_notes
            )
        else:
            # 如果智能方法无法获取转矩，使用默认估算
            torque = 50  # 默认值
            results['torque'] = CalculationResult(
                value=torque,
                method=CalculationMethod.ESTIMATION,
                confidence=0.3,
                formula="默认估算",
                notes="缺乏信息，使用典型值"
            )
        
        # 使用智能功率获取策略
        power_value, power_method, power_confidence, power_notes = self._get_smart_power_for_calculation()
        
        if power_value is not None:
            results['rated_power'] = CalculationResult(
                value=power_value,
                method=power_method,
                confidence=power_confidence,
                formula="智能参数检查",
                notes=power_notes
            )
        else:
            # 如果智能方法无法获取功率，基于转矩计算功率
            power = results['torque'].value * angular_velocity.value
            results['rated_power'] = CalculationResult(
                value=power,
                method=CalculationMethod.THEORETICAL,
                confidence=results['torque'].confidence,
                formula="P = T × ω",
                notes="基于转矩的功率计算"
            )
        
        # 机械功率（等于额定功率）
        results['mechanical'] = results['rated_power']
        
        # 电气功率计算
        if self.motor_params.efficiency is not None:
            # 有效率时，基于效率计算
            electrical_power = results['rated_power'].value / (self.motor_params.efficiency / 100)
            results['electrical'] = CalculationResult(
                value=electrical_power,
                method=CalculationMethod.THEORETICAL,
                confidence=0.9,
                formula="P_elec = P_mech / η",
                notes="基于效率的电气功率计算"
            )
        else:
            # 无效率时，尝试通过电压、电流、功率因数计算
            # 这需要在电流计算完成后进行，暂时先设置为None
            results['electrical'] = None
        
        return results
    
    def _calculate_electrical_power_from_voltage_current(self, voltage_results: Dict[str, CalculationResult],
                                                       current_results: Dict[str, CalculationResult]) -> CalculationResult:
        """通过电压、电流和功率因数计算电气功率"""
        try:
            # 获取线电压和电流
            line_voltage = voltage_results['rated_line_voltage'].value
            current = current_results['rms'].value
            
            # 获取功率因数
            power_factor = getattr(self.motor_params, 'power_factor', 0.85)
            if power_factor is None:
                power_factor = 0.85
            
            # 计算三相电气功率: P = √3 × U_line × I × cosφ
            electrical_power = math.sqrt(3) * line_voltage * current * power_factor
            
            return CalculationResult(
                value=electrical_power,
                method=CalculationMethod.THEORETICAL,
                confidence=0.8,
                formula="P_elec = √3 × U_line × I × cosφ",
                notes="基于电压、电流和功率因数的电气功率计算"
            )
        except Exception as e:
            logger.warning(f"电气功率计算失败: {e}，使用默认估算")
            # 如果计算失败，返回基于机械功率的估算
            mechanical_power = self.motor_params.rated_power or 185000
            estimated_electrical_power = mechanical_power / 0.9  # 假设90%效率
            
            return CalculationResult(
                value=estimated_electrical_power,
                method=CalculationMethod.ESTIMATION,
                confidence=0.5,
                formula="P_elec ≈ P_mech / 0.9",
                notes="电气功率估算（假设90%效率）"
            )
    
    def _smart_calculate_moment_of_inertia(self, torque_power_results: Dict[str, CalculationResult]) -> CalculationResult:
        """智能计算转动惯量"""
        if self.motor_params.moment_of_inertia is not None:
            return CalculationResult(
                value=self.motor_params.moment_of_inertia,
                method=CalculationMethod.USER_INPUT,
                confidence=1.0,
                formula="用户输入",
                notes="用户提供的转动惯量"
            )
        
        # 方法1：基于几何参数估算
        if (self.motor_params.rotor_diameter is not None and 
            self.motor_params.stack_length is not None and
            self.motor_params.motor_mass is not None):
            # 简化为实心圆柱体：J = 0.5 × m × r²
            radius = self.motor_params.rotor_diameter / 2
            # 假设转子质量为总质量的60%
            rotor_mass = self.motor_params.motor_mass * 0.6
            inertia = 0.5 * rotor_mass * radius**2
            return CalculationResult(
                value=inertia,
                method=CalculationMethod.THEORETICAL,
                confidence=0.7,
                formula="J = 0.5 × m_rotor × r²",
                notes="基于几何参数的理论计算"
            )
        
        # 方法2：基于功率和转速的优化估算
        if self.motor_params.rated_power is not None:
            # 优化的经验公式：考虑电机类型和功率等级
            # 小功率电机 (<1kW): k = 0.015
            # 中功率电机 (1-10kW): k = 0.020  
            # 大功率电机 (>10kW): k = 0.025
            if self.motor_params.rated_power < 1000:
                k = 0.015
                power_category = "小功率"
            elif self.motor_params.rated_power < 10000:
                k = 0.020
                power_category = "中功率"
            else:
                k = 0.025
                power_category = "大功率"
            
            omega = 2 * math.pi * self.motor_params.rated_speed_rpm / 60
            # 基于旋转动能关系：E_kinetic = (1/2) × J × ω²
            # 经验关系：J ≈ k × P_rated / ω²
            inertia = k * self.motor_params.rated_power / (omega**2)
            return CalculationResult(
                value=inertia,
                method=CalculationMethod.EMPIRICAL,
                confidence=0.6,
                formula=f"J = {k} × P_rated / ω²",
                notes=f"基于{power_category}电机的优化经验公式，考虑功率等级影响"
            )
        
        # 方法3：基于转矩的估算
        if torque_power_results.get('torque'):
            # 假设启动时间和加速度
            startup_time = 2.0  # 假设2秒启动时间
            omega = 2 * math.pi * self.motor_params.rated_speed_rpm / 60
            angular_acceleration = omega / startup_time
            # T = J × α，假设启动转矩为额定转矩的1.5倍
            startup_torque = torque_power_results['torque'].value * 1.5
            inertia = startup_torque / angular_acceleration
            return CalculationResult(
                value=inertia,
                method=CalculationMethod.ESTIMATION,
                confidence=0.4,
                formula="J = T_startup / α",
                notes="基于启动特性的估算"
            )
        
        # 默认估算
        logger.warning("转动惯量参数不足，使用默认估算值")
        inertia = 0.01  # 典型值
        return CalculationResult(
            value=inertia,
            method=CalculationMethod.ESTIMATION,
            confidence=0.3,
            formula="默认典型值",
            notes="缺乏足够信息，使用典型估算值"
        )
    
    def _calculate_frequency_impedance(self, inductance: CalculationResult, 
                                     resistance: CalculationResult) -> Dict[str, CalculationResult]:
        """计算频率和阻抗参数"""
        results = {}
        
        # 电气频率
        frequency = self.motor_params.pole_pairs * self.motor_params.rated_speed_rpm / 60
        results['frequency'] = CalculationResult(
            value=frequency,
            method=CalculationMethod.THEORETICAL,
            confidence=1.0,
            formula="f = p × n / 60",
            notes="基于极对数p和转速n的理论计算"
        )
        
        # 感抗
        reactance = 2 * math.pi * frequency * inductance.value
        results['reactance'] = CalculationResult(
            value=reactance,
            method=CalculationMethod.THEORETICAL,
            confidence=inductance.confidence,
            formula="XL = 2π × f × L",
            notes="基于频率和电感的感抗计算"
        )
        
        # 总阻抗
        impedance = math.sqrt(resistance.value**2 + reactance**2)
        results['impedance'] = CalculationResult(
            value=impedance,
            method=CalculationMethod.THEORETICAL,
            confidence=min(resistance.confidence, inductance.confidence),
            formula="Z = √(R² + XL²)",
            notes="基于电阻和感抗的总阻抗"
        )
        
        return results
    
    def _calculate_efficiency_losses(self, torque_power_results: Dict[str, CalculationResult],
                                   current_results: Dict[str, CalculationResult],
                                   resistance: CalculationResult) -> Dict[str, CalculationResult]:
        """计算效率和损耗"""
        results = {}
        
        # 铜损耗
        copper_losses = 3 * current_results['rms'].value**2 * resistance.value
        results['copper_losses'] = CalculationResult(
            value=copper_losses,
            method=CalculationMethod.THEORETICAL,
            confidence=min(current_results['rms'].confidence, resistance.confidence),
            formula="P_cu = 3 × I_rated² × R",
            notes="基于电流和电阻的铜损计算"
        )
        
        # 总损耗
        if self.motor_params.efficiency is not None:
            mechanical_power = torque_power_results['mechanical'].value
            total_losses = mechanical_power * (100 - self.motor_params.efficiency) / self.motor_params.efficiency
            results['total_losses'] = CalculationResult(
                value=total_losses,
                method=CalculationMethod.THEORETICAL,
                confidence=0.8,
                formula="P_loss = P_mech × (100-η) / η",
                notes="基于效率的总损耗计算"
            )
        else:
            # 估算总损耗为铜损的1.5倍
            total_losses = copper_losses * 1.5
            results['total_losses'] = CalculationResult(
                value=total_losses,
                method=CalculationMethod.ESTIMATION,
                confidence=0.5,
                formula="P_loss ≈ P_cu × 1.5",
                notes="基于铜损的总损耗估算"
            )
        
        # 效率
        if self.motor_params.efficiency is not None:
            results['efficiency'] = CalculationResult(
                value=self.motor_params.efficiency,
                method=CalculationMethod.USER_INPUT,
                confidence=1.0,
                formula="用户输入",
                notes="用户提供的效率值"
            )
        else:
            mechanical_power = torque_power_results['mechanical'].value
            electrical_power = mechanical_power + results['total_losses'].value
            efficiency = (mechanical_power / electrical_power) * 100
            results['efficiency'] = CalculationResult(
                value=efficiency,
                method=CalculationMethod.THEORETICAL,
                confidence=0.7,
                formula="η = P_mech / P_elec × 100%",
                notes="基于功率的效率计算"
            )
        
        return results
    
    def _calculate_other_parameters(self, inductance: CalculationResult, 
                                  resistance: CalculationResult,
                                  current_results: Dict[str, CalculationResult]) -> Dict[str, CalculationResult]:
        """计算其他参数"""
        results = {}
        
        # 电感时间常数
        time_constant = inductance.value / resistance.value
        results['time_constant'] = CalculationResult(
            value=time_constant,
            method=CalculationMethod.THEORETICAL,
            confidence=min(inductance.confidence, resistance.confidence),
            formula="τ = L / R",
            notes="电感时间常数"
        )
        
        return results
    
    def _calculate_back_emf_constant(self, voltage_results: Dict[str, CalculationResult],
                                   angular_velocity: CalculationResult,
                                   flux_linkage: CalculationResult) -> CalculationResult:
        """
        计算反电动势常数 Ke
        
        完整定义式和物理模型：
        
        1. 基本定义：
           Ke = E / ω (反电动势/角速度)
           
        2. 基于磁链的理论公式：
           - 相反电动势：E_phase = Ψ × p × ω
           - 线反电动势：E_line = √3 × Ψ × p × ω
           - 相反电动势常数：Ke_phase = Ψ × p
           - 线反电动势常数：Ke_line = √3 × Ψ × p
           
        3. 与转矩常数的关系：
           - Kt = (3/2) × p × Ψ (完整三相电机模型)
           - Ke = p × Ψ (相反电动势常数)
           - 理论比值：Kt/Ke = 1.5
           
        4. 单位：
           - Ke: V·s/rad 或 V/(rad/s)
           - 工程单位：V·min/r (需要转换系数)
        """
        
        # 方法1：基于磁链的理论计算（推荐）
        if flux_linkage.confidence >= 0.5:
            # 计算相反电动势常数（基于相电压）
            ke_phase = flux_linkage.value * self.motor_params.pole_pairs
            return CalculationResult(
                value=ke_phase,
                method=CalculationMethod.THEORETICAL,
                confidence=flux_linkage.confidence,
                formula="Ke = Ψ × P",
                notes="基于磁链的相反电动势常数，完整三相电机模型"
            )
        
        # 方法2：基于空载电压计算
        peak_voltage = voltage_results['phase_back_emf'].value * math.sqrt(2)
        ke = peak_voltage / angular_velocity.value
        return CalculationResult(
            value=ke,
            method=CalculationMethod.THEORETICAL,
            confidence=voltage_results['phase_back_emf'].confidence,
            formula="Ke = E_phase_peak / ω",
            notes="基于空载相电压的反电动势常数"
        )
    
    def _calculate_torque_constant(self, torque_power_results: Dict[str, CalculationResult],
                                 current_results: Dict[str, CalculationResult],
                                 flux_linkage: CalculationResult) -> CalculationResult:
        """
        计算转矩常数 Kt
        
        完整定义式和物理模型：
        
        1. 基本定义：
           Kt = T_rated / I_rated (转矩/电流)
           
        2. 基于磁链的理论公式：
           - 永磁同步电机转矩方程：T = (3/2) × p × Ψ × I_q
           - 对于正弦波驱动：I_q ≈ I_rated
           - 转矩常数：Kt = (3/2) × p × Ψ
           
        3. 与反电动势常数的关系：
           - Ke = p × Ψ (相反电动势常数)
           - Kt = (3/2) × p × Ψ = 1.5 × Ke
           - 理论比值：Kt/Ke = 1.5
           
        4. 单位：
           - Kt: N·m/A (牛顿米/安培)
           - 工程单位：oz·in/A, kg·cm/A 等
           
        5. 物理意义：
           - 表示单位电流产生的转矩大小
           - 是电机转矩性能的重要指标
        """
        
        # 方法1：基于磁链的理论计算（推荐）
        if flux_linkage.confidence >= 0.5:
            # 完整物理模型：Kt = (3/2) × P × Ψ
            kt_full = 1.5 * self.motor_params.pole_pairs * flux_linkage.value
            
            return CalculationResult(
                value=kt_full,
                method=CalculationMethod.THEORETICAL,
                confidence=flux_linkage.confidence,
                formula="Kt = (3/2) × p × Ψ",
                notes="基于磁链的完整三相电机模型转矩常数"
            )
        
        # 方法2：基于转矩和电流的直接计算
        kt = torque_power_results['torque'].value / current_results['rms'].value
        confidence = min(torque_power_results['torque'].confidence, current_results['rms'].confidence)
        return CalculationResult(
            value=kt,
            method=CalculationMethod.THEORETICAL,
            confidence=confidence,
            formula="Kt = T_rated / I_rated",
            notes="基于额定转矩和电流的转矩常数"
        )
    
    def _calculate_overload_parameters(self, current_results: Dict[str, CalculationResult],
                                     torque_power_results: Dict[str, CalculationResult],
                                     resistance: CalculationResult,
                                     inductance: CalculationResult) -> Dict[str, CalculationResult]:
        """计算过载参数"""
        results = {}
        
        if self.motor_params.overload_factor is None:
            return results
        
        overload_factor = self.motor_params.overload_factor
        
        # 过载电流
        overload_current = current_results['rms'].value * overload_factor
        results['current'] = CalculationResult(
            value=overload_current,
            method=CalculationMethod.THEORETICAL,
            confidence=current_results['rms'].confidence,
            formula=f"I_overload = I_rated × {overload_factor}",
            notes=f"{overload_factor}倍过载电流"
        )
        
        # 过载转矩（假设转矩与电流成正比）
        overload_torque = torque_power_results['torque'].value * overload_factor
        results['torque'] = CalculationResult(
            value=overload_torque,
            method=CalculationMethod.THEORETICAL,
            confidence=torque_power_results['torque'].confidence,
            formula=f"T_overload = T_rated × {overload_factor}",
            notes=f"{overload_factor}倍过载转矩"
        )
        
        # 过载功率（假设功率与转矩成正比）
        overload_power = torque_power_results['rated_power'].value * overload_factor
        results['power'] = CalculationResult(
            value=overload_power,
            method=CalculationMethod.THEORETICAL,
            confidence=torque_power_results['rated_power'].confidence,
            formula=f"P_overload = P_rated × {overload_factor}",
            notes=f"{overload_factor}倍过载功率"
        )
        
        # 过载损耗（铜损与电流平方成正比）
        copper_losses_rated = 3 * resistance.value * (current_results['rms'].value ** 2)
        overload_copper_losses = 3 * resistance.value * (overload_current ** 2)
        results['losses'] = CalculationResult(
            value=overload_copper_losses,
            method=CalculationMethod.THEORETICAL,
            confidence=min(resistance.confidence, current_results['rms'].confidence),
            formula=f"P_cu_overload = 3 × R × I_overload²",
            notes=f"过载铜损，为额定铜损的{overload_factor**2:.1f}倍"
        )
        
        # 过载时的电压计算（考虑完整阻抗）
        if hasattr(self, '_last_voltage_results') and self._last_voltage_results:
            # 计算过载时的阻抗和电压降
            angular_velocity_value = self._calculate_angular_velocity().value
            reactance = angular_velocity_value * inductance.value
            impedance = math.sqrt(resistance.value**2 + reactance**2)
            voltage_drop_overload = overload_current * impedance
            
            # 过载相电压（反电动势 + 阻抗压降的向量和）
            # 过载时需要更高的端电压来克服更大的阻抗压降
            if 'phase_back_emf' in self._last_voltage_results:
                back_emf_phase = self._last_voltage_results['phase_back_emf'].value
                power_factor = getattr(self.motor_params, 'power_factor', 0.85)
                # 确保power_factor不为None
                if power_factor is None:
                    power_factor = 0.85
                
                # 使用向量关系计算过载电压
                overload_phase_voltage = math.sqrt(
                    (back_emf_phase + voltage_drop_overload * power_factor)**2 + 
                    (voltage_drop_overload * math.sqrt(1 - power_factor**2))**2
                )
                
                results['overload_phase_voltage'] = CalculationResult(
                    value=overload_phase_voltage,
                    method=CalculationMethod.THEORETICAL,
                    confidence=min(resistance.confidence, inductance.confidence, current_results['rms'].confidence),
                    formula="U_phase_overload = √[(E_phase+I_overload×Z×cosφ)² + (I_overload×Z×sinφ)²]",
                    notes=f"过载时相电压，考虑{overload_factor}倍电流的完整阻抗压降"
                )
                
                # 过载线电压
                overload_line_voltage = overload_phase_voltage * math.sqrt(3)
                results['overload_line_voltage'] = CalculationResult(
                    value=overload_line_voltage,
                    method=CalculationMethod.THEORETICAL,
                    confidence=min(resistance.confidence, current_results['rms'].confidence),
                    formula="U_line_overload = U_phase_overload × √3",
                    notes=f"过载时线电压"
                )
                
                # 所需母线电压（使用线电压峰值）
                overload_line_voltage_peak = overload_line_voltage * math.sqrt(2)
                required_bus_voltage = overload_line_voltage_peak / 0.577
                results['overload_bus_voltage'] = CalculationResult(
                    value=required_bus_voltage,
                    method=CalculationMethod.THEORETICAL,
                    confidence=min(resistance.confidence, current_results['rms'].confidence),
                    formula="U_bus_overload = (U_line_overload × √2) / 0.577",
                    notes=f"过载时所需母线电压，基于线电压峰值和SVPWM调制比"
                )
        
        # 热时间常数估算
        if self.motor_params.motor_mass is not None:
            # 简化热模型：τ_th = C_th / G_th
            # 假设热容量与质量成正比，散热系数为常数
            thermal_capacity = self.motor_params.motor_mass * 900  # J/K，假设比热容900 J/(kg·K)
            thermal_conductance = 50  # W/K，典型散热系数
            thermal_time_constant = thermal_capacity / thermal_conductance
            
            results['thermal_time_constant'] = CalculationResult(
                value=thermal_time_constant,
                method=CalculationMethod.ESTIMATION,
                confidence=0.5,
                formula="τ_th = C_th / G_th = m × c / G",
                notes="热时间常数估算，用于过载时间计算"
            )
        else:
            # 基于功率等级的经验估算
            power_kw = torque_power_results['rated_power'].value / 1000
            thermal_time_constant = 300 * (power_kw ** 0.3)  # 经验公式
            
            results['thermal_time_constant'] = CalculationResult(
                value=thermal_time_constant,
                method=CalculationMethod.EMPIRICAL,
                confidence=0.4,
                formula="τ_th ≈ 300 × P^0.3",
                notes="基于功率等级的热时间常数经验估算"
            )
        
        return results

def print_smart_results(motor_params: SmartMotorParameters, results: SmartCalculatedResults):
    """打印智能计算结果"""
    print("\n" + "="*80)
    print("\t\t智能电机参数计算结果")
    print("="*80)
    
    def print_result(name: str, result: CalculationResult, unit: str = ""):
        """打印单个结果"""
        confidence_str = f"({result.confidence*100:.0f}%)"
        method_str = f"[{result.method.value}]"
        print(f"{name}: {result.value:.6f} {unit} {confidence_str} {method_str}")
        if result.notes:
            print(f"    └─ {result.notes}")
    
    print("\n【输入参数】")
    print(f"极对数: {motor_params.pole_pairs}")
    print(f"额定转速: {motor_params.rated_speed_rpm:.0f} r/min")
    
    # 显示所有输入的可选参数
    optional_params = [
        ('定子电阻', motor_params.stator_resistance, 'Ω'),
        ('定子电感', motor_params.stator_inductance, 'H'),
        ('磁链', motor_params.flux_linkage, 'Wb'),
        ('额定电流', motor_params.rated_current, 'A'),
        ('额定线反电势', motor_params.rated_line_back_emf, 'V'),
        ('母线电压', motor_params.bus_voltage, 'V'),
        ('额定转矩', motor_params.rated_torque, 'Nm'),
        ('转动惯量', motor_params.moment_of_inertia, 'kg·m²'),
        ('电机质量', motor_params.motor_mass, 'kg'),
        ('额定功率', motor_params.rated_power, 'KW'),
        ('功率因数', motor_params.power_factor, ''),
        ('效率', motor_params.efficiency, '%'),
        ('过载倍数', motor_params.overload_factor, ''),
        ('过载持续时间', motor_params.overload_duration, 's')
    ]
    
    for name, value, unit in optional_params:
        if value is not None:
            print(f"{name}: {value} {unit} [用户输入]")
    
    print("\n【计算结果】")
    print("\n基本电气参数:")
    print_result("角速度", results.rated_angular_velocity, "rad/s")
    print_result("反电动势常数", results.back_emf_constant, "V·s/rad")
    print_result("转矩常数", results.torque_constant, "Nm/A")
    print_result("磁链", results.flux_linkage, "Wb")
    
    print("\n电阻电感参数:")
    print_result("定子电阻", results.stator_resistance, "Ω")
    print_result("定子电感", results.stator_inductance, "H")
    
    print("\n反电动势参数:")
    print_result("额定相反电动势", results.rated_phase_back_emf, "V")
    print_result("额定线反电动势", results.rated_line_back_emf, "V")
    
    print("\n电压参数:")
    print_result("额定线电压", results.rated_line_voltage, "V")
    print_result("额定相电压", results.rated_phase_voltage, "V")
    
    print("\n电流参数:")
    print_result("额定电流", results.rated_current, "A")
    print_result("峰值电流", results.peak_current, "A")
    
    print("\n转矩和功率参数:")
    print_result("额定转矩", results.rated_torque, "Nm")
    print_result("额定功率", results.rated_power, "KW")
    print_result("机械功率", results.mechanical_power, "KW")
    print_result("电气功率", results.electrical_power, "KW")
    
    # 过载参数（如果存在）
    if results.overload_current is not None:
        print("\n过载参数:")
        print_result("过载电流", results.overload_current, "A")
        print_result("过载转矩", results.overload_torque, "Nm")
        print_result("过载功率", results.overload_power, "KW")
        print_result("过载铜损", results.overload_losses, "W")
        if results.thermal_time_constant is not None:
            print_result("热时间常数", results.thermal_time_constant, "s")
            
            # 计算过载允许时间
            if motor_params.overload_factor is not None:
                # 简化热模型：θ(t) = θ_∞ × (1 - e^(-t/τ))
                # 假设允许温升为额定温升的1.5倍
                overload_factor_sq = motor_params.overload_factor ** 2
                max_time = results.thermal_time_constant.value * math.log(1.5 / (overload_factor_sq - 1) + 1)
                if max_time > 0:
                    print(f"    估算最大过载时间: {max_time:.1f} s (基于1.5倍额定温升)")
    
    print("\n转动惯量:")
    print_result("转动惯量", results.moment_of_inertia, "kg·m²")
    
    print("\n频率和阻抗参数:")
    print_result("电气频率", results.electrical_frequency, "Hz")
    print_result("感抗", results.reactance, "Ω")
    print_result("总阻抗", results.impedance, "Ω")
    
    print("\n效率和损耗:")
    print_result("效率", results.efficiency, "%")
    print_result("总损耗", results.total_losses, "W")
    print_result("铜损耗", results.copper_losses, "W")
    
    print("\n其他参数:")
    print_result("电感时间常数", results.inductance_time_constant, "s")
    
    # Kt和Ke关系说明
    print("\n【Kt和Ke定义与关系说明】")
    kt_value = results.torque_constant.value
    ke_value = results.back_emf_constant.value
    ratio = kt_value / ke_value if ke_value != 0 else 0
    
    print("\n定义式：")
    print("• 转矩常数 Kt = T_rated / I_rated = (3/2) × p × Ψ")
    print("  其中：T_rated为额定转矩(Nm), I_rated为额定电流(A), p为极对数, Ψ为磁链(Wb)")
    print("• 反电动势常数 Ke = E / ω = p × Ψ")
    print("  其中：E为反电动势(V), ω为角速度(rad/s), p为极对数")
    
    print(f"\n计算结果：")
    print(f"转矩常数 Kt: {kt_value:.6f} Nm/A")
    print(f"反电动势常数 Ke: {ke_value:.6f} V·s/rad")
    print(f"Kt/Ke 比值: {ratio:.6f}")
    
    if abs(ratio - 1.5) < 0.1:
        print("✓ Kt ≈ 1.5×Ke，符合完整物理模型")
    else:
        print("⚠ Kt和Ke比值异常，期望值应为1.5")
    
    print("\n理论关系：")
    print("• Kt = (3/2) × p × Ψ")
    print("• Ke = p × Ψ")
    print("• 因此：Kt/Ke = 1.5 (完整三相电机模型)")
    print("• 磁链关系：Ψ = Ke/p = Kt/(1.5×p)")
    
    print("\n【计算方法说明】")
    print("[user_input]: 用户直接输入")
    print("[theoretical]: 理论公式计算")
    print("[empirical]: 经验公式估算")
    print("[estimation]: 工程估算")
    print("\n置信度说明: 100%=精确值, 90%=高可信, 70%=较可信, 50%=一般估算, 30%=粗略估算")

def create_interactive_calculator():
    """创建交互式计算器"""
    print("乾勤电机参数计算器")
    print("请输入已知参数，未知参数将自动计算")
    print("直接按回车跳过可选参数")
    print("-" * 50)
    
    # 必需参数输入函数
    def get_required_int(prompt):
        while True:
            try:
                value = input(f"{prompt}: ").strip()
                if not value:
                    print("此参数为必需参数，请输入有效值")
                    continue
                return int(value)
            except ValueError:
                print("请输入有效的整数")
    
    def get_required_float(prompt):
        while True:
            try:
                value = input(f"{prompt}: ").strip()
                if not value:
                    print("此参数为必需参数，请输入有效值")
                    continue
                return float(value)
            except ValueError:
                print("请输入有效的数字")
    
    # 必需参数
    pole_pairs = get_required_int("极对数 p (pole pairs)")
    rated_speed_rpm = get_required_float("额定转速 (r/min)")
    
    # 可选参数
    def get_optional_float(prompt):
        while True:
            try:
                value = input(f"{prompt} (回车跳过): ").strip()
                if not value:
                    return None
                return float(value)
            except ValueError:
                print("请输入有效的数字或直接按回车跳过")
    
    params = SmartMotorParameters(
        pole_pairs=pole_pairs,
        rated_speed_rpm=rated_speed_rpm,
        stator_resistance=get_optional_float("定子电阻 R (Ω)"),
        stator_inductance=get_optional_float("定子电感 L (H)"),
        flux_linkage=get_optional_float("磁链 Ψ (Wb)"),
        rated_current=get_optional_float("额定电流 I (A)"),
        rated_line_back_emf=get_optional_float("额定线反电动势 E (V)"),
        rated_torque=get_optional_float("额定转矩 T (Nm)"),
        overload_factor=get_optional_float("过载倍数 (如2.0表示2倍过载)"),
        overload_duration=get_optional_float("过载持续时间 (s)"),
        moment_of_inertia=get_optional_float("转动惯量 J (kg·m²)"),
        motor_mass=get_optional_float("电机质量 m (kg)"),
        rated_power=get_optional_float("额定功率 P_rated (KW)"),
        power_factor=get_optional_float("功率因数 cosφ"),
        efficiency=get_optional_float("效率 η (%)"),
        stator_outer_diameter=get_optional_float("定子外径 (m)"),
        rotor_diameter=get_optional_float("转子直径 (m)"),
        stack_length=get_optional_float("铁心长度 (m)"),
        air_gap=get_optional_float("气隙长度 (m)")
    )
    
    return params

def main():
    """主函数"""
    print("乾勤电机参数计算器")
    print("支持多种计算方法和参数估算")
    print("="*50)
    
    # 选择运行模式
    mode = input("选择模式 (1: 使用默认参数, 2: 交互式输入): ").strip()
    
    if mode == "2":
        motor_params = create_interactive_calculator()
    else:
        # 使用默认参数（部分参数）
        motor_params = SmartMotorParameters(
            pole_pairs=2,
            rated_speed_rpm=45000,
            stator_resistance=0.002215,
            flux_linkage=0.0357,
            rated_current=426,
            rated_line_back_emf=412.3,  # 额定线反电动势
            rated_torque=39.25,
            motor_mass=9.2,
            rated_power=185,  # 185kW
            power_factor=0.8
            # 故意省略一些参数来测试估算功能
        )
    
    # 创建计算器并计算
    calculator = SmartMotorCalculator(motor_params)
    results = calculator.calculate_all_parameters()
    
    # 打印结果
    print_smart_results(motor_params, results)
    
    # 分析建议
    print("\n" + "="*80)
    print("\t\t智能分析建议")
    print("="*80)
    
    # 检查计算质量
    low_confidence_params = []
    for attr_name in dir(results):
        if not attr_name.startswith('_'):
            attr = getattr(results, attr_name)
            if isinstance(attr, CalculationResult) and attr.confidence < 0.7:
                low_confidence_params.append((attr_name, attr.confidence))
    
    if low_confidence_params:
        print("\n⚠ 以下参数置信度较低，建议提供更多输入信息:")
        for param_name, confidence in low_confidence_params:
            print(f"  - {param_name}: {confidence*100:.0f}%")
    
    print("\n💡 提高计算精度的建议:")
    print("1. 提供更多的输入参数可以提高计算精度")
    print("2. 电阻、电感、磁链是核心参数，建议优先测量")
    print("3. 几何参数有助于更准确的转动惯量估算")
    print("4. 实测的效率和功率因数可以改善功率计算")
    print("5. 对于关键应用，建议验证估算参数的准确性")

if __name__ == "__main__":
    main()
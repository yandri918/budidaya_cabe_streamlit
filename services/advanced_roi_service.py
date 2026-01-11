"""
Advanced ROI & Financial Analysis Service
Provides sophisticated financial metrics: NPV, IRR, Payback Period, Sensitivity Analysis
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class AdvancedROIService:
    
    @staticmethod
    def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
        """
        Calculate Net Present Value
        
        Args:
            cash_flows: List of cash flows [initial_investment (negative), cf1, cf2, ...]
            discount_rate: Annual discount rate (e.g., 0.10 for 10%)
        
        Returns:
            NPV value
        """
        npv = 0
        for t, cf in enumerate(cash_flows):
            npv += cf / ((1 + discount_rate) ** t)
        return npv
    
    @staticmethod
    def calculate_irr(cash_flows: List[float], max_iterations: int = 1000, tolerance: float = 1e-6) -> Optional[float]:
        """
        Calculate Internal Rate of Return using Newton-Raphson method
        
        Args:
            cash_flows: List of cash flows [initial_investment (negative), cf1, cf2, ...]
            max_iterations: Maximum iterations for convergence
            tolerance: Convergence tolerance
        
        Returns:
            IRR as decimal (e.g., 0.15 for 15%) or None if not found
        """
        # Initial guess
        irr = 0.1
        
        for _ in range(max_iterations):
            # Calculate NPV and derivative
            npv = 0
            npv_derivative = 0
            
            for t, cf in enumerate(cash_flows):
                npv += cf / ((1 + irr) ** t)
                if t > 0:
                    npv_derivative -= t * cf / ((1 + irr) ** (t + 1))
            
            # Check convergence
            if abs(npv) < tolerance:
                return irr
            
            # Newton-Raphson update
            if npv_derivative != 0:
                irr = irr - npv / npv_derivative
            else:
                return None
        
        return None
    
    @staticmethod
    def calculate_payback_period(cash_flows: List[float]) -> Tuple[Optional[float], List[float]]:
        """
        Calculate payback period in years
        
        Args:
            cash_flows: List of cash flows [initial_investment (negative), cf1, cf2, ...]
        
        Returns:
            Tuple of (payback_period_years, cumulative_cash_flows)
        """
        cumulative = []
        running_total = 0
        
        for cf in cash_flows:
            running_total += cf
            cumulative.append(running_total)
        
        # Find when cumulative becomes positive
        for i, cum_cf in enumerate(cumulative):
            if cum_cf >= 0:
                if i == 0:
                    return 0.0, cumulative
                
                # Linear interpolation for fractional year
                prev_cum = cumulative[i - 1]
                fraction = abs(prev_cum) / (cum_cf - prev_cum)
                payback = i + fraction
                return payback, cumulative
        
        return None, cumulative
    
    @staticmethod
    def calculate_profitability_index(cash_flows: List[float], discount_rate: float) -> float:
        """
        Calculate Profitability Index (PI)
        PI = PV of future cash flows / Initial Investment
        
        Args:
            cash_flows: List of cash flows
            discount_rate: Discount rate
        
        Returns:
            Profitability Index
        """
        initial_investment = abs(cash_flows[0])
        
        pv_future_flows = 0
        for t in range(1, len(cash_flows)):
            pv_future_flows += cash_flows[t] / ((1 + discount_rate) ** t)
        
        if initial_investment > 0:
            return pv_future_flows / initial_investment
        return 0
    
    @staticmethod
    def sensitivity_analysis(
        base_yield: float,
        base_price: float,
        base_cost: float,
        land_area: float = 1.0,
        yield_range: Tuple[float, float] = (0.7, 1.3),
        price_range: Tuple[float, float] = (0.7, 1.3),
        cost_range: Tuple[float, float] = (0.85, 1.15),
        steps: int = 5
    ) -> Dict:
        """
        Perform sensitivity analysis on key variables
        
        Args:
            base_yield: Base yield (ton/ha)
            base_price: Base price (Rp/kg)
            base_cost: Base cost (Rp/ha)
            land_area: Land area (ha)
            yield_range: (min_multiplier, max_multiplier) for yield
            price_range: (min_multiplier, max_multiplier) for price
            cost_range: (min_multiplier, max_multiplier) for cost
            steps: Number of steps for each variable
        
        Returns:
            Dictionary with sensitivity results
        """
        # Calculate base profit
        base_revenue = base_yield * 1000 * base_price * land_area
        base_profit = base_revenue - base_cost
        base_roi = (base_profit / base_cost * 100) if base_cost > 0 else 0
        
        # Yield sensitivity
        yield_multipliers = np.linspace(yield_range[0], yield_range[1], steps)
        yield_impacts = []
        
        for mult in yield_multipliers:
            revenue = (base_yield * mult) * 1000 * base_price * land_area
            profit = revenue - base_cost
            roi = (profit / base_cost * 100) if base_cost > 0 else 0
            yield_impacts.append({
                'multiplier': mult,
                'yield': base_yield * mult,
                'profit': profit,
                'roi': roi,
                'change_from_base': roi - base_roi
            })
        
        # Price sensitivity
        price_multipliers = np.linspace(price_range[0], price_range[1], steps)
        price_impacts = []
        
        for mult in price_multipliers:
            revenue = base_yield * 1000 * (base_price * mult) * land_area
            profit = revenue - base_cost
            roi = (profit / base_cost * 100) if base_cost > 0 else 0
            price_impacts.append({
                'multiplier': mult,
                'price': base_price * mult,
                'profit': profit,
                'roi': roi,
                'change_from_base': roi - base_roi
            })
        
        # Cost sensitivity
        cost_multipliers = np.linspace(cost_range[0], cost_range[1], steps)
        cost_impacts = []
        
        for mult in cost_multipliers:
            cost = base_cost * mult
            profit = base_revenue - cost
            roi = (profit / cost * 100) if cost > 0 else 0
            cost_impacts.append({
                'multiplier': mult,
                'cost': cost,
                'profit': profit,
                'roi': roi,
                'change_from_base': roi - base_roi
            })
        
        # Calculate elasticity (% change in ROI / % change in variable)
        yield_elasticity = (yield_impacts[-1]['roi'] - yield_impacts[0]['roi']) / (
            (yield_range[1] - yield_range[0]) * base_roi
        ) if base_roi != 0 else 0
        
        price_elasticity = (price_impacts[-1]['roi'] - price_impacts[0]['roi']) / (
            (price_range[1] - price_range[0]) * base_roi
        ) if base_roi != 0 else 0
        
        cost_elasticity = (cost_impacts[-1]['roi'] - cost_impacts[0]['roi']) / (
            (cost_range[1] - cost_range[0]) * base_roi
        ) if base_roi != 0 else 0
        
        return {
            'base_scenario': {
                'yield': base_yield,
                'price': base_price,
                'cost': base_cost,
                'revenue': base_revenue,
                'profit': base_profit,
                'roi': base_roi
            },
            'yield_sensitivity': yield_impacts,
            'price_sensitivity': price_impacts,
            'cost_sensitivity': cost_impacts,
            'elasticity': {
                'yield': abs(yield_elasticity),
                'price': abs(price_elasticity),
                'cost': abs(cost_elasticity)
            },
            'most_sensitive_to': max(
                [('yield', abs(yield_elasticity)), 
                 ('price', abs(price_elasticity)), 
                 ('cost', abs(cost_elasticity))],
                key=lambda x: x[1]
            )[0]
        }
    
    @staticmethod
    def multi_scenario_analysis(
        base_yield: float,
        base_price: float,
        base_cost: float,
        land_area: float = 1.0,
        discount_rate: float = 0.10,
        cycles_per_year: int = 3
    ) -> Dict:
        """
        Analyze best case, base case, and worst case scenarios
        
        Args:
            base_yield: Base yield (ton/ha)
            base_price: Base price (Rp/kg)
            base_cost: Base cost (Rp/ha)
            land_area: Land area (ha)
            discount_rate: Discount rate for NPV
            cycles_per_year: Number of planting cycles per year
        
        Returns:
            Dictionary with scenario analysis
        """
        scenarios = {}
        
        # Define scenario parameters
        scenario_params = {
            'worst_case': {
                'yield_mult': 0.7,
                'price_mult': 0.75,
                'cost_mult': 1.15,
                'description': 'Hama berat, harga rendah, biaya tinggi'
            },
            'base_case': {
                'yield_mult': 1.0,
                'price_mult': 1.0,
                'cost_mult': 1.0,
                'description': 'Kondisi normal sesuai rencana'
            },
            'best_case': {
                'yield_mult': 1.2,
                'price_mult': 1.3,
                'cost_mult': 0.95,
                'description': 'Panen optimal, harga tinggi, efisiensi baik'
            }
        }
        
        for scenario_name, params in scenario_params.items():
            yield_val = base_yield * params['yield_mult']
            price_val = base_price * params['price_mult']
            cost_val = base_cost * params['cost_mult']
            
            # Calculate per cycle
            revenue_per_cycle = yield_val * 1000 * price_val * land_area
            profit_per_cycle = revenue_per_cycle - cost_val
            roi_per_cycle = (profit_per_cycle / cost_val * 100) if cost_val > 0 else 0
            
            # Calculate annual (multiple cycles)
            annual_revenue = revenue_per_cycle * cycles_per_year
            annual_cost = cost_val * cycles_per_year
            annual_profit = annual_revenue - annual_cost
            annual_roi = (annual_profit / annual_cost * 100) if annual_cost > 0 else 0
            
            # Cash flows for NPV (initial investment + 3 cycles)
            cash_flows = [-cost_val]  # Initial investment
            for _ in range(cycles_per_year):
                cash_flows.append(revenue_per_cycle)
            
            npv = AdvancedROIService.calculate_npv(cash_flows, discount_rate)
            irr = AdvancedROIService.calculate_irr(cash_flows)
            payback, _ = AdvancedROIService.calculate_payback_period(cash_flows)
            
            scenarios[scenario_name] = {
                'description': params['description'],
                'assumptions': {
                    'yield': yield_val,
                    'price': price_val,
                    'cost': cost_val
                },
                'per_cycle': {
                    'revenue': revenue_per_cycle,
                    'cost': cost_val,
                    'profit': profit_per_cycle,
                    'roi': roi_per_cycle
                },
                'annual': {
                    'revenue': annual_revenue,
                    'cost': annual_cost,
                    'profit': annual_profit,
                    'roi': annual_roi
                },
                'financial_metrics': {
                    'npv': npv,
                    'irr': irr * 100 if irr else None,
                    'payback_months': payback * 4 if payback else None,  # Convert cycles to months
                    'profitability_index': AdvancedROIService.calculate_profitability_index(
                        cash_flows, discount_rate
                    )
                }
            }
        
        return {
            'scenarios': scenarios,
            'comparison': {
                'profit_range': {
                    'min': scenarios['worst_case']['annual']['profit'],
                    'base': scenarios['base_case']['annual']['profit'],
                    'max': scenarios['best_case']['annual']['profit']
                },
                'roi_range': {
                    'min': scenarios['worst_case']['annual']['roi'],
                    'base': scenarios['base_case']['annual']['roi'],
                    'max': scenarios['best_case']['annual']['roi']
                },
                'risk_assessment': AdvancedROIService._assess_risk(scenarios)
            }
        }
    
    @staticmethod
    def _assess_risk(scenarios: Dict) -> Dict:
        """Assess investment risk based on scenarios"""
        worst_profit = scenarios['worst_case']['annual']['profit']
        base_profit = scenarios['base_case']['annual']['profit']
        best_profit = scenarios['best_case']['annual']['profit']
        
        # Downside risk
        downside_risk = abs(worst_profit - base_profit) if worst_profit < base_profit else 0
        
        # Upside potential
        upside_potential = best_profit - base_profit if best_profit > base_profit else 0
        
        # Risk-reward ratio
        risk_reward = upside_potential / downside_risk if downside_risk > 0 else float('inf')
        
        # Probability of loss (simplified)
        prob_loss = 0.0
        if worst_profit < 0:
            prob_loss = 0.15  # 15% in worst case
        
        # Risk level
        if worst_profit > 0 and risk_reward > 2:
            risk_level = 'Low'
            risk_color = '#2ECC71'
        elif worst_profit > 0 and risk_reward > 1:
            risk_level = 'Medium'
            risk_color = '#F39C12'
        else:
            risk_level = 'High'
            risk_color = '#E74C3C'
        
        return {
            'downside_risk': downside_risk,
            'upside_potential': upside_potential,
            'risk_reward_ratio': risk_reward,
            'probability_of_loss': prob_loss,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'recommendation': AdvancedROIService._get_risk_recommendation(risk_level, worst_profit)
        }
    
    @staticmethod
    def _get_risk_recommendation(risk_level: str, worst_profit: float) -> str:
        """Get investment recommendation based on risk"""
        if risk_level == 'Low':
            return "✅ Investasi sangat layak - risiko rendah dengan potensi keuntungan baik"
        elif risk_level == 'Medium':
            return "⚠️ Investasi layak dengan monitoring ketat - perhatikan manajemen biaya"
        else:
            if worst_profit < 0:
                return "❌ Risiko tinggi - pertimbangkan ulang atau tingkatkan mitigasi risiko"
            else:
                return "⚠️ Risiko cukup tinggi - pastikan manajemen optimal untuk mencapai target"

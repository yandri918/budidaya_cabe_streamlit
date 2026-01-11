"""
Monte Carlo Simulation Service
Provides probabilistic modeling and risk analysis for agricultural scenarios
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class DistributionParams:
    """Parameters for probability distributions"""
    dist_type: str  # 'normal', 'triangular', 'uniform'
    mean: float
    std: Optional[float] = None
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    mode: Optional[float] = None  # For triangular


class MonteCarloService:
    
    @staticmethod
    def run_simulation(
        yield_params: DistributionParams,
        price_params: DistributionParams,
        cost_params: DistributionParams,
        land_area: float = 1.0,
        iterations: int = 10000,
        random_seed: Optional[int] = None
    ) -> Dict:
        """
        Run Monte Carlo simulation for agricultural profit analysis
        
        Args:
            yield_params: Distribution parameters for yield (ton/ha)
            price_params: Distribution parameters for price (Rp/kg)
            cost_params: Distribution parameters for cost (Rp/ha)
            land_area: Land area in hectares
            iterations: Number of simulation iterations
            random_seed: Random seed for reproducibility
        
        Returns:
            Dictionary with simulation results
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Generate random samples
        yields = MonteCarloService._generate_samples(yield_params, iterations)
        prices = MonteCarloService._generate_samples(price_params, iterations)
        costs = MonteCarloService._generate_samples(cost_params, iterations)
        
        # Calculate outcomes
        revenues = yields * 1000 * prices * land_area  # Convert ton to kg
        profits = revenues - costs
        rois = (profits / costs) * 100
        
        # Calculate statistics
        results = {
            'iterations': iterations,
            'inputs': {
                'yield': MonteCarloService._calculate_statistics(yields),
                'price': MonteCarloService._calculate_statistics(prices),
                'cost': MonteCarloService._calculate_statistics(costs)
            },
            'outputs': {
                'revenue': MonteCarloService._calculate_statistics(revenues),
                'profit': MonteCarloService._calculate_statistics(profits),
                'roi': MonteCarloService._calculate_statistics(rois)
            },
            'risk_metrics': MonteCarloService._calculate_risk_metrics(profits, rois),
            'probability_analysis': MonteCarloService._calculate_probabilities(profits, rois),
            'percentiles': MonteCarloService._calculate_percentiles(profits, rois),
            'raw_data': {
                'yields': yields.tolist(),
                'prices': prices.tolist(),
                'costs': costs.tolist(),
                'revenues': revenues.tolist(),
                'profits': profits.tolist(),
                'rois': rois.tolist()
            }
        }
        
        return results
    
    @staticmethod
    def _generate_samples(params: DistributionParams, size: int) -> np.ndarray:
        """Generate random samples based on distribution type"""
        if params.dist_type == 'normal':
            samples = np.random.normal(params.mean, params.std, size)
            # Clip to prevent negative values for yield/price
            if params.min_val is not None:
                samples = np.maximum(samples, params.min_val)
            if params.max_val is not None:
                samples = np.minimum(samples, params.max_val)
            return samples
        
        elif params.dist_type == 'triangular':
            return np.random.triangular(params.min_val, params.mode, params.max_val, size)
        
        elif params.dist_type == 'uniform':
            return np.random.uniform(params.min_val, params.max_val, size)
        
        else:
            raise ValueError(f"Unsupported distribution type: {params.dist_type}")
    
    @staticmethod
    def _calculate_statistics(data: np.ndarray) -> Dict:
        """Calculate descriptive statistics"""
        return {
            'mean': float(np.mean(data)),
            'median': float(np.median(data)),
            'std': float(np.std(data)),
            'min': float(np.min(data)),
            'max': float(np.max(data)),
            'cv': float(np.std(data) / np.mean(data)) if np.mean(data) != 0 else 0  # Coefficient of variation
        }
    
    @staticmethod
    def _calculate_risk_metrics(profits: np.ndarray, rois: np.ndarray) -> Dict:
        """Calculate risk metrics"""
        # Value at Risk (VaR) - 5th percentile
        var_95 = np.percentile(profits, 5)
        
        # Conditional Value at Risk (CVaR) / Expected Shortfall
        cvar_95 = np.mean(profits[profits <= var_95])
        
        # Downside deviation (semi-deviation)
        mean_profit = np.mean(profits)
        downside_returns = profits[profits < mean_profit]
        downside_deviation = np.std(downside_returns) if len(downside_returns) > 0 else 0
        
        # Sortino ratio (return / downside risk)
        sortino_ratio = mean_profit / downside_deviation if downside_deviation > 0 else 0
        
        # Maximum drawdown
        max_drawdown = mean_profit - np.min(profits)
        
        return {
            'var_95': float(var_95),
            'cvar_95': float(cvar_95),
            'downside_deviation': float(downside_deviation),
            'sortino_ratio': float(sortino_ratio),
            'max_drawdown': float(max_drawdown),
            'risk_assessment': MonteCarloService._assess_overall_risk(var_95, mean_profit)
        }
    
    @staticmethod
    def _calculate_probabilities(profits: np.ndarray, rois: np.ndarray) -> Dict:
        """Calculate probability of various outcomes"""
        total = len(profits)
        
        return {
            'profit_positive': float(np.sum(profits > 0) / total),
            'profit_above_50m': float(np.sum(profits > 50000000) / total),
            'profit_above_100m': float(np.sum(profits > 100000000) / total),
            'roi_above_50': float(np.sum(rois > 50) / total),
            'roi_above_100': float(np.sum(rois > 100) / total),
            'roi_above_150': float(np.sum(rois > 150) / total),
            'loss_probability': float(np.sum(profits < 0) / total)
        }
    
    @staticmethod
    def _calculate_percentiles(profits: np.ndarray, rois: np.ndarray) -> Dict:
        """Calculate percentile values"""
        percentiles = [5, 10, 25, 50, 75, 90, 95]
        
        return {
            'profit': {
                f'p{p}': float(np.percentile(profits, p)) for p in percentiles
            },
            'roi': {
                f'p{p}': float(np.percentile(rois, p)) for p in percentiles
            }
        }
    
    @staticmethod
    def _assess_overall_risk(var_95: float, mean_profit: float) -> Dict:
        """Assess overall risk level"""
        if var_95 > 0 and mean_profit > var_95 * 2:
            risk_level = 'Low'
            risk_color = '#2ECC71'
            message = 'Risiko rendah - bahkan di skenario terburuk masih untung'
        elif var_95 > 0:
            risk_level = 'Medium'
            risk_color = '#F39C12'
            message = 'Risiko sedang - potensi untung baik tapi perlu monitoring'
        elif var_95 > -mean_profit * 0.5:
            risk_level = 'Medium-High'
            risk_color = '#E67E22'
            message = 'Risiko cukup tinggi - ada kemungkinan rugi di skenario buruk'
        else:
            risk_level = 'High'
            risk_color = '#E74C3C'
            message = 'Risiko tinggi - potensi kerugian signifikan'
        
        return {
            'level': risk_level,
            'color': risk_color,
            'message': message
        }
    
    @staticmethod
    def scenario_comparison(
        scenarios: List[Dict],
        iterations: int = 10000
    ) -> Dict:
        """
        Compare multiple scenarios using Monte Carlo simulation
        
        Args:
            scenarios: List of scenario dictionaries with yield/price/cost params
            iterations: Number of iterations per scenario
        
        Returns:
            Comparison results
        """
        results = {}
        
        for scenario in scenarios:
            name = scenario['name']
            result = MonteCarloService.run_simulation(
                yield_params=scenario['yield_params'],
                price_params=scenario['price_params'],
                cost_params=scenario['cost_params'],
                land_area=scenario.get('land_area', 1.0),
                iterations=iterations
            )
            results[name] = result
        
        # Comparative analysis
        comparison = {
            'scenarios': results,
            'ranking': MonteCarloService._rank_scenarios(results),
            'best_scenario': None,
            'recommendation': None
        }
        
        # Determine best scenario (highest expected profit with acceptable risk)
        best = max(
            results.items(),
            key=lambda x: x[1]['outputs']['profit']['mean'] * (
                1 - x[1]['probability_analysis']['loss_probability']
            )
        )
        
        comparison['best_scenario'] = best[0]
        comparison['recommendation'] = f"Skenario '{best[0]}' memberikan kombinasi terbaik antara profit dan risiko"
        
        return comparison
    
    @staticmethod
    def _rank_scenarios(results: Dict) -> List[Dict]:
        """Rank scenarios by risk-adjusted return"""
        rankings = []
        
        for name, result in results.items():
            # Risk-adjusted score
            mean_profit = result['outputs']['profit']['mean']
            loss_prob = result['probability_analysis']['loss_probability']
            var_95 = result['risk_metrics']['var_95']
            
            # Higher score = better (high profit, low risk)
            score = mean_profit * (1 - loss_prob) + var_95 * 0.5
            
            rankings.append({
                'scenario': name,
                'score': score,
                'mean_profit': mean_profit,
                'loss_probability': loss_prob,
                'var_95': var_95
            })
        
        # Sort by score descending
        rankings.sort(key=lambda x: x['score'], reverse=True)
        
        return rankings
    
    @staticmethod
    def sensitivity_tornado(
        base_yield: float,
        base_price: float,
        base_cost: float,
        land_area: float = 1.0,
        variation_pct: float = 20.0
    ) -> Dict:
        """
        Create tornado diagram data for sensitivity analysis
        
        Args:
            base_yield: Base yield (ton/ha)
            base_price: Base price (Rp/kg)
            base_cost: Base cost (Rp/ha)
            land_area: Land area (ha)
            variation_pct: Percentage variation for each variable
        
        Returns:
            Tornado diagram data
        """
        # Base case
        base_revenue = base_yield * 1000 * base_price * land_area
        base_profit = base_revenue - base_cost
        
        variation = variation_pct / 100
        
        # Test each variable
        variables = []
        
        # Yield impact
        yield_low = (base_yield * (1 - variation)) * 1000 * base_price * land_area - base_cost
        yield_high = (base_yield * (1 + variation)) * 1000 * base_price * land_area - base_cost
        variables.append({
            'variable': 'Yield',
            'low_value': base_yield * (1 - variation),
            'high_value': base_yield * (1 + variation),
            'low_profit': yield_low,
            'high_profit': yield_high,
            'impact_range': abs(yield_high - yield_low),
            'impact_pct': abs(yield_high - yield_low) / base_profit * 100 if base_profit != 0 else 0
        })
        
        # Price impact
        price_low = base_yield * 1000 * (base_price * (1 - variation)) * land_area - base_cost
        price_high = base_yield * 1000 * (base_price * (1 + variation)) * land_area - base_cost
        variables.append({
            'variable': 'Price',
            'low_value': base_price * (1 - variation),
            'high_value': base_price * (1 + variation),
            'low_profit': price_low,
            'high_profit': price_high,
            'impact_range': abs(price_high - price_low),
            'impact_pct': abs(price_high - price_low) / base_profit * 100 if base_profit != 0 else 0
        })
        
        # Cost impact
        cost_low = base_revenue - (base_cost * (1 + variation))  # Higher cost = lower profit
        cost_high = base_revenue - (base_cost * (1 - variation))  # Lower cost = higher profit
        variables.append({
            'variable': 'Cost',
            'low_value': base_cost * (1 + variation),
            'high_value': base_cost * (1 - variation),
            'low_profit': cost_low,
            'high_profit': cost_high,
            'impact_range': abs(cost_high - cost_low),
            'impact_pct': abs(cost_high - cost_low) / base_profit * 100 if base_profit != 0 else 0
        })
        
        # Sort by impact (largest first)
        variables.sort(key=lambda x: x['impact_range'], reverse=True)
        
        return {
            'base_profit': base_profit,
            'variation_pct': variation_pct,
            'variables': variables,
            'most_sensitive': variables[0]['variable'],
            'interpretation': MonteCarloService._interpret_tornado(variables)
        }
    
    @staticmethod
    def _interpret_tornado(variables: List[Dict]) -> str:
        """Interpret tornado diagram results"""
        most_sensitive = variables[0]['variable']
        
        interpretations = {
            'Yield': "Produktivitas (yield) adalah faktor paling kritis. Fokus pada optimasi agronomi dan pengendalian hama.",
            'Price': "Harga pasar adalah faktor paling kritis. Pertimbangkan strategi timing penjualan dan diversifikasi pasar.",
            'Cost': "Biaya produksi adalah faktor paling kritis. Fokus pada efisiensi operasional dan negosiasi supplier."
        }
        
        return interpretations.get(most_sensitive, "Analisis sensitivitas menunjukkan faktor kritis untuk dikelola.")

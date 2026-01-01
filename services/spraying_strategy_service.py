"""
Spraying Strategy Service
Provides spray schedule, dosage calculation, and rotation recommendations
"""

from data.pesticide_database import (
    PESTICIDE_DATABASE,
    SPRAY_SCHEDULE,
    ROTATION_GROUPS,
    get_pesticide_info,
    get_schedule_for_phase
)

class SprayingStrategyService:
    
    @staticmethod
    def calculate_dosage(pesticide_name, land_area_m2, tank_capacity_L=16, application_method="Semprot"):
        """
        Calculate pesticide dosage and water requirements
        
        Args:
            pesticide_name: Name of pesticide
            land_area_m2: Land area in square meters
            tank_capacity_L: Spray tank capacity in liters (default 16L)
            application_method: "Semprot" or "Kocor"
        
        Returns:
            dict with dosage calculations
        """
        pesticide = get_pesticide_info(pesticide_name)
        if not pesticide:
            return None
        
        # Water volume per m2 based on method
        if application_method == "Semprot":
            water_per_m2 = 0.4  # 400 ml/m2 for foliar spray
        else:  # Kocor
            water_per_m2 = 0.2  # 200 ml/m2 for drench
        
        # Total water needed
        total_water_L = land_area_m2 * water_per_m2
        
        # Dosage calculation
        if 'dosage_ml_per_liter' in pesticide:
            dosage_per_liter = pesticide['dosage_ml_per_liter']
            total_pesticide_ml = total_water_L * dosage_per_liter
            unit = "ml"
        else:  # gram-based
            dosage_per_liter = pesticide['dosage_gram_per_liter']
            total_pesticide_ml = total_water_L * dosage_per_liter
            unit = "gram"
        
        # Number of tanks needed
        num_tanks = total_water_L / tank_capacity_L
        
        # Pesticide per tank
        pesticide_per_tank = dosage_per_liter * tank_capacity_L
        
        # Cost calculation
        if unit == "ml":
            pesticide_volume_L = total_pesticide_ml / 1000
            cost = pesticide_volume_L * pesticide['price_per_liter']
        else:  # gram
            pesticide_volume_kg = total_pesticide_ml / 1000
            cost = pesticide_volume_kg * pesticide['price_per_kg']
        
        return {
            'pesticide': pesticide_name,
            'land_area_m2': land_area_m2,
            'land_area_ha': land_area_m2 / 10000,
            'method': application_method,
            'total_water_L': round(total_water_L, 1),
            'total_pesticide': round(total_pesticide_ml, 1),
            'unit': unit,
            'dosage_per_liter': dosage_per_liter,
            'tank_capacity_L': tank_capacity_L,
            'num_tanks': round(num_tanks, 1),
            'pesticide_per_tank': round(pesticide_per_tank, 2),
            'cost': round(cost, 0),
            'cost_per_ha': round(cost / (land_area_m2 / 10000), 0) if land_area_m2 > 0 else 0
        }
    
    @staticmethod
    def get_spray_schedule(growth_phase):
        """Get spray schedule for a growth phase"""
        return get_schedule_for_phase(growth_phase)
    
    @staticmethod
    def get_all_pesticides():
        """Get all pesticides grouped by type"""
        grouped = {
            'Insektisida': [],
            'Fungisida': [],
            'Bakterisida': [],
            'Organik': []
        }
        
        for name, data in PESTICIDE_DATABASE.items():
            pest_type = data['type']
            if 'Organik' in pest_type or 'Bio' in pest_type:
                grouped['Organik'].append(name)
            elif 'Insektisida' in pest_type:
                grouped['Insektisida'].append(name)
            elif 'Fungisida' in pest_type:
                grouped['Fungisida'].append(name)
            elif 'Bakterisida' in pest_type:
                grouped['Bakterisida'].append(name)
        
        return grouped
    
    @staticmethod
    def get_rotation_plan(weeks=4):
        """
        Generate rotation plan to prevent resistance
        
        Args:
            weeks: Number of weeks to plan
        
        Returns:
            list of weekly recommendations
        """
        rotation_plan = []
        
        # Simple rotation: alternate between groups
        insect_groups = list(ROTATION_GROUPS['Insektisida'].keys())
        fungi_groups = list(ROTATION_GROUPS['Fungisida'].keys())
        
        for week in range(1, weeks + 1):
            # Rotate insecticide groups
            insect_group_idx = (week - 1) % len(insect_groups)
            insect_group = insect_groups[insect_group_idx]
            insecticides = ROTATION_GROUPS['Insektisida'][insect_group]
            
            # Rotate fungicide groups
            fungi_group_idx = (week - 1) % len(fungi_groups)
            fungi_group = fungi_groups[fungi_group_idx]
            fungicides = ROTATION_GROUPS['Fungisida'][fungi_group]
            
            rotation_plan.append({
                'week': week,
                'insecticide_group': insect_group,
                'recommended_insecticides': insecticides,
                'fungicide_group': fungi_group,
                'recommended_fungicides': fungicides
            })
        
        return rotation_plan
    
    @staticmethod
    def calculate_monthly_cost(land_area_ha, spray_frequency_per_month=4, pesticide_cost_per_spray=150000):
        """
        Calculate monthly spraying cost
        
        Args:
            land_area_ha: Land area in hectares
            spray_frequency_per_month: Number of sprays per month
            pesticide_cost_per_spray: Average cost per spray per hectare
        
        Returns:
            dict with cost breakdown
        """
        cost_per_month = land_area_ha * spray_frequency_per_month * pesticide_cost_per_spray
        cost_per_year = cost_per_month * 12
        
        # Assume 5 month growing cycle
        cost_per_cycle = cost_per_month * 5
        
        return {
            'land_area_ha': land_area_ha,
            'spray_frequency_per_month': spray_frequency_per_month,
            'cost_per_spray_per_ha': pesticide_cost_per_spray,
            'cost_per_month': cost_per_month,
            'cost_per_year': cost_per_year,
            'cost_per_cycle': cost_per_cycle,
            'cost_per_spray_total': land_area_ha * pesticide_cost_per_spray
        }

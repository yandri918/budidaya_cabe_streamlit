"""
📊 Analytics Hub - Advanced Analytics Dashboard
Comprehensive analytics with predictive, prescriptive, and comparative features
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime

# Import services
from services.analytics_service import AnalyticsService
from services.advanced_roi_service import AdvancedROIService
from services.monte_carlo_service import MonteCarloService, DistributionParams
from data.benchmark_data import BenchmarkDatabase

# Page config
st.set_page_config(
    page_title="Analytics Hub",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 Analytics Hub")
st.markdown("**Enterprise-grade analytics untuk decision making yang lebih baik**")
st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Predictive Analytics",
    "💡 Prescriptive Recommendations",
    "🏆 Comparative Benchmarking",
    "💰 ROI & Financial Analysis",
    "🎲 What-If Scenarios"
])

# ===== TAB 1: PREDICTIVE ANALYTICS =====
with tab1:
    st.header("🎯 Predictive Analytics")
    st.info("**Model prediksi dengan confidence intervals statistik untuk estimasi hasil panen yang akurat**")
    
    col_input1, col_input2, col_input3 = st.columns(3)
    
    with col_input1:
        st.markdown("**📏 Parameter Tanaman**")
        hst = st.number_input("HST (Hari Setelah Tanam)", min_value=0, max_value=200, value=120, step=1)
        avg_height = st.number_input("Tinggi Rata-rata (cm)", min_value=0, max_value=150, value=65, step=1)
        avg_leaves = st.number_input("Jumlah Daun Rata-rata", min_value=0, max_value=100, value=45, step=1)
    
    with col_input2:
        st.markdown("**🌧️ Kondisi Lingkungan**")
        rainfall_mm = st.number_input("Total Curah Hujan (mm)", min_value=0, max_value=2000, value=500, step=10)
        pest_severity = st.slider("Tingkat Serangan Hama (%)", min_value=0, max_value=100, value=10, step=5)
    
    with col_input3:
        st.markdown("**🧪 Input Pupuk (kg/ha)**")
        npk_phonska = st.number_input("NPK Phonska", min_value=0, max_value=500, value=150, step=10, help="Pupuk NPK 15-15-15")
        urea = st.number_input("Urea", min_value=0, max_value=300, value=80, step=10, help="Pupuk nitrogen")
        sp36 = st.number_input("SP-36", min_value=0, max_value=200, value=50, step=10, help="Pupuk fosfat")
        kcl = st.number_input("KCl", min_value=0, max_value=200, value=40, step=10, help="Pupuk kalium")
        
    # Calculate total fertilizer
    fertilizer_kg = npk_phonska + urea + sp36 + kcl
    
    st.caption(f"**Total Pupuk: {fertilizer_kg} kg/ha** (Phonska: {npk_phonska}, Urea: {urea}, SP-36: {sp36}, KCl: {kcl})")

    
    if st.button("🔮 Generate Prediction", type="primary", key="predict_btn"):
        with st.spinner("Calculating predictions..."):
            prediction = AnalyticsService.predict_yield(
                hst, avg_height, avg_leaves, rainfall_mm, fertilizer_kg, pest_severity
            )
        
        st.markdown("---")
        
        # Main prediction
        col_pred1, col_pred2, col_pred3, col_pred4 = st.columns(4)
        
        with col_pred1:
            st.metric(
                "Predicted Yield",
                f"{prediction['predicted_yield']} ton/ha",
                help="Point estimate dari model"
            )
        
        with col_pred2:
            st.metric(
                "95% CI Range",
                f"{prediction['confidence_intervals']['ci_95']['low']:.1f} - {prediction['confidence_intervals']['ci_95']['high']:.1f}",
                help="95% confidence interval"
            )
        
        with col_pred3:
            st.metric(
                "Model Accuracy",
                f"{prediction['accuracy']}%",
                help="Historical accuracy"
            )
        
        with col_pred4:
            st.metric(
                "R² Score",
                f"{prediction['r_squared']:.2f}",
                help="Model goodness of fit"
            )
        
        # Confidence interval visualization
        st.subheader("📊 Confidence Intervals")
        
        fig_ci = go.Figure()
        
        # Add confidence bands
        ci_data = [
            ('80% CI', prediction['confidence_intervals']['ci_80'], '#3498DB', 0.2),
            ('90% CI', prediction['confidence_intervals']['ci_90'], '#2ECC71', 0.15),
            ('95% CI', prediction['confidence_intervals']['ci_95'], '#F39C12', 0.1)
        ]
        
        for name, ci, color, opacity in ci_data:
            fig_ci.add_trace(go.Scatter(
                x=[name, name],
                y=[ci['low'], ci['high']],
                mode='lines+markers',
                name=name,
                line=dict(color=color, width=8),
                marker=dict(size=12, symbol='diamond'),
                opacity=opacity + 0.5
            ))
        
        # Add point estimate
        fig_ci.add_trace(go.Scatter(
            x=['Point Estimate'],
            y=[prediction['predicted_yield']],
            mode='markers',
            name='Prediction',
            marker=dict(size=15, color='#E74C3C', symbol='star')
        ))
        
        fig_ci.update_layout(
            title='Prediction with Confidence Intervals',
            yaxis_title='Yield (ton/ha)',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig_ci, use_container_width=True)
        
        # Factor analysis
        st.subheader("🔍 Factor Analysis")
        
        for factor in prediction['factors']:
            st.markdown(f"""
            <div style='padding: 10px; background-color: {factor['color']}20; border-left: 4px solid {factor['color']}; margin: 5px 0;'>
                <strong>{factor['factor']}</strong>: {factor['impact']}
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.subheader("💡 Quick Recommendations")
        for i, rec in enumerate(prediction['recommendations'], 1):
            st.write(f"{i}. {rec}")

# ===== TAB 2: PRESCRIPTIVE RECOMMENDATIONS =====
with tab2:
    st.header("💡 Prescriptive Recommendations")
    st.info("**Rekomendasi prioritas dengan cost-benefit analysis untuk maximize ROI**")
    
    # Input data for recommendations
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.subheader("Current Performance")
        rec_yield = st.number_input("Current Yield (ton/ha)", min_value=0.0, max_value=20.0, value=9.5, step=0.1, key="rec_yield")
        rec_cost = st.number_input("Total Cost (Rp)", min_value=0, max_value=100000000, value=50000000, step=1000000, key="rec_cost")
        rec_hst = st.number_input("Current HST", min_value=0, max_value=200, value=85, step=1, key="rec_hst")
    
    with col_rec2:
        st.subheader("Benchmark Data")
        rec_yield_percentile = st.slider("Yield Percentile", 0, 100, 45, key="rec_yield_perc")
        rec_roi_percentile = st.slider("ROI Percentile", 0, 100, 50, key="rec_roi_perc")
        rec_efficiency = st.slider("Cost Efficiency Score", 0, 100, 72, key="rec_eff")
    
    if st.button("💡 Generate Recommendations", type="primary", key="rec_btn"):
        with st.spinner("Analyzing and generating recommendations..."):
            # Prepare data
            prediction_data = {
                'predicted_yield': rec_yield,
                'factors': [{'factor': 'Hama Sedang', 'impact': '-10%'}] if rec_yield < 10 else []
            }
            
            cost_data = {
                'efficiency_score': rec_efficiency,
                'opportunities': [
                    {
                        'category': 'Pupuk',
                        'saving': 5000000,
                        'actions': ['Gunakan pupuk organik', 'Beli dalam jumlah besar']
                    },
                    {
                        'category': 'Pestisida',
                        'saving': 3000000,
                        'actions': ['Rotasi pestisida', 'Gunakan IPM']
                    }
                ] if rec_efficiency < 80 else []
            }
            
            benchmark_data = {
                'yield_percentile': rec_yield_percentile,
                'roi_percentile': rec_roi_percentile
            }
            
            recommendations = AnalyticsService.generate_prescriptive_recommendations(
                prediction_data, cost_data, benchmark_data, rec_hst
            )
        
        st.markdown("---")
        
        # Summary
        summary = recommendations['summary']
        col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
        
        with col_sum1:
            st.metric("Total Recommendations", summary['total_recommendations'])
        
        with col_sum2:
            st.metric("Critical Actions", summary['critical_actions'], delta="Urgent")
        
        with col_sum3:
            st.metric("Potential Impact", f"Rp {summary['total_potential_impact']:,.0f}")
        
        with col_sum4:
            st.metric("Aggregate ROI", f"{summary['aggregate_roi']:.0f}%")
        
        # Action Plan
        st.subheader("📅 Phased Action Plan")
        
        action_plan = recommendations['action_plan']
        
        col_phase1, col_phase2, col_phase3 = st.columns(3)
        
        with col_phase1:
            st.markdown("### 🚨 Phase 1: Immediate")
            st.caption(action_plan['phase_1_immediate']['timeframe'])
            for action in action_plan['phase_1_immediate']['actions']:
                st.write(f"• {action}")
            st.metric("Expected Impact", f"Rp {action_plan['phase_1_immediate']['expected_impact']:,.0f}")
        
        with col_phase2:
            st.markdown("### ⚡ Phase 2: Short-term")
            st.caption(action_plan['phase_2_short_term']['timeframe'])
            for action in action_plan['phase_2_short_term']['actions']:
                st.write(f"• {action}")
            st.metric("Expected Impact", f"Rp {action_plan['phase_2_short_term']['expected_impact']:,.0f}")
        
        with col_phase3:
            st.markdown("### 📈 Phase 3: Medium-term")
            st.caption(action_plan['phase_3_medium_term']['timeframe'])
            for action in action_plan['phase_3_medium_term']['actions']:
                st.write(f"• {action}")
            st.metric("Expected Impact", f"Rp {action_plan['phase_3_medium_term']['expected_impact']:,.0f}")
        
        # Detailed recommendations
        st.subheader("📋 Detailed Recommendations")
        
        for i, rec in enumerate(recommendations['recommendations'], 1):
            # Color based on priority
            priority_colors = {
                'Critical': '#E74C3C',
                'High': '#F39C12',
                'Medium': '#3498DB',
                'Low': '#95A5A6'
            }
            
            color = priority_colors.get(rec['priority'], '#95A5A6')
            
            with st.expander(f"#{i} [{rec['urgency']}] {rec['title']}", expanded=(i <= 2)):
                col_detail1, col_detail2 = st.columns([2, 1])
                
                with col_detail1:
                    st.markdown(f"**Category:** {rec['category']}")
                    st.markdown(f"**Timeline:** {rec['timeline']}")
                    
                    st.markdown("**Implementation Steps:**")
                    for step in rec['implementation_steps']:
                        st.write(f"• {step}")
                    
                    st.markdown(f"**Modules to Use:** {', '.join(rec['modules_to_use'])}")
                
                with col_detail2:
                    st.metric("Estimated Impact", f"Rp {rec['estimated_impact']:,.0f}")
                    st.metric("Implementation Cost", f"Rp {rec['cost_to_implement']:,.0f}")
                    st.metric("ROI Estimate", f"{rec['roi_estimate']:.0f}%")

# ===== TAB 3: COMPARATIVE BENCHMARKING =====
with tab3:
    st.header("🏆 Comparative Benchmarking")
    st.info("**Bandingkan performa Anda dengan petani lain di region yang sama**")
    
    col_bench1, col_bench2 = st.columns(2)
    
    with col_bench1:
        st.subheader("Your Performance")
        bench_yield = st.number_input("Your Yield (ton/ha)", min_value=0.0, max_value=20.0, value=11.0, step=0.1, key="bench_yield")
        bench_cost = st.number_input("Your Cost (Rp/ha)", min_value=0, max_value=100000000, value=48000000, step=1000000, key="bench_cost")
        bench_roi = st.number_input("Your ROI (%)", min_value=0, max_value=500, value=115, step=5, key="bench_roi")
    
    with col_bench2:
        st.subheader("Context")
        bench_region = st.selectbox("Region", BenchmarkDatabase.get_all_regions(), key="bench_region")
        bench_variety = st.selectbox("Variety", BenchmarkDatabase.get_all_varieties(), key="bench_variety")
        bench_area = st.number_input("Farm Size (ha)", min_value=0.1, max_value=10.0, value=1.0, step=0.1, key="bench_area")
    
    if st.button("🏆 Compare Performance", type="primary", key="bench_btn"):
        with st.spinner("Analyzing performance..."):
            # Get benchmarks
            region_key = bench_region.lower().replace(' ', '_').replace('(', '').replace(')', '')
            regional_bench = BenchmarkDatabase.get_regional_benchmark(region_key)
            
            # Calculate percentiles
            yield_percentile = BenchmarkDatabase.calculate_percentile_rank(
                bench_yield, regional_bench['yield']
            )
            cost_percentile = BenchmarkDatabase.calculate_percentile_rank(
                bench_cost, regional_bench['cost'], lower_is_better=True
            )
            roi_percentile = BenchmarkDatabase.calculate_percentile_rank(
                bench_roi, regional_bench['roi']
            )
            
            # Overall rank
            overall_rank = (yield_percentile + cost_percentile + roi_percentile) / 3
        
        st.markdown("---")
        
        # Performance tier
        tier_info = BenchmarkDatabase.get_performance_tier(int(overall_rank))
        
        st.markdown(f"""
        <div style='padding: 20px; background: linear-gradient(135deg, {tier_info['color']}20, {tier_info['color']}40); 
                    border: 2px solid {tier_info['color']}; border-radius: 10px; text-align: center;'>
            <h2>{tier_info['icon']} {tier_info['tier']}</h2>
            <p style='font-size: 18px;'>{tier_info['message']}</p>
            <p style='font-size: 24px; font-weight: bold;'>Overall Rank: {overall_rank:.0f}th Percentile</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Detailed metrics
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        with col_metric1:
            st.metric(
                "Yield Ranking",
                f"{yield_percentile}th percentile",
                f"{bench_yield - regional_bench['yield']['p50']:.1f} vs median"
            )
        
        with col_metric2:
            st.metric(
                "Cost Efficiency",
                f"{cost_percentile}th percentile",
                f"{(regional_bench['cost']['p50'] - bench_cost)/1000000:.1f}M vs median"
            )
        
        with col_metric3:
            st.metric(
                "ROI Ranking",
                f"{roi_percentile}th percentile",
                f"+{bench_roi - regional_bench['roi']['p50']:.0f}% vs median"
            )
        
        # Benchmark comparison chart
        st.subheader("📊 Performance vs Regional Benchmarks")
        
        metrics_data = {
            'Metric': ['Yield', 'Cost', 'ROI'],
            'Your Value': [bench_yield, bench_cost/1000000, bench_roi],
            'P25': [regional_bench['yield']['p25'], regional_bench['cost']['p25']/1000000, regional_bench['roi']['p25']],
            'Median (P50)': [regional_bench['yield']['p50'], regional_bench['cost']['p50']/1000000, regional_bench['roi']['p50']],
            'P75': [regional_bench['yield']['p75'], regional_bench['cost']['p75']/1000000, regional_bench['roi']['p75']],
            'P90': [regional_bench['yield']['p90'], regional_bench['cost']['p90']/1000000, regional_bench['roi']['p90']]
        }
        
        df_metrics = pd.DataFrame(metrics_data)
        
        fig_bench = go.Figure()
        
        # Add benchmark ranges
        for i, metric in enumerate(['Yield (ton/ha)', 'Cost (Juta Rp)', 'ROI (%)']):
            fig_bench.add_trace(go.Box(
                y=[df_metrics.iloc[i]['P25'], df_metrics.iloc[i]['Median (P50)'], 
                   df_metrics.iloc[i]['P75'], df_metrics.iloc[i]['P90']],
                name=df_metrics.iloc[i]['Metric'],
                boxmean='sd'
            ))
            
            # Add your value as marker
            fig_bench.add_trace(go.Scatter(
                x=[df_metrics.iloc[i]['Metric']],
                y=[df_metrics.iloc[i]['Your Value']],
                mode='markers',
                name=f'Your {df_metrics.iloc[i]["Metric"]}',
                marker=dict(size=15, color='red', symbol='star')
            ))
        
        fig_bench.update_layout(
            title=f'Performance Comparison - {bench_region}',
            yaxis_title='Value',
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig_bench, use_container_width=True)
        
        # Improvement targets
        st.subheader("🎯 Improvement Targets")
        
        col_target1, col_target2, col_target3 = st.columns(3)
        
        with col_target1:
            if bench_yield < regional_bench['yield']['p75']:
                targets = BenchmarkDatabase.get_improvement_targets(
                    bench_yield, regional_bench['yield'], 'yield'
                )
                st.markdown("**Yield Targets:**")
                for target in targets:
                    st.write(f"• {target['level']}: {target['value']:.1f} ton/ha (+{target['improvement']:.1f})")
        
        with col_target2:
            if bench_cost > regional_bench['cost']['p25']:
                targets = BenchmarkDatabase.get_improvement_targets(
                    bench_cost, regional_bench['cost'], 'cost'
                )
                st.markdown("**Cost Targets:**")
                for target in targets:
                    st.write(f"• {target['level']}: Rp {target['value']/1000000:.1f}M (-Rp {target['improvement']/1000000:.1f}M)")
        
        with col_target3:
            if bench_roi < regional_bench['roi']['p75']:
                targets = BenchmarkDatabase.get_improvement_targets(
                    bench_roi, regional_bench['roi'], 'roi'
                )
                st.markdown("**ROI Targets:**")
                for target in targets:
                    st.write(f"• {target['level']}: {target['value']:.0f}% (+{target['improvement']:.0f}%)")

# Continue in next part due to length...

# ===== TAB 4: ROI & FINANCIAL ANALYSIS =====
with tab4:
    st.header("💰 ROI & Financial Analysis")
    st.info("**Analisis finansial mendalam dengan NPV, IRR, dan sensitivity analysis**")
    
    col_roi1, col_roi2 = st.columns(2)
    
    with col_roi1:
        st.subheader("Investment Parameters")
        roi_initial_investment = st.number_input("Initial Investment (Rp)", min_value=0, max_value=200000000, value=50000000, step=1000000, key="roi_invest")
        roi_yield = st.number_input("Expected Yield (ton/ha)", min_value=0.0, max_value=30.0, value=12.0, step=0.5, key="roi_yield")
        roi_price = st.number_input("Selling Price (Rp/kg)", min_value=0, max_value=100000, value=25000, step=1000, key="roi_price")
    
    with col_roi2:
        st.subheader("Financial Settings")
        roi_discount_rate = st.slider("Discount Rate (%)", min_value=0, max_value=30, value=10, step=1, key="roi_discount") / 100
        roi_cycles = st.number_input("Cycles per Year", min_value=1, max_value=4, value=3, step=1, key="roi_cycles")
        roi_land_area = st.number_input("Land Area (ha)", min_value=0.1, max_value=10.0, value=1.0, step=0.1, key="roi_area")
    
    if st.button("💰 Calculate Financial Metrics", type="primary", key="roi_btn"):
        with st.spinner("Calculating financial metrics..."):
            # Multi-scenario analysis
            scenarios = AdvancedROIService.multi_scenario_analysis(
                base_yield=roi_yield,
                base_price=roi_price,
                base_cost=roi_initial_investment,
                land_area=roi_land_area,
                discount_rate=roi_discount_rate,
                cycles_per_year=roi_cycles
            )
            
            # Sensitivity analysis
            sensitivity = AdvancedROIService.sensitivity_analysis(
                base_yield=roi_yield,
                base_price=roi_price,
                base_cost=roi_initial_investment,
                land_area=roi_land_area
            )
        
        st.markdown("---")
        
        # Scenario comparison
        st.subheader("📊 Multi-Scenario Analysis")
        
        scenario_names = ['worst_case', 'base_case', 'best_case']
        scenario_labels = ['Worst Case', 'Base Case', 'Best Case']
        scenario_colors = ['#E74C3C', '#3498DB', '#2ECC71']
        
        col_sc1, col_sc2, col_sc3 = st.columns(3)
        
        for col, name, label, color in zip([col_sc1, col_sc2, col_sc3], scenario_names, scenario_labels, scenario_colors):
            with col:
                scenario = scenarios['scenarios'][name]
                st.markdown(f"### {label}")
                st.caption(scenario['description'])
                
                st.metric("Annual Profit", f"Rp {scenario['annual']['profit']:,.0f}")
                st.metric("Annual ROI", f"{scenario['annual']['roi']:.1f}%")
                
                if scenario['financial_metrics']['npv']:
                    st.metric("NPV", f"Rp {scenario['financial_metrics']['npv']:,.0f}")
                
                if scenario['financial_metrics']['irr']:
                    st.metric("IRR", f"{scenario['financial_metrics']['irr']:.1f}%")
                
                if scenario['financial_metrics']['payback_months']:
                    st.metric("Payback Period", f"{scenario['financial_metrics']['payback_months']:.1f} months")
        
        # Risk assessment
        st.markdown("---")
        st.subheader("⚠️ Risk Assessment")
        
        risk = scenarios['comparison']['risk_assessment']
        
        st.markdown(f"""
        <div style='padding: 20px; background-color: {risk['risk_color']}20; border: 2px solid {risk['risk_color']}; border-radius: 10px;'>
            <h3>Risk Level: {risk['risk_level']}</h3>
            <p>{risk['recommendation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_risk1, col_risk2, col_risk3 = st.columns(3)
        
        with col_risk1:
            st.metric("Downside Risk", f"Rp {risk['downside_risk']:,.0f}")
        
        with col_risk2:
            st.metric("Upside Potential", f"Rp {risk['upside_potential']:,.0f}")
        
        with col_risk3:
            st.metric("Risk-Reward Ratio", f"{risk['risk_reward_ratio']:.2f}")
        
        # Sensitivity analysis
        st.markdown("---")
        st.subheader("🎯 Sensitivity Analysis")
        
        st.info(f"**Most Sensitive To:** {sensitivity['most_sensitive_to'].title()} - Fokuskan effort pada faktor ini untuk maximize impact")
        
        # Tornado diagram
        st.markdown("#### Tornado Diagram - Impact on Profit")
        
        fig_tornado = go.Figure()
        
        variables = sensitivity['yield_sensitivity'] + sensitivity['price_sensitivity'] + sensitivity['cost_sensitivity']
        var_names = ['Yield -20%', 'Yield +20%', 'Price -20%', 'Price +20%', 'Cost +20%', 'Cost -20%']
        
        # Create tornado chart
        base_profit = sensitivity['base_scenario']['profit']
        
        tornado_data = []
        for var_type, var_list in [('Yield', sensitivity['yield_sensitivity']), 
                                     ('Price', sensitivity['price_sensitivity']), 
                                     ('Cost', sensitivity['cost_sensitivity'])]:
            low_impact = var_list[0]['profit'] - base_profit
            high_impact = var_list[-1]['profit'] - base_profit
            tornado_data.append({
                'variable': var_type,
                'low': low_impact,
                'high': high_impact,
                'range': abs(high_impact - low_impact)
            })
        
        # Sort by range
        tornado_data.sort(key=lambda x: x['range'], reverse=True)
        
        for data in tornado_data:
            fig_tornado.add_trace(go.Bar(
                name=f"{data['variable']} Impact",
                y=[data['variable']],
                x=[data['high']],
                orientation='h',
                marker=dict(color='#2ECC71')
            ))
            
            fig_tornado.add_trace(go.Bar(
                name=f"{data['variable']} Impact",
                y=[data['variable']],
                x=[data['low']],
                orientation='h',
                marker=dict(color='#E74C3C')
            ))
        
        fig_tornado.update_layout(
            title='Sensitivity Tornado Diagram',
            xaxis_title='Impact on Profit (Rp)',
            barmode='overlay',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_tornado, use_container_width=True)

# ===== TAB 5: WHAT-IF SCENARIOS =====
with tab5:
    st.header("🎲 What-If Scenario Modeling")
    st.info("**Monte Carlo simulation untuk probabilistic analysis dan risk assessment**")
    
    st.subheader("📊 Define Uncertainty Ranges")
    
    col_mc1, col_mc2, col_mc3 = st.columns(3)
    
    with col_mc1:
        st.markdown("**Yield Uncertainty**")
        mc_yield_mean = st.number_input("Mean Yield (ton/ha)", min_value=0.0, max_value=30.0, value=10.0, step=0.5, key="mc_yield_mean")
        mc_yield_std = st.number_input("Std Dev (%)", min_value=0, max_value=50, value=15, step=1, key="mc_yield_std") / 100
        mc_yield_min = mc_yield_mean * (1 - mc_yield_std * 2)
        mc_yield_max = mc_yield_mean * (1 + mc_yield_std * 2)
    
    with col_mc2:
        st.markdown("**Price Uncertainty**")
        mc_price_mean = st.number_input("Mean Price (Rp/kg)", min_value=0, max_value=100000, value=25000, step=1000, key="mc_price_mean")
        mc_price_std = st.number_input("Std Dev (%) ", min_value=0, max_value=50, value=20, step=1, key="mc_price_std") / 100
        mc_price_min = mc_price_mean * (1 - mc_price_std * 2)
        mc_price_max = mc_price_mean * (1 + mc_price_std * 2)
    
    with col_mc3:
        st.markdown("**Cost Uncertainty**")
        mc_cost_mean = st.number_input("Mean Cost (Rp)", min_value=0, max_value=200000000, value=50000000, step=1000000, key="mc_cost_mean")
        mc_cost_std = st.number_input("Std Dev (%)  ", min_value=0, max_value=30, value=10, step=1, key="mc_cost_std") / 100
        mc_cost_min = mc_cost_mean * (1 - mc_cost_std * 2)
        mc_cost_max = mc_cost_mean * (1 + mc_cost_std * 2)
    
    mc_iterations = st.slider("Number of Simulations", min_value=1000, max_value=10000, value=5000, step=1000, key="mc_iterations")
    mc_land_area = st.number_input("Land Area (ha) ", min_value=0.1, max_value=10.0, value=1.0, step=0.1, key="mc_area")
    
    if st.button("🎲 Run Monte Carlo Simulation", type="primary", key="mc_btn"):
        with st.spinner(f"Running {mc_iterations:,} simulations..."):
            # Create distribution parameters
            yield_params = DistributionParams(
                dist_type='normal',
                mean=mc_yield_mean,
                std=mc_yield_mean * mc_yield_std,
                min_val=max(0, mc_yield_min),
                max_val=mc_yield_max
            )
            
            price_params = DistributionParams(
                dist_type='normal',
                mean=mc_price_mean,
                std=mc_price_mean * mc_price_std,
                min_val=max(0, mc_price_min),
                max_val=mc_price_max
            )
            
            cost_params = DistributionParams(
                dist_type='normal',
                mean=mc_cost_mean,
                std=mc_cost_mean * mc_cost_std,
                min_val=max(0, mc_cost_min),
                max_val=mc_cost_max
            )
            
            # Run simulation
            results = MonteCarloService.run_simulation(
                yield_params=yield_params,
                price_params=price_params,
                cost_params=cost_params,
                land_area=mc_land_area,
                iterations=mc_iterations,
                random_seed=42
            )
        
        st.success(f"✅ Simulation completed! Analyzed {mc_iterations:,} scenarios")
        
        st.markdown("---")
        
        # Summary statistics
        st.subheader("📈 Simulation Results")
        
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        
        with col_res1:
            st.metric("Mean Profit", f"Rp {results['outputs']['profit']['mean']:,.0f}")
            st.caption(f"Median: Rp {results['outputs']['profit']['median']:,.0f}")
        
        with col_res2:
            st.metric("Mean ROI", f"{results['outputs']['roi']['mean']:.1f}%")
            st.caption(f"Median: {results['outputs']['roi']['median']:.1f}%")
        
        with col_res3:
            st.metric("Profit Range", f"Rp {(results['outputs']['profit']['max'] - results['outputs']['profit']['min'])/1000000:.1f}M")
            st.caption(f"Min to Max spread")
        
        with col_res4:
            st.metric("Std Deviation", f"Rp {results['outputs']['profit']['std']/1000000:.1f}M")
            st.caption(f"Volatility measure")
        
        # Probability analysis
        st.markdown("---")
        st.subheader("🎯 Probability Analysis")
        
        prob = results['probability_analysis']
        
        col_prob1, col_prob2, col_prob3 = st.columns(3)
        
        with col_prob1:
            st.metric("Probability of Profit", f"{prob['profit_positive']*100:.1f}%")
            st.progress(prob['profit_positive'])
        
        with col_prob2:
            st.metric("Prob ROI > 100%", f"{prob['roi_above_100']*100:.1f}%")
            st.progress(prob['roi_above_100'])
        
        with col_prob3:
            st.metric("Prob ROI > 150%", f"{prob['roi_above_150']*100:.1f}%")
            st.progress(prob['roi_above_150'])
        
        # Risk metrics
        st.markdown("---")
        st.subheader("⚠️ Risk Metrics")
        
        risk_metrics = results['risk_metrics']
        risk_assessment = risk_metrics['risk_assessment']
        
        st.markdown(f"""
        <div style='padding: 20px; background-color: {risk_assessment['color']}20; border: 2px solid {risk_assessment['color']}; border-radius: 10px;'>
            <h3>Risk Level: {risk_assessment['level']}</h3>
            <p>{risk_assessment['message']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_risk_mc1, col_risk_mc2, col_risk_mc3, col_risk_mc4 = st.columns(4)
        
        with col_risk_mc1:
            st.metric("VaR (95%)", f"Rp {risk_metrics['var_95']:,.0f}", help="Value at Risk - worst case in 95% of scenarios")
        
        with col_risk_mc2:
            st.metric("CVaR (95%)", f"Rp {risk_metrics['cvar_95']:,.0f}", help="Conditional VaR - expected loss when VaR is exceeded")
        
        with col_risk_mc3:
            st.metric("Sortino Ratio", f"{risk_metrics['sortino_ratio']:.2f}", help="Return per unit of downside risk")
        
        with col_risk_mc4:
            st.metric("Max Drawdown", f"Rp {risk_metrics['max_drawdown']/1000000:.1f}M", help="Maximum potential loss")
        
        # Distribution charts
        st.markdown("---")
        st.subheader("📊 Probability Distributions")
        
        col_dist1, col_dist2 = st.columns(2)
        
        with col_dist1:
            # Profit distribution
            fig_profit_dist = go.Figure()
            
            fig_profit_dist.add_trace(go.Histogram(
                x=results['raw_data']['profits'],
                nbinsx=50,
                name='Profit Distribution',
                marker_color='#3498DB'
            ))
            
            # Add mean line
            fig_profit_dist.add_vline(
                x=results['outputs']['profit']['mean'],
                line_dash="dash",
                line_color="red",
                annotation_text="Mean"
            )
            
            # Add VaR line
            fig_profit_dist.add_vline(
                x=risk_metrics['var_95'],
                line_dash="dash",
                line_color="orange",
                annotation_text="VaR 95%"
            )
            
            fig_profit_dist.update_layout(
                title='Profit Distribution',
                xaxis_title='Profit (Rp)',
                yaxis_title='Frequency',
                height=400
            )
            
            st.plotly_chart(fig_profit_dist, use_container_width=True)
        
        with col_dist2:
            # ROI distribution
            fig_roi_dist = go.Figure()
            
            fig_roi_dist.add_trace(go.Histogram(
                x=results['raw_data']['rois'],
                nbinsx=50,
                name='ROI Distribution',
                marker_color='#2ECC71'
            ))
            
            # Add mean line
            fig_roi_dist.add_vline(
                x=results['outputs']['roi']['mean'],
                line_dash="dash",
                line_color="red",
                annotation_text="Mean"
            )
            
            fig_roi_dist.update_layout(
                title='ROI Distribution',
                xaxis_title='ROI (%)',
                yaxis_title='Frequency',
                height=400
            )
            
            st.plotly_chart(fig_roi_dist, use_container_width=True)
        
        # Percentile table
        st.markdown("---")
        st.subheader("📊 Percentile Analysis")
        
        percentiles_df = pd.DataFrame({
            'Percentile': ['P5', 'P10', 'P25', 'P50 (Median)', 'P75', 'P90', 'P95'],
            'Profit (Rp)': [
                f"Rp {results['percentiles']['profit']['p5']:,.0f}",
                f"Rp {results['percentiles']['profit']['p10']:,.0f}",
                f"Rp {results['percentiles']['profit']['p25']:,.0f}",
                f"Rp {results['percentiles']['profit']['p50']:,.0f}",
                f"Rp {results['percentiles']['profit']['p75']:,.0f}",
                f"Rp {results['percentiles']['profit']['p90']:,.0f}",
                f"Rp {results['percentiles']['profit']['p95']:,.0f}"
            ],
            'ROI (%)': [
                f"{results['percentiles']['roi']['p5']:.1f}%",
                f"{results['percentiles']['roi']['p10']:.1f}%",
                f"{results['percentiles']['roi']['p25']:.1f}%",
                f"{results['percentiles']['roi']['p50']:.1f}%",
                f"{results['percentiles']['roi']['p75']:.1f}%",
                f"{results['percentiles']['roi']['p90']:.1f}%",
                f"{results['percentiles']['roi']['p95']:.1f}%"
            ]
        })
        
        st.dataframe(percentiles_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>📊 Analytics Hub - Advanced Analytics Dashboard</strong></p>
    <p><small>Enterprise-grade analytics untuk data-driven decision making</small></p>
</div>
""", unsafe_allow_html=True)

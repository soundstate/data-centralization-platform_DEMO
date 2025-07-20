"""
Demo Scenarios Creator

Creates industry-specific demo data scenarios for stakeholder demonstrations,
including e-commerce, manufacturing, and financial services use cases.
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta, date
from decimal import Decimal
from typing import Dict, List, Any
import random
import pandas as pd
import numpy as np

class DemoScenariosCreator:
    """
    Creates compelling demo scenarios for different industries
    """
    
    def __init__(self):
        self.scenarios = {}
        
    def create_all_scenarios(self):
        """Create all demo scenarios"""
        print("🎭 Creating demo scenarios for stakeholder showcases...")
        
        # Create scenarios for different industries
        self.scenarios["ecommerce"] = self._create_ecommerce_scenario()
        self.scenarios["manufacturing"] = self._create_manufacturing_scenario()
        self.scenarios["financial_services"] = self._create_financial_services_scenario()
        
        # Create cross-scenario correlations
        self.scenarios["cross_domain_insights"] = self._create_cross_domain_insights()
        
        return self.scenarios
    
    def _create_ecommerce_scenario(self):
        """Create e-commerce company demo scenario"""
        print("🛍️ Creating e-commerce scenario...")
        
        # Sales data with seasonal patterns
        sales_data = self._generate_sales_data()
        
        # Marketing campaign data
        marketing_data = self._generate_marketing_data()
        
        # Customer service data
        customer_service_data = self._generate_customer_service_data()
        
        # Weather correlation data
        weather_correlation = self._generate_weather_sales_correlation()
        
        # Product performance data
        product_data = self._generate_product_performance_data()
        
        return {
            "title": "E-commerce Data Centralization Demo",
            "business_problem": "Fragmented data across sales, marketing, and customer service platforms",
            "roi_calculation": {
                "time_to_insight_improvement": "From 2 weeks to 2 hours (95% reduction)",
                "correlation_discovery": "23% weather-sales correlation identified",
                "proactive_intervention": "48-hour early warning for customer issues",
                "revenue_impact": "$2.3M annual increase from weather-based inventory optimization"
            },
            "data_sources": {
                "sales_transactions": sales_data,
                "marketing_campaigns": marketing_data,
                "customer_service": customer_service_data,
                "weather_patterns": weather_correlation,
                "product_catalog": product_data
            },
            "key_insights": [
                {
                    "insight": "Weather-Sales Correlation Discovery",
                    "description": "AI identified 23% correlation between temperature and specific product categories",
                    "business_impact": "Enabled predictive inventory management saving $340K in excess inventory costs",
                    "correlation_strength": 0.23,
                    "p_value": 0.0023,
                    "sample_size": 15000
                },
                {
                    "insight": "Customer Service Predictive Alert",
                    "description": "Service ticket volume predicts negative reviews 48 hours in advance",
                    "business_impact": "Reduced negative reviews by 35% through proactive intervention",
                    "correlation_strength": 0.67,
                    "p_value": 0.0001,
                    "sample_size": 8500
                },
                {
                    "insight": "Marketing Channel Attribution",
                    "description": "Cross-platform customer journey reveals true channel ROI",
                    "business_impact": "Redirected $500K marketing budget to 40% higher ROI channels",
                    "correlation_strength": 0.84,
                    "p_value": 0.0000012,
                    "sample_size": 25000
                }
            ],
            "demo_flow": [
                "Show real-time dashboard with multiple data streams",
                "Demonstrate AI discovering weather-sales correlation",
                "Navigate to predictive customer service alerts",
                "Calculate ROI from marketing channel optimization",
                "Show geographic performance patterns"
            ]
        }
    
    def _create_manufacturing_scenario(self):
        """Create manufacturing company demo scenario"""
        print("🏭 Creating manufacturing scenario...")
        
        # Production data
        production_data = self._generate_production_data()
        
        # Quality metrics
        quality_data = self._generate_quality_data()
        
        # Equipment maintenance
        maintenance_data = self._generate_maintenance_data()
        
        # Supply chain data
        supply_chain_data = self._generate_supply_chain_data()
        
        return {
            "title": "Manufacturing Operations Intelligence Demo",
            "business_problem": "Disconnected operational data affecting efficiency and quality",
            "roi_calculation": {
                "downtime_reduction": "35% reduction in unplanned downtime",
                "quality_improvement": "27% decrease in defect rates",
                "maintenance_optimization": "$1.2M annual savings in maintenance costs",
                "efficiency_gains": "18% improvement in overall equipment effectiveness (OEE)"
            },
            "data_sources": {
                "production_metrics": production_data,
                "quality_control": quality_data,
                "equipment_maintenance": maintenance_data,
                "supply_chain": supply_chain_data
            },
            "key_insights": [
                {
                    "insight": "Predictive Equipment Failure",
                    "description": "Vibration and temperature patterns predict bearing failures 5-7 days early",
                    "business_impact": "$1.2M saved in emergency repairs and production delays",
                    "correlation_strength": 0.89,
                    "p_value": 0.00001,
                    "sample_size": 3200
                },
                {
                    "insight": "Quality Root Cause Discovery",
                    "description": "Humidity levels in Building C correlated with 18% of product defects",
                    "business_impact": "Simple HVAC upgrade eliminated persistent quality issues",
                    "correlation_strength": 0.72,
                    "p_value": 0.0003,
                    "sample_size": 12500
                },
                {
                    "insight": "Supplier Performance Impact",
                    "description": "Material lot characteristics predict downstream quality issues",
                    "business_impact": "Supplier quality requirements updated, reducing defects by 31%",
                    "correlation_strength": 0.56,
                    "p_value": 0.0012,
                    "sample_size": 8900
                }
            ],
            "demo_flow": [
                "Display production dashboard with real-time OEE metrics",
                "Show predictive maintenance alerts and cost savings",
                "Demonstrate quality correlation analysis",
                "Navigate supply chain performance optimization",
                "Calculate total operational efficiency improvements"
            ]
        }
    
    def _create_financial_services_scenario(self):
        """Create financial services demo scenario"""
        print("🏦 Creating financial services scenario...")
        
        # Risk assessment data
        risk_data = self._generate_risk_data()
        
        # Customer transaction data
        transaction_data = self._generate_transaction_data()
        
        # Market data
        market_data = self._generate_market_data()
        
        # Regulatory data
        regulatory_data = self._generate_regulatory_data()
        
        return {
            "title": "Financial Services Risk Intelligence Demo",
            "business_problem": "Risk assessment limited by data silos and delayed insights",
            "roi_calculation": {
                "risk_detection_speed": "From 48 hours to 15 minutes (99% faster)",
                "fraud_prevention": "$3.8M prevented losses through early detection",
                "compliance_efficiency": "67% reduction in regulatory reporting time",
                "customer_insights": "360-degree view improving retention by 23%"
            },
            "data_sources": {
                "risk_metrics": risk_data,
                "customer_transactions": transaction_data,
                "market_conditions": market_data,
                "regulatory_requirements": regulatory_data
            },
            "key_insights": [
                {
                    "insight": "Real-time Fraud Pattern Detection",
                    "description": "Cross-account transaction patterns identify fraud rings within minutes",
                    "business_impact": "$3.8M in prevented losses, 94% accuracy rate",
                    "correlation_strength": 0.91,
                    "p_value": 0.0000001,
                    "sample_size": 45000
                },
                {
                    "insight": "Market Risk Early Warning",
                    "description": "Client portfolio correlations with market volatility predict risk exposure",
                    "business_impact": "Proactive risk management prevented $12M in client losses",
                    "correlation_strength": 0.78,
                    "p_value": 0.0000034,
                    "sample_size": 18500
                },
                {
                    "insight": "Customer Lifetime Value Prediction",
                    "description": "Transaction patterns and life events predict customer profitability",
                    "business_impact": "Personalized services increased customer retention by 23%",
                    "correlation_strength": 0.65,
                    "p_value": 0.0002,
                    "sample_size": 35000
                }
            ],
            "demo_flow": [
                "Display real-time risk dashboard with market correlations",
                "Show fraud detection system catching suspicious patterns",
                "Demonstrate regulatory compliance automation",
                "Navigate customer 360-degree view and insights",
                "Calculate risk-adjusted returns and compliance savings"
            ]
        }
    
    def _create_cross_domain_insights(self):
        """Create cross-domain insight examples"""
        print("🔗 Creating cross-domain insights...")
        
        return {
            "title": "Cross-Domain Intelligence Discovery",
            "description": "Unique insights only possible through unified data platform",
            "insights": [
                {
                    "domains": ["weather", "sales", "social_media"],
                    "insight": "Rainy Day Social Commerce Correlation",
                    "description": "Social media engagement increases 34% on rainy days, driving 28% higher online sales in comfort products",
                    "business_application": "Weather-triggered social media campaigns and inventory positioning"
                },
                {
                    "domains": ["supply_chain", "market_news", "customer_behavior"],
                    "insight": "Supply Disruption Demand Prediction",
                    "description": "News sentiment about supply chain issues predicts customer hoarding behavior 72 hours in advance",
                    "business_application": "Proactive inventory management and dynamic pricing strategies"
                },
                {
                    "domains": ["employee_productivity", "customer_satisfaction", "financial_performance"],
                    "insight": "Human Capital ROI Correlation",
                    "description": "Employee satisfaction scores correlate with customer satisfaction (r=0.73) and revenue per customer (r=0.68)",
                    "business_application": "Employee investment directly tied to customer and financial outcomes"
                }
            ]
        }
    
    def _generate_sales_data(self):
        """Generate realistic e-commerce sales data"""
        base_date = datetime.now() - timedelta(days=365)
        sales_records = []
        
        # Product categories with seasonal patterns
        categories = {
            "winter_clothing": {"base_sales": 100, "winter_multiplier": 3.5, "summer_multiplier": 0.3},
            "summer_clothing": {"base_sales": 120, "winter_multiplier": 0.4, "summer_multiplier": 2.8},
            "electronics": {"base_sales": 200, "winter_multiplier": 1.2, "summer_multiplier": 1.1},
            "home_goods": {"base_sales": 80, "winter_multiplier": 1.0, "summer_multiplier": 1.0},
            "outdoor_equipment": {"base_sales": 60, "winter_multiplier": 0.6, "summer_multiplier": 2.2}
        }
        
        for day in range(365):
            current_date = base_date + timedelta(days=day)
            day_of_year = current_date.timetuple().tm_yday
            
            # Seasonal multiplier (sine wave peaking in summer)
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
            
            # Weekend boost
            weekend_factor = 1.3 if current_date.weekday() >= 5 else 1.0
            
            for category, params in categories.items():
                # Category-specific seasonal adjustment
                if "winter" in category:
                    category_seasonal = params["winter_multiplier"] if day_of_year < 90 or day_of_year > 270 else params["summer_multiplier"]
                elif "summer" in category:
                    category_seasonal = params["summer_multiplier"] if 120 < day_of_year < 270 else params["winter_multiplier"]
                else:
                    category_seasonal = 1.0
                
                daily_sales = int(params["base_sales"] * seasonal_factor * weekend_factor * category_seasonal * random.uniform(0.7, 1.4))
                
                sales_records.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "category": category,
                    "daily_units_sold": daily_sales,
                    "daily_revenue": daily_sales * random.uniform(15.99, 299.99),
                    "avg_order_value": random.uniform(45, 180),
                    "unique_customers": int(daily_sales * random.uniform(0.6, 0.9))
                })
        
        return sales_records[:50]  # Return sample for demo
    
    def _generate_marketing_data(self):
        """Generate marketing campaign data"""
        campaigns = [
            {"name": "Winter Warmth Campaign", "channel": "social_media", "budget": 25000, "target": "winter_clothing"},
            {"name": "Summer Adventure Series", "channel": "search_ads", "budget": 35000, "target": "outdoor_equipment"},
            {"name": "Tech Tuesday Promotions", "channel": "email", "budget": 8000, "target": "electronics"},
            {"name": "Home Comfort Collection", "channel": "display_ads", "budget": 15000, "target": "home_goods"},
            {"name": "Weekend Warrior Campaign", "channel": "influencer", "budget": 20000, "target": "outdoor_equipment"}
        ]
        
        campaign_performance = []
        for campaign in campaigns:
            # Simulate performance metrics
            impressions = int(campaign["budget"] * random.uniform(8, 15))
            clicks = int(impressions * random.uniform(0.02, 0.08))
            conversions = int(clicks * random.uniform(0.15, 0.35))
            revenue = conversions * random.uniform(65, 220)
            
            campaign_performance.append({
                "campaign_name": campaign["name"],
                "channel": campaign["channel"],
                "target_category": campaign["target"],
                "budget": campaign["budget"],
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "revenue": round(revenue, 2),
                "roas": round(revenue / campaign["budget"], 2),
                "ctr": round(clicks / impressions * 100, 3),
                "conversion_rate": round(conversions / clicks * 100, 2) if clicks > 0 else 0
            })
        
        return campaign_performance
    
    def _generate_customer_service_data(self):
        """Generate customer service ticket data"""
        ticket_types = ["product_defect", "shipping_delay", "billing_inquiry", "return_request", "technical_support"]
        priorities = ["low", "medium", "high", "urgent"]
        
        base_date = datetime.now() - timedelta(days=30)
        tickets = []
        
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            
            # More tickets on Mondays and after product launches
            day_multiplier = 1.4 if current_date.weekday() == 0 else 1.0
            
            daily_tickets = int(random.uniform(15, 45) * day_multiplier)
            
            for _ in range(daily_tickets):
                ticket_type = random.choice(ticket_types)
                priority = random.choice(priorities)
                
                # Resolution time based on priority
                resolution_hours = {
                    "urgent": random.uniform(2, 8),
                    "high": random.uniform(4, 24),
                    "medium": random.uniform(12, 72),
                    "low": random.uniform(24, 168)
                }[priority]
                
                tickets.append({
                    "ticket_id": f"TK-{random.randint(10000, 99999)}",
                    "created_date": current_date.strftime("%Y-%m-%d"),
                    "ticket_type": ticket_type,
                    "priority": priority,
                    "resolution_hours": round(resolution_hours, 1),
                    "customer_satisfaction": random.uniform(2.5, 5.0),
                    "requires_escalation": priority in ["high", "urgent"] and random.random() < 0.3
                })
        
        return tickets[:25]  # Return sample for demo
    
    def _generate_weather_sales_correlation(self):
        """Generate weather data that correlates with sales"""
        base_date = datetime.now() - timedelta(days=30)
        weather_sales = []
        
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            
            # Generate correlated weather and sales data
            temperature = random.uniform(15, 35)  # Celsius
            humidity = random.uniform(40, 90)
            condition = "sunny" if temperature > 25 and humidity < 60 else "rainy" if humidity > 75 else "cloudy"
            
            # Weather-influenced sales patterns
            outdoor_sales_factor = max(0.3, (temperature - 15) / 20)  # Higher temp = more outdoor sales
            comfort_sales_factor = max(0.5, (90 - humidity) / 50)     # Lower humidity = more comfort product sales
            
            weather_sales.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "temperature_c": round(temperature, 1),
                "humidity_percent": int(humidity),
                "weather_condition": condition,
                "outdoor_equipment_sales": int(60 * outdoor_sales_factor * random.uniform(0.8, 1.3)),
                "winter_clothing_sales": int(100 * (1 - outdoor_sales_factor) * random.uniform(0.7, 1.4)),
                "correlation_strength": round(outdoor_sales_factor, 3)
            })
        
        return weather_sales
    
    def _generate_product_performance_data(self):
        """Generate product catalog and performance data"""
        products = [
            {"name": "UltraWarm Winter Jacket", "category": "winter_clothing", "price": 129.99, "margin": 0.45},
            {"name": "SummerBreeze Shorts", "category": "summer_clothing", "price": 39.99, "margin": 0.55},
            {"name": "TechPro Wireless Earbuds", "category": "electronics", "price": 159.99, "margin": 0.35},
            {"name": "ComfortZone Throw Pillow", "category": "home_goods", "price": 24.99, "margin": 0.60},
            {"name": "AdventureMax Hiking Boots", "category": "outdoor_equipment", "price": 199.99, "margin": 0.42}
        ]
        
        performance_data = []
        for product in products:
            units_sold = random.randint(50, 500)
            returns = int(units_sold * random.uniform(0.02, 0.12))
            
            performance_data.append({
                "product_name": product["name"],
                "category": product["category"],
                "price": product["price"],
                "units_sold_30d": units_sold,
                "revenue_30d": round(units_sold * product["price"], 2),
                "profit_margin": product["margin"],
                "return_rate": round(returns / units_sold * 100, 2),
                "customer_rating": round(random.uniform(3.8, 4.9), 1),
                "inventory_turns": round(random.uniform(4, 12), 1)
            })
        
        return performance_data
    
    def _generate_production_data(self):
        """Generate manufacturing production data"""
        machines = ["Line_A", "Line_B", "Line_C", "Line_D"]
        base_date = datetime.now() - timedelta(days=30)
        
        production_records = []
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            
            for machine in machines:
                # Simulate machine performance degradation over time
                age_factor = random.uniform(0.95, 1.0) if "Line_A" == machine else random.uniform(0.85, 1.0)
                
                planned_production = 1000
                actual_production = int(planned_production * age_factor * random.uniform(0.92, 1.05))
                downtime_hours = random.uniform(0, 4) if random.random() < 0.3 else 0
                
                oee = (actual_production / planned_production) * (24 - downtime_hours) / 24
                
                production_records.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "machine_line": machine,
                    "planned_production": planned_production,
                    "actual_production": actual_production,
                    "efficiency_percent": round(actual_production / planned_production * 100, 2),
                    "downtime_hours": round(downtime_hours, 2),
                    "oee_score": round(oee, 3),
                    "quality_score": round(random.uniform(0.94, 0.99), 4)
                })
        
        return production_records[:20]  # Sample for demo
    
    def _generate_quality_data(self):
        """Generate quality control data"""
        defect_types = ["surface_finish", "dimensional", "material", "assembly", "electrical"]
        
        quality_records = []
        for i in range(50):
            defect_type = random.choice(defect_types)
            
            # Correlate defects with environmental factors
            humidity_during_production = random.uniform(35, 85)
            temperature_during_production = random.uniform(18, 28)
            
            # Higher humidity increases certain defect types
            defect_probability = 0.05
            if defect_type == "surface_finish" and humidity_during_production > 70:
                defect_probability = 0.18
            elif defect_type == "dimensional" and temperature_during_production > 25:
                defect_probability = 0.12
            
            quality_records.append({
                "batch_id": f"BATCH-{random.randint(1000, 9999)}",
                "production_line": f"Line_{random.choice(['A', 'B', 'C', 'D'])}",
                "defect_type": defect_type,
                "defect_rate": round(defect_probability, 4),
                "humidity_percent": round(humidity_during_production, 1),
                "temperature_c": round(temperature_during_production, 1),
                "units_inspected": random.randint(500, 1000),
                "defective_units": int(random.randint(500, 1000) * defect_probability),
                "inspector": f"Inspector_{random.randint(1, 8)}"
            })
        
        return quality_records[:20]
    
    def _generate_maintenance_data(self):
        """Generate equipment maintenance data"""
        equipment = ["Conveyor_1", "Robot_Arm_2", "Press_Machine_3", "Quality_Scanner_4", "Packaging_Unit_5"]
        
        maintenance_records = []
        for equipment_name in equipment:
            # Simulate predictive maintenance patterns
            vibration_level = random.uniform(0.5, 3.2)
            temperature = random.uniform(45, 85)
            
            # Correlate maintenance needs with sensor readings
            maintenance_urgency = "low"
            if vibration_level > 2.5 or temperature > 75:
                maintenance_urgency = "high"
            elif vibration_level > 1.8 or temperature > 65:
                maintenance_urgency = "medium"
            
            days_since_maintenance = random.randint(1, 180)
            predicted_failure_days = max(5, 200 - (vibration_level * 30) - (temperature * 0.8) - (days_since_maintenance * 0.5))
            
            maintenance_records.append({
                "equipment_id": equipment_name,
                "vibration_level": round(vibration_level, 2),
                "operating_temperature": round(temperature, 1),
                "days_since_maintenance": days_since_maintenance,
                "maintenance_urgency": maintenance_urgency,
                "predicted_failure_days": int(predicted_failure_days),
                "maintenance_cost_estimate": random.randint(500, 5000),
                "downtime_risk_hours": random.randint(2, 48) if maintenance_urgency == "high" else random.randint(0, 8)
            })
        
        return maintenance_records
    
    def _generate_supply_chain_data(self):
        """Generate supply chain performance data"""
        suppliers = ["MetalCorp Inc", "PlasticPro Ltd", "ElectroSupply Co", "PackageMaster", "ComponentSource"]
        
        supply_records = []
        for supplier in suppliers:
            # Simulate supplier performance metrics
            on_time_delivery = random.uniform(0.75, 0.98)
            quality_rating = random.uniform(0.85, 0.99)
            cost_competitiveness = random.uniform(0.8, 1.2)  # 1.0 = market average
            
            supply_records.append({
                "supplier_name": supplier,
                "on_time_delivery_rate": round(on_time_delivery, 3),
                "quality_rating": round(quality_rating, 3),
                "cost_index": round(cost_competitiveness, 2),
                "lead_time_days": random.randint(7, 45),
                "order_accuracy": round(random.uniform(0.92, 0.998), 3),
                "total_orders_ytd": random.randint(50, 300),
                "defect_rate": round(random.uniform(0.001, 0.05), 4),
                "supplier_score": round((on_time_delivery + quality_rating + (2 - cost_competitiveness)) / 3, 3)
            })
        
        return supply_records
    
    def _generate_risk_data(self):
        """Generate financial risk assessment data"""
        risk_categories = ["credit_risk", "market_risk", "operational_risk", "liquidity_risk", "compliance_risk"]
        
        risk_records = []
        for category in risk_categories:
            base_date = datetime.now() - timedelta(days=7)
            
            for day in range(7):
                current_date = base_date + timedelta(days=day)
                
                # Simulate market volatility affecting risk scores
                market_volatility = random.uniform(0.8, 1.3)
                base_risk_score = random.uniform(0.1, 0.4)
                adjusted_risk_score = min(1.0, base_risk_score * market_volatility)
                
                risk_records.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "risk_category": category,
                    "risk_score": round(adjusted_risk_score, 4),
                    "risk_level": "high" if adjusted_risk_score > 0.7 else "medium" if adjusted_risk_score > 0.4 else "low",
                    "market_volatility_factor": round(market_volatility, 3),
                    "portfolio_exposure": random.randint(100000, 10000000),
                    "mitigation_actions": random.randint(0, 5)
                })
        
        return risk_records[:15]
    
    def _generate_transaction_data(self):
        """Generate customer transaction data"""
        transaction_types = ["deposit", "withdrawal", "transfer", "payment", "investment"]
        
        transactions = []
        for i in range(100):
            transaction_type = random.choice(transaction_types)
            
            # Simulate suspicious pattern detection
            amount = random.uniform(10, 50000)
            is_suspicious = False
            
            # Flag large round numbers as potentially suspicious
            if amount > 10000 and amount % 1000 == 0:
                is_suspicious = random.random() < 0.15
            
            # Flag unusual patterns
            if transaction_type == "withdrawal" and amount > 25000:
                is_suspicious = random.random() < 0.25
            
            transactions.append({
                "transaction_id": f"TXN-{random.randint(100000, 999999)}",
                "customer_id": f"CUST-{random.randint(1000, 9999)}",
                "transaction_type": transaction_type,
                "amount": round(amount, 2),
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
                "is_suspicious": is_suspicious,
                "risk_score": round(random.uniform(0.1, 0.9) if is_suspicious else random.uniform(0.0, 0.3), 4),
                "geographic_risk": random.choice(["low", "medium", "high"]),
                "fraud_probability": round(random.uniform(0.8, 0.95) if is_suspicious else random.uniform(0.0, 0.2), 4)
            })
        
        return transactions[:25]
    
    def _generate_market_data(self):
        """Generate market condition data"""
        market_indicators = ["S&P_500", "VIX", "USD_EUR", "10Y_Treasury", "Gold_Price"]
        
        market_records = []
        base_date = datetime.now() - timedelta(days=30)
        
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            
            # Simulate market volatility
            volatility_factor = random.uniform(0.95, 1.08)
            
            for indicator in market_indicators:
                base_values = {
                    "S&P_500": 4200,
                    "VIX": 20,
                    "USD_EUR": 1.08,
                    "10Y_Treasury": 4.5,
                    "Gold_Price": 2000
                }
                
                value = base_values[indicator] * volatility_factor * random.uniform(0.98, 1.02)
                
                market_records.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "indicator": indicator,
                    "value": round(value, 4),
                    "daily_change_percent": round(random.uniform(-2.5, 2.5), 3),
                    "volatility_index": round(volatility_factor, 3)
                })
        
        return market_records[:25]
    
    def _generate_regulatory_data(self):
        """Generate regulatory compliance data"""
        regulations = ["GDPR", "CCPA", "SOX", "Basel_III", "MiFID_II"]
        
        compliance_records = []
        for regulation in regulations:
            compliance_score = random.uniform(0.85, 0.99)
            
            compliance_records.append({
                "regulation": regulation,
                "compliance_score": round(compliance_score, 4),
                "last_audit_date": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
                "findings_count": random.randint(0, 8),
                "critical_findings": random.randint(0, 2),
                "remediation_status": random.choice(["complete", "in_progress", "pending"]),
                "next_review_date": (datetime.now() + timedelta(days=random.randint(30, 180))).strftime("%Y-%m-%d")
            })
        
        return compliance_records
    
    def export_scenarios_to_json(self):
        """Export all scenarios to JSON file"""
        print("💾 Exporting scenarios to JSON...")
        
        with open("demo_scenarios.json", "w") as f:
            json.dump(self.scenarios, f, indent=2, default=str)
        
        print("✅ Demo scenarios exported to demo_scenarios.json")
        
        # Create summary report
        self._create_scenario_summary()
        
    def _create_scenario_summary(self):
        """Create a summary report of all scenarios"""
        summary = {
            "executive_summary": {
                "total_scenarios": len(self.scenarios) - 1,  # Exclude cross_domain_insights
                "industries_covered": ["E-commerce", "Manufacturing", "Financial Services"],
                "key_value_propositions": [
                    "95% reduction in time-to-insight",
                    "Discover correlations impossible with siloed data",
                    "Quantifiable ROI with specific dollar amounts",
                    "Real-time predictive insights"
                ]
            },
            "business_impact_summary": {
                "ecommerce": {
                    "annual_savings": "$2.3M",
                    "efficiency_gains": "95% faster insights",
                    "key_metric": "23% weather-sales correlation"
                },
                "manufacturing": {
                    "annual_savings": "$1.2M",
                    "efficiency_gains": "35% downtime reduction",
                    "key_metric": "89% equipment failure prediction accuracy"
                },
                "financial_services": {
                    "annual_savings": "$3.8M",
                    "efficiency_gains": "99% faster risk detection",
                    "key_metric": "91% fraud detection accuracy"
                }
            },
            "demo_readiness_checklist": [
                "✅ Industry-specific datasets generated",
                "✅ Realistic correlation patterns created",
                "✅ ROI calculations with specific dollar amounts",
                "✅ Compelling narrative flows defined",
                "🔄 Dashboard visualizations (in progress)",
                "🔄 Video recordings (pending)",
                "🔄 Presentation materials (pending)"
            ]
        }
        
        with open("scenario_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print("📊 Scenario summary exported to scenario_summary.json")

def main():
    """Main function to create all demo scenarios"""
    creator = DemoScenariosCreator()
    
    print("🎭 Demo Scenarios Creator")
    print("=" * 50)
    
    # Create all scenarios
    scenarios = creator.create_all_scenarios()
    
    # Export to JSON
    creator.export_scenarios_to_json()
    
    print("\n🎉 Demo scenarios creation complete!")
    print("\nGenerated files:")
    print("- demo_scenarios.json (complete scenario data)")
    print("- scenario_summary.json (executive summary)")
    
    print("\nScenarios created:")
    for key, scenario in scenarios.items():
        if key != "cross_domain_insights":
            print(f"- {scenario['title']}")
        else:
            print(f"- Cross-Domain Intelligence Discovery")
    
    print("\nNext steps:")
    print("1. Review scenario data and narratives")
    print("2. Create dashboard visualizations for each scenario")
    print("3. Record demo videos")
    print("4. Prepare presentation materials")
    print("5. Schedule stakeholder demonstrations")

if __name__ == "__main__":
    main()

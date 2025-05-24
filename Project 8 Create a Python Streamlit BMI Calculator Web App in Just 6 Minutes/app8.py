import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF, HTMLMixin
from datetime import datetime
import numpy as np
import io
import base64

# Custom CSS for premium styling
def inject_custom_css():
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 3rem;
            border-radius: 15px;
        }
        .section {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background: linear-gradient(to right, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.7rem 1.5rem;
            border-radius: 25px;
            font-size: 1rem;
        }
        .health-metric {
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Enhanced PDF Report with HTML support
class HealthReport(FPDF, HTMLMixin):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Comprehensive Health Assessment', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Health Calculations
def calculate_health_metrics(data):
    # BMI Calculation
    height_m = data['height'] / 100
    data['bmi'] = round(data['weight'] / (height_m ** 2), 1)
    
    # Body Fat Percentage (Navy Method)
    if data['gender'] == 'Male':
        data['body_fat'] = round(86.010 * np.log10(data['waist'] - data['neck']) - 70.041 * np.log10(data['height']) + 36.76, 1)
    else:
        data['body_fat'] = round(163.205 * np.log10(data['waist'] + data['hips'] - data['neck']) - 97.684 * np.log10(data['height']) - 78.387, 1)
    
    # BMR (Harris-Benedict Equation)
    if data['gender'] == 'Male':
        data['bmr'] = round(88.362 + (13.397 * data['weight']) + (4.799 * data['height']) - (5.677 * data['age']))
    else:
        data['bmr'] = round(447.593 + (9.247 * data['weight']) + (3.098 * data['height']) - (4.330 * data['age']))
    
    return data

# Generate comprehensive PDF report
def generate_full_report(data):
    pdf = HealthReport()
    pdf.add_page()
    
    # Cover Page
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 20, "Personal Health Report", 0, 1, 'C')
    pdf.ln(15)
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%B %d, %Y')}", 0, 1, 'C')
    pdf.ln(20)
    
    # Page 2: Personal Information
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "1. Personal Information", 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, "Name:", 0, 0)
    pdf.cell(0, 10, data['name'], 0, 1)
    pdf.cell(40, 10, "Age:", 0, 0)
    pdf.cell(0, 10, str(data['age']), 0, 1)
    pdf.cell(40, 10, "Gender:", 0, 0)
    pdf.cell(0, 10, data['gender'], 0, 1)
    pdf.ln(10)
    
    # Page 3: Health Metrics
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "2. Health Metrics Analysis", 0, 1)
    pdf.ln(5)
    
    metrics = [
        ("BMI", str(data['bmi']), "18.5-24.9", "Weight-to-height ratio"),
        ("Body Fat %", f"{data['body_fat']}%", "Male: 8-19%, Female: 21-33%", "Adipose tissue percentage"),
        ("BMR", f"{data['bmr']} kcal", "Varies by individual", "Basal Metabolic Rate")
    ]
    
    for metric in metrics:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, metric[0], 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(30, 10, metric[1], 0, 0)
        pdf.cell(50, 10, f"Normal Range: {metric[2]}", 0, 0)
        pdf.cell(0, 10, metric[3], 0, 1)
        pdf.ln(3)
    
    # Page 4: Charts
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "3. Health Trends", 0, 1)
    
    # Generate sample chart
    plt.figure(figsize=(6, 3))
    plt.bar(['BMI', 'Body Fat', 'BMR'], [data['bmi'], data['body_fat'], data['bmr']/100])
    plt.title('Health Metrics Comparison')
    plt.tight_layout()
    
    # Save chart to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Add image from buffer
    pdf.image(buf, x=30, w=150)
    
    # Page 5: Recommendations
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "4. Personalized Recommendations", 0, 1)
    pdf.ln(5)
    
    recommendations = [
        ("Nutrition", "Increase vegetable intake to 5 servings/day"),
        ("Exercise", "30 minutes cardio 5x/week"),
        ("Sleep", "Maintain 7-9 hours nightly"),
        ("Stress", "Practice mindfulness 10 min/day")
    ]
    
    for rec in recommendations:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(30, 10, rec[0], 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, rec[1])
        pdf.ln(2)
    
    # Return as bytes (not bytearray)
    return bytes(pdf.output(dest='S'))

# Main Application
def main():
    inject_custom_css()
    
    st.title("Comprehensive Health Assessment")
    st.markdown("Complete this form to generate your personalized health report")
    
    # Initialize session state
    if 'health_data' not in st.session_state:
        st.session_state.health_data = None
    
    with st.form("health_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", key="name")
            age = st.number_input("Age", min_value=5, max_value=120, value=30, key="age")
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
            email = st.text_input("Email (optional)", key="email")
        
        st.subheader("Body Measurements")
        col1, col2, col3 = st.columns(3)
        with col1:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=70.0, key="weight")
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, key="height")
        with col2:
            waist = st.number_input("Waist Circumference (cm)", min_value=50.0, max_value=200.0, value=80.0, key="waist")
            neck = st.number_input("Neck Circumference (cm)", min_value=20.0, max_value=50.0, value=35.0, key="neck")
        with col3:
            hips = st.number_input("Hips Circumference (cm) (Women)", min_value=50.0, max_value=200.0, value=95.0, key="hips")
        
        st.subheader("Lifestyle Factors")
        activity = st.selectbox("Activity Level", [
            "Sedentary (little/no exercise)",
            "Lightly active (light exercise 1-3 days/week)",
            "Moderately active (moderate exercise 3-5 days/week)",
            "Very active (hard exercise 6-7 days/week)",
            "Extremely active (very hard exercise & physical job)"
        ], key="activity")
        
        col1, col2 = st.columns(2)
        with col1:
            sleep = st.number_input("Average Sleep (hours/night)", min_value=0, max_value=24, value=7, key="sleep")
        with col2:
            water = st.number_input("Water Intake (glasses/day)", min_value=0, max_value=20, value=8, key="water")
        
        submitted = st.form_submit_button("Generate Comprehensive Health Report")
        
        if submitted:
            # Collect all data
            health_data = {
                'name': name,
                'age': age,
                'gender': gender,
                'email': email,
                'weight': weight,
                'height': height,
                'waist': waist,
                'neck': neck,
                'hips': hips,
                'activity': activity,
                'sleep': sleep,
                'water': water,
                'report_date': datetime.now().strftime("%B %d, %Y")
            }
            
            # Calculate health metrics
            health_data = calculate_health_metrics(health_data)
            
            # Store in session state
            st.session_state.health_data = health_data
    
    if st.session_state.health_data:
        # Generate PDF
        pdf_bytes = generate_full_report(st.session_state.health_data)
        
        # Show summary
        with st.expander("Preview Key Metrics", expanded=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("BMI", st.session_state.health_data['bmi'], "Normal: 18.5-24.9")
            col2.metric("Body Fat %", f"{st.session_state.health_data['body_fat']}%", 
                        "Male: 8-19%, Female: 21-33%")
            col3.metric("BMR", f"{st.session_state.health_data['bmr']} kcal/day", "Calories at rest")
        
        # Download button
        st.download_button(
            label="📄 Download Full Health Report (PDF)",
            data=pdf_bytes,
            file_name=f"health_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
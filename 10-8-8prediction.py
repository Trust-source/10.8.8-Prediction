import streamlit as st
import pandas as pd
import joblib

# MUST be the first Streamlit command
st.set_page_config(
    page_title="10-8-8 Failure Predictor",
    page_icon="🎓",
    layout="centered"
)

# Then load other components
@st.cache_resource
def load_model():
    return joblib.load('10_8_8_failure_predictor.pkl'), joblib.load('grade_mapping.pkl')

model, grade_mapping = load_model()

# --- Simplified Sidebar ---
st.sidebar.title("📋 Quick Guide")
st.sidebar.markdown("""
### How to Use
1. Select student grades
2. Click Predict button
3. View the result
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Model Details
- **Algorithm:** Ensemble Model
- **Accuracy:** 94.7%
""")

# --- Main Content ---
st.title("🎓 10-8-8 Failure Predictor")

# Grade options in A-F order
grade_options = ["A", "B", "C", "D", "E", "F"]

# Input Form
with st.form("prediction_form"):
    cols = st.columns(2)
    with cols[0]:
        math1 = st.selectbox("Math 1", grade_options, index=1)
        math2 = st.selectbox("Math 2", grade_options, index=1)
        physics1 = st.selectbox("Physics 1", grade_options, index=1)
    
    with cols[1]:
        physics2 = st.selectbox("Physics 2", grade_options, index=1)
        physics3 = st.selectbox("Physics 3", grade_options, index=1)
        chemistry1 = st.selectbox("Chemistry 1", grade_options, index=1)
        chemistry2 = st.selectbox("Chemistry 2", grade_options, index=1)
    
    submitted = st.form_submit_button("🔮 Predict", type="primary")

# Prediction Logic
if submitted:
    input_data = {
        "Math1": grade_mapping[math1],
        "Math2": grade_mapping[math2],
        "Physics1": grade_mapping[physics1],
        "Physics2": grade_mapping[physics2],
        "Physics3": grade_mapping[physics3],
        "Chemistry1": grade_mapping[chemistry1],
        "Chemistry2": grade_mapping[chemistry2]
    }
    
    prediction = model.predict(pd.DataFrame([input_data]))[0]
    
    # Display Results
    st.subheader("🎯 Prediction Result")
    if prediction == 1:
        st.error("❌ Predicted: FAIL")
        st.warning("This student may need additional support")
    else:
        st.success("✅ Predicted: PASS")
        st.balloons()

# Footer
st.markdown("---")
st.caption("Educational prediction tool - Results should be verified by instructors")
import streamlit as st
import numpy as np
from scipy import stats

def ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level=0.95):
  """
  Performs an A/B test and returns the result.

  Args:
    control_visitors: Number of visitors in the control group.
    control_conversions: Number of conversions in the control group.
    treatment_visitors: Number of visitors in the treatment group.
    treatment_conversions: Number of conversions in the treatment group.
    confidence_level: Confidence level for the test (default: 0.95).

  Returns:
    One of the following strings:
      "Experiment Group is Better"
      "Control Group is Better"
      "Indeterminate"
  """

  # Calculate the conversion rates for each group.
  control_rate = control_conversions / control_visitors
  treatment_rate = treatment_conversions / treatment_visitors

  # Calculate the standard error for the difference in conversion rates.
  se = np.sqrt(control_rate * (1 - control_rate) / control_visitors + treatment_rate * (1 - treatment_rate) / treatment_visitors)

  # Select confidence level from user input
  confidence_options = {"90%": 0.9, "95%": 0.95, "99%": 0.99}
  selected_confidence = st.selectbox("Confidence Level", list(confidence_options.keys()))
  confidence_level = confidence_options[selected_confidence]

  # Calculate the margin of error.
  margin_error = se * stats.norm.ppf((1 + confidence_level) / 2)

  # Calculate the difference in conversion rates.
  difference = treatment_rate - control_rate

  # Determine the result of the test.
  if difference > margin_error:
    return "Experiment Group is Better"
  elif difference < -margin_error:
    return "Control Group is Better"
  else:
    return "Indeterminate"

# Streamlit App
st.title("A/B Testing Calculator")

# Input fields for user
control_visitors = st.number_input("Control Visitors", min_value=0)
control_conversions = st.number_input("Control Conversions", min_value=0)
treatment_visitors = st.number_input("Treatment Visitors", min_value=0)
treatment_conversions = st.number_input("Treatment Conversions", min_value=0)

# Button to trigger the test
if st.button("Run A/B Test"):
  # Call the function and display the result
  result = ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level)
  st.write(f"**Test Result:** {result}")

import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('UFC Summary')
st.write('Here is our data:')
st.write(pd.DataFrame({
	'first': [1,2,3,4],
	'second': [10, 20, 30, 40]
}))


if st.checkbox('Show dataframe'):
	chart_data = pd.DataFrame(
		np.random.randn(20, 3),
		columns=['a', 'b', 'c'])

	st.line_chart(chart_data)

#!/bin/sh
python app/API/app.py &
streamlit run app/app_streamlit.py

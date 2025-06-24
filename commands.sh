#!/bin/bash

# Lancer FastAPI en arrière-plan
fastapi dev main.py &

# Lancer Streamlit en arrière-plan
streamlit run front_end/app.py & 
from flask import render_template, flash, redirect, request, jsonify
from app import app
from functions import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Index')

@app.route('/zfactor', methods=['POST'])
def zfactor():
    molars = list(map(float, request.form['molars'].split()))
    temperatures = list(map(float, request.form['temperatures'].split()))
    pressures = list(map(float, request.form['pressures'].split()))

    data = [[molars[i], temperatures[i], pressures[i]] for i in range(len(molars))]

    T_system = float(request.form['tSystem'])
    P_system = float(request.form['pSystem'])

    T_c = get_pseudo_critical_temperature(data)
    P_c = get_pseudo_critical_pressure(data)

    P_pr = get_pseudo_reduced_value(P_system, P_c)
    T_pr = get_pseudo_reduced_value(T_system, T_c)

    z = get_z_factor(T_pr, P_pr)

    return jsonify({"result" : str(z.real) })
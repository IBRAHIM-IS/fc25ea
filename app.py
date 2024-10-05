from flask import Flask, render_template, redirect, request
import pickle
import pandas as pd
import numpy as np

pipe = pickle.load(open("finalized_model.pickle", 'rb'))

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home_page():
    if(request.method == 'POST'):
        PAC = request.form['PAC']
        SHO = request.form['SHO']
        DRI = request.form['DRI']
        PAS = request.form['PAS']
        DEF = request.form['DEF']
        PHY = request.form['PHY']
        position = request.form['position']

        # Validate input
        if PAC == "" or SHO == "" or DRI == "" or PAS == "" or DEF == "" or PHY == "" or position == "":
            return(render_template("index.html", prediction=-2))

        try:
            # Check for valid input ranges
            if float(PAC) > 99 or float(SHO) > 99 or float(PAS) > 99 or float(DRI) > 99 or float(DEF) > 99 or float(PHY) > 99 :
                return(render_template("index.html", prediction=-2))

            # Initialize weights based on position
            weights = {'PAC': 0, 'SHO': 0, 'DRI': 0, 'PAS': 0, 'DEF': 0, 'PHY' : 0}

            if position == '1':  # RB or LB
                weights['DEF'] = 3
                weights['PAC'] = 2
                weights['DRI'] = 1
                weights['PHY'] = 1
                weights['SHO'] = 1

            elif position == '2':  # CB
                weights['DEF'] = 4
                weights['PHY'] = 2
                weights['PAS'] = 1
                weights['PAC'] = 1

            elif position == '3':  # CM
                weights['PAS'] = 3
                weights['DRI'] = 2
                weights['PHY'] = 2

            elif position == '4':  # ST
                weights['SHO'] = 3
                weights['PAC'] = 2
                weights['DRI'] = 1
                weights['PHY'] = 1
                weights['PAS'] = 1

            elif position == '5':  # RW or LW
                weights['PAC'] = 3
                weights['SHO'] = 2
                weights['DRI'] = 2
                weights['PAS'] = 2
                weights['PHY'] = 1

            elif position == '6':  # CDM
                weights['DEF'] = 3
                weights['PHY'] = 2
                weights['PAS'] = 2
                weights['PAC'] = 1
                weights['SHO'] = 1

            elif position == '7':  # CAM
                weights['PAS'] = 3
                weights['DRI'] = 3
                weights['SHO'] = 2
                weights['PAC'] = 1
                weights['DEF'] = 1

            # Calculate the weighted total
            total = (float(PAC) * weights['PAC'] +
                     float(SHO) * weights['SHO'] +
                     float(DRI) * weights['DRI'] +
                     float(PAS) * weights['PAS'] +
                     float(DEF) * weights['DEF'] +
                     float(DEF) * weights['PHY'] )

            # Normalize by the total weight
            total_weight = sum(weights.values())
            if total_weight == 0:
                return(render_template("index.html", prediction=-2))

            average = total / total_weight

        except Exception as e:

            # Ensure the average does not exceed the maximum, but output without percentage
            if average > 100.0:
                average = 100

            return(render_template("index.html", prediction=-2))

        return(render_template("index.html", prediction=round(average, 2)))  # No percentage sign

    return render_template('index.html', prediction=-1)

if __name__ == '__main__':
    app.run(debug=True)

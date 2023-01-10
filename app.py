
from flask import Flask, render_template, request ,flash ,redirect, url_for
import pickle
import pandas as pd



filename = 'first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))




app = Flask(__name__)
app.config['SECRET_KEY'] = 'ljadfnjbf'

@app.route('/')
def home():


	return render_template('index.html')


@app.route('/predict', methods=['POST'])


def predict():
        
    if request.method == 'POST':
            
        batting_team = request.form['batting-team']

        bowling_team = request.form['bowling-team']

        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])

        try:
            if  batting_team == bowling_team:
                flash('batting team & bowling team should not be same')  
                return redirect(url_for('home'))

            elif batting_team == 'none':

                flash('batting team should notnull ')  
                return redirect(url_for('home'))


            elif bowling_team == 'none':

                flash('bowling team should notnull')
                return redirect(url_for('home'))
            
            elif runs <0 :
            
                flash('runs shound not be less than 0')
                return redirect(url_for('home'))   

            elif runs_in_prev_5 <0 :
            
                flash('runs in previous 5 overs shound not be less than 0')
                return redirect(url_for('home'))   

            elif overs <4  or overs>21:
            
                flash('overs shound not be greater than 5 or less than 21')
                return redirect(url_for('home'))    



            elif wickets < 0:

                flash('wickets shound not be less than 0 ')
                return redirect(url_for('home')) 

            elif  wickets_in_prev_5 < 0 :

                flash('wickets in previous 5 overs shound not be less than 0 ')
                return redirect(url_for('home')) 


            elif runs < runs_in_prev_5:

                flash('runs in previous 5 overs should not be greater than current runs ')
                return redirect(url_for('home'))


            elif wickets < wickets_in_prev_5:

                flash('wickets in previous 5  overs should not be greater than current wickets ')
                return redirect(url_for('home')) 


            elif wickets>11:

                flash('wickets count should not greater than 10 ')
                return redirect(url_for('home'))
            

            elif  wickets_in_prev_5>11:

                flash('wickets in previous 5 overs count should not greater than 10 ')
                return redirect(url_for('home'))
            else:

                
                data = pd.DataFrame([[batting_team,bowling_team ,runs,wickets,overs, runs_in_prev_5, wickets_in_prev_5]],columns=['bat_team','bowl_team','runs','wickets','overs','runs_last_5','wickets_last_5'])
                print(data)

                my_prediction = int(regressor.predict(data)[0])

                
                return render_template('result.html', lower_limit = my_prediction-10, upper_limit = my_prediction, )

        except Exception as e:
            print(e)


if __name__ == '__main__':
	app.run(debug=True)
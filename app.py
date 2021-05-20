
from flask import Flask, render_template, url_for,request,redirect
app = Flask(__name__)
import requests
from datetime import datetime
from getData import districtData,stateData,districtDataState

@app.route("/")
@app.route("/home")
def home():
    sd = stateData()
    return render_template('home.html',sd = sd)

@app.route("/main")
def main():
    return render_template('main.html')

@app.route("/states",methods = ['POST','GET'])
def states():
    if request.method == 'POST':
      state = request.form['state']
      print(state)
      return redirect(url_for('stateDistrict',state = state))

    sd = stateData()
    return render_template('states.html',sd = sd)

@app.route("/search", methods=['GET', 'POST'])
def search():
   if request.method == 'POST':
      city = request.form['city']
      return redirect(url_for('result',city = city))

   return render_template('search.html')


@app.route("/result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        city = request.form['city']


        return redirect(url_for('result',city = city))

    # Getting variables form search and passing it to the Result page
    city = request.args.get('city')
    dData = districtData(city.strip().title())

    sd = stateData()
    try: 
        return render_template('result.html',city = city,dData= dData,sd =sd)
    except UnboundLocalError:
        return redirect(url_for('notFound',city = city))   

@app.route('/districts-state',methods = ['GET','POST'])
def stateDistrict():
    if request.method == 'POST':
        state = request.form['state']


        return redirect(url_for('stateDistrict',state = state))    
    state = request.args.get('state')
    dData = districtDataState(state.title().strip())
    try:
        return render_template('stateDistricts.html',state = state,dData = dData)
    except KeyError:
        return redirect(url_for('StatenotFound',state = state))    

# @app.route('/all-district-data')
# def allData():

#     dData = districtDataState()
#     return render_template('allDistricts.html',dData = dData,states = states)    

@app.route('/not-Found',methods = ['GET','POST'])
def notFound():
   if request.method == 'POST':
      city = request.form['city']


      return redirect(url_for('result',city = city))  

   city = request.args.get('city')
   return render_template('ERROR.html',city = city)


@app.route('/not-Found-State',methods = ['GET','POST'])
def StatenotFound():
   if request.method == 'POST':
      state = request.form['state']

      return redirect(url_for('stateDistrict',state = state))  

   state = request.args.get('state')
   return render_template('errorState.html',state = state)



if __name__ == '__main__':
    app.run(debug = False)
from flask import Flask, render_template, request
import pandas as pd
import pickle


app = Flask(__name__)
model = pickle.load(open("picklefile.pkl", 'rb',))
car= pd.read_csv('Cleaned Car.csv')

@app.route('/')
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()
    return render_template('index.html', companies=companies, car_models=car_models, years = years, fuel_type=fuel_type)

@app.route('/predict',methods=['POST'])
def predict():
    company = request.form.get('company')
    car_model = request.form.get('car_model')
    year = int(request.form.get('years'))
    fuel_type = request.form.get('fuel_type')
    kms_driven = int(request.form.get('kilo_driven'))
    print(company, car_model, year, fuel_type, kms_driven)
    
    pred = model.predict(pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]], columns=['name','company','year','kms_driven','fuel_type']))
    print(pred)
    rounded_number = round(pred[0], 3)
    return str(rounded_number)


if __name__ == "__main__":
    app.run(debug=True)
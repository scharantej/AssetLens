
# Import the necessary libraries
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Create a Flask application
app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def index():
    # Render the HTML template for the home page
    return render_template('index.html')


# Define the route for the API endpoint to retrieve the historical values of the assets
@app.route('/api/asset_data', methods=['GET'])
def get_asset_data():
    # Retrieve the asset name and time range from the request parameters
    asset_name = request.args.get('asset_name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Query the database to fetch the historical values of the asset
    asset_data = pd.read_sql(f"""
        SELECT *
        FROM asset_data
        WHERE asset_name = '{asset_name}'
        AND date >= '{start_date}'
        AND date <= '{end_date}'
    """, con=db_connection)

    # Convert the Pandas DataFrame to a JSON object
    json_data = asset_data.to_json(orient='records')

    # Return the JSON object as the response
    return jsonify(json_data)


# Define the route for the API endpoint to generate insights
@app.route('/api/insights', methods=['GET'])
def get_insights():
    # Retrieve the asset name from the request parameters
    asset_name = request.args.get('asset_name')

    # Query the database to fetch the historical values of the asset
    asset_data = pd.read_sql(f"""
        SELECT *
        FROM asset_data
        WHERE asset_name = '{asset_name}'
    """, con=db_connection)

    # Generate insights based on the historical values of the asset
    insights = generate_insights(asset_data)

    # Convert the insights to a JSON object
    json_data = insights.to_json(orient='records')

    # Return the JSON object as the response
    return jsonify(json_data)


# Define the function to generate insights
def generate_insights(asset_data):
    # Calculate the mean and standard deviation of the asset values
    mean_value = asset_data['value'].mean()
    std_dev = asset_data['value'].std()

    # Create a scatter plot of the asset values over time
    plt.scatter(asset_data['date'], asset_data['value'])
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title(f'Historical Values of {asset_name}')

    # Fit a linear regression model to the asset values
    model = LinearRegression()
    model.fit(asset_data['date'].values.reshape(-1, 1), asset_data['value'].values)

    # Calculate the R-squared value of the model
    r_squared = model.score(asset_data['date'].values.reshape(-1, 1), asset_data['value'].values)

    # Create a dataframe of the insights
    insights = pd.DataFrame({
        'Metric': ['Mean Value', 'Standard Deviation', 'R-Squared'],
        'Value': [mean_value, std_dev, r_squared]
    })

    # Return the dataframe of insights
    return insights


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

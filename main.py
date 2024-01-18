from flask import Flask, request, jsonify, send_file
from flask import request
import pandas as pd 
import matplotlib.pyplot as plt 
from io import BytesIO


app = Flask(__name__)

# returns the overall trend of programming language over the years

@app.route("/api/trends", methods=['GET'])
def find_trends():
    df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], skiprows= 1, header=0)
    df.DATE = pd.to_datetime(df.DATE)
    table = df.pivot_table(index='DATE', columns='TAG', values='POSTS').fillna(0)
    table.index = table.index.strftime('%Y-%m-%d')
    return jsonify(table.to_dict())

# returns the specific tren for each programming language over the years
@app.route("/api/trends/image", methods=['GET'])
def find_trends_image():
    df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], skiprows= 1, header=0)
    df.DATE = pd.to_datetime(df.DATE)
    table = df.pivot_table(index='DATE', columns='TAG', values='POSTS').fillna(0)
    rolling_df = table.rolling(window=6).mean()

    plt.figure(figsize=(15,10)) 
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel('Date',fontsize=12)
    plt.ylabel('Number of posts',fontsize=12)
    plt.ylim(0,30000)


    for column in rolling_df.columns:
        plt.plot(rolling_df.index, rolling_df[column],linewidth=2,label=rolling_df[column].name)
    plt.legend(fontsize=12)

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

    # plt.savefig('graph.png')
    # return send_file('graph.png', mimetype='image/gif')

    

@app.route("/api/trend/<language>", methods=['GET'])
def find_language_trend(language):
    df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
    df.DATE = pd.to_datetime(df.DATE)

    table = df.pivot(index='DATE', columns='TAG', values='POSTS').fillna(0)
    if language in table.columns:
        return jsonify({language: table[language].to_dict()})
    else:
         return jsonify({'error': 'Language not found'}),404 
    
# summarize the data
@app.route("/api/summary", methods=['GET'])
def get_summary():
    df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
    summary = df.groupby('TAG')['POSTS'].sum().to_dict()
    return jsonify(summary)

# return an analysis for any csv file the user enters 


@app.route("/api/analyze", methods=['POST'])
def analyze_data():
    if 'file' not in request.files:
        return jsonify({'error': 'File does not exist'}), 400
    file = request.files(['file'])
    if file.filename == '':
        return jsonify({'error':'No file selected'}),400
    if file:
        df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
        result = df.groupby('TAG').sum().to_dict()
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True,port=8080)





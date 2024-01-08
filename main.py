from flask import Flask, request, jsonify
import pandas as pd 
import matplotlib.pyplot as plt 


app = Flask(__name__)

# returns the overall trend of programming language over the years

@app.route("/api/trends", methods=['GET'])
def find_trends():
    df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
    df.DATE = pd.to_datetime(df.DATE)
    df_int = df.DATE.values
    table = pd.DataFrame(df_int).pivot(index='DATE', columns='TAG', values='POSTS')
    table.fillna(0)

    return jsonify(table.to_dict())

# returns the specific tren for each programming language over the years

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
from flask import request

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



# df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)

# #reading the amount of posts each language has
# df.groupby('TAG').sum()

# #number of months of entries for each language
# df.groupby('TAG').count()

# # looking at the dates and changing the format
# df.DATE[1]
# df.DATE = pd.to_datetime(df.DATE)
# #changes all of the date format 
# df.head()

# #change the order of the table 
# table = df.pivot(index='DATE', columns='TAG', values='POSTS')

# # remove the NaN values 
# table.count()
# table.fillna(0, inplace=True) 
# table.fillna(0)

# table.isna().values.any()

# rolling_df = table.rolling(window=6).mean()

# plt.figure(figsize=(15,10)) 
# plt.xticks(fontsize=11)
# plt.yticks(fontsize=11)
# plt.xlabel('Date',fontsize=12)
# plt.ylabel('Number of posts',fontsize=12)
# plt.ylim(0,30000)


# for column in rolling_df.columns:
#     plt.plot(rolling_df.index, rolling_df[column],linewidth=2,label=rolling_df[column].name)
# plt.legend(fontsize=12)


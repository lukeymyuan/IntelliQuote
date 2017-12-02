import pymongo
import requests
import csv

client = pymongo.MongoClient("mongodb://admin1:Naman123@localhost:27017/admin")
def split_date(date):
    splot = date.split("T")
    return[splot[0].split('-')[0], splot[0].split('-')[1]]

def quote_to_number(quote_type):
    if quote_type == "Bronze": return 0
    if quote_type == "Silver": return 1
    if quote_type == "Gold": return 2
    if quote_type == "Platinum": return 3
    return -1
def worker(filename):
    participant = requests.get("https://v3v10.vitechinc.com/solr/v_participant/select?q=*:*&sort=id asc&rows=1000&wt=json").json()['response']['docs']
    participant_details = requests.get("https://v3v10.vitechinc.com/solr/v_participant_detail/select?q=*:*&sort=id asc&rows=1000&wt=json").json()['response']['docs']
    quotes = requests.get("https://v3v10.vitechinc.com/solr/v_quotes/select?q=*:*&sort=id asc&rows=1000&wt=json").json()['response']['docs']
    for index in range(len(participant)):
        print(participant[index])
        print(participant_details[index])
        print(quotes[index])
        assert participant[index]['id'] == participant_details[index]['id'], "Unordered!"
        assert participant[index]['id'] == quotes[index]['id'], exit(1)

    with open(filename, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        for index in range(len(participant)):
            #preconditions = participant_details[index]['preconitions']
            #preconditions_json = json.parse(preconditions)

            writer.writerow([participant[index]['id']]+[participant[index]['latitude']]+[participant[index]['longitude']]+[1 if participant[index]['sex']=="M" else 0]+\
                            [split_date(participant[index]['DOB'])[0]]+[split_date(participant[index]['DOB'])[1]]\
                            +[1 if participant_details[index]['TOBACCO'] == "Yes" else 0] + [participant_details[index]['ANNUAL_INCOME']] + [participant_details[index]['OPTIONAL_INSURED']] \
                            + [particEpant_details[index]['WEIGHT']]+[participant_details[index]['HEIGHT']]+[0 if participant_details[index]['MARITAL_STATUS'] == "S" else 1] \
                            +[quotes[index]['GOLD']]+[quotes[index]['SILVER']]+[quotes[index]['BRONZE']]+[quote_to_number(quotes[index]['PURCHASED'])]\
                            )
if __name__ == '__main__':
    worker('test.csv')

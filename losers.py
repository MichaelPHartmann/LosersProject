from FinMesh.iex import stock
import datetime
import csv
import pickle

def create_new_pickle():
    with open('losers.pickle', 'wb') as pf:
        losers = []
        pickle.dump(losers, pf, pickle.HIGHEST_PROTOCOL)

def date_file_builder(folder='data'):
    ## Builds a non-slash, easy-to-read date
    today = datetime.datetime.now()
    day = today.strftime('%d')
    month = today.strftime('%b')
    year = today.strftime('%y')
    date = day+month+year
    filename = f"{folder}/{date}.csv"
    return filename

def create_new_file(filename, tickers):
    ## Create a new file with the day's losers and their closing prices
    with open(filename, 'a') as csvf:
        writer = csv.writer(csvf, delimiter=',')
        header_to_write = ['',]
        for tick in tickers:
            header_to_write.append(tick)
        writer.writerow(header_to_write)
        tick_price = []
        for t in range(5):
            symbol = tickers[t]
            price = stock.price(symbol)
            tick_price.append(price)
        date = datetime.datetime.now().strftime('%x')
        prices_to_write = [date]
        for p in tick_price:
            prices_to_write.append(p)
        writer.writerow(prices_to_write)

    # Pickles the results so we can iterate previous days
    with open('losers.pickle', 'ab+') as f:
        pickle.dump(filename,f)

    return filename

def update_files():
    ## Updates already existing files with fresh closing prices
    with open('losers.pickle', 'rb') as f:
        files = pickle.load(f)

    counter = 0
    for filename in files:
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            tickers = header[1:]

        with open(filename, 'a') as csvf:
            writer = csv.writer(csvf, delimiter=' ',quotechar='"')
            tick_price = []
            for t in range(5):
                symbol = tickers[t]
                price = stock.price(symbol)
                tick_price.append(price)
            date = datetime.datetime.now().strftime('%x')
            prices_to_write = [date]
            for p in tick_price:
                prices_to_write.append(p)
            writer.writerow(price_to_write)
        counter += 1

    print(f'Done Updating {counter} files!')

def run():
    tickers_added = 0
    tickers = []
    while tickers_added < 5:
        ticker = input(" Please enter a ticker: ")
        tickers.append(ticker)
        tickers_added +=1
    print('Updating old files!')
    update_files()
    new_filename = date_file_builder()
    print('Building new file')
    create_new_file(new_filename, tickers)
    print('Done!')


if __name__ == '__main__':
    run()

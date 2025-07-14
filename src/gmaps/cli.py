import argparse

from .scraper import run

def main():
    p = argparse.ArgumentParser(prog = 'greview', description = 'Scrape Reviews from Google Maps')
    p.add_argument('-p', '--place-id', required = True, help = 'Google place ID to Scrape')
    p.add_argument('-o', '--outfile', default = 'reviews.csv', help = 'Path to save the csv output')
    args = p.parse_args()
    run(place_id = args.place_id, outfile = args.outfile)

if __name__ == '__main__':
    main()


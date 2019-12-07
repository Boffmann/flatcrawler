from flatcrawler import FlatCrawler
import argparse

if __name__ == "__main__":
    # Parse config
    parser = argparse.ArgumentParser(description='Specify config file')
    parser.add_argument('--config', help='foo help')
    args = parser.parse_args()
    # Start flatcrawler
    flatcrawler = FlatCrawler(config=args.config)
    flatcrawler.run()

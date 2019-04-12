# Robert Bowne Foundation

This repo is for Vipul Naik's Donations List Website: https://github.com/vipulnaik/donations

Specific issue that caused this repo to exist: https://github.com/vipulnaik/donations/issues/99

## Instructions for running the scripts

Get the data:

```bash
./scrape.py > grants.csv
```

Use the data to get the SQL file:

```bash
./proc.py grants.csv > out.sql
```

## License

CC0 for the scripts and readme.

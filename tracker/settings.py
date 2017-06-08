import ConfigParser

DB_DSN = 'postgresql://mariusz:password@127.0.0.1/mariuszdb'

Config = ConfigParser.ConfigParser()
Config.read("test.ini")

d = {}

if Config.sections():

    section = "Test"
    options = Config.options(section)
    for option in options:
        try:
            d[option] = Config.get(section, option)
        except:
            print("exception on %s!" % option)
            d[option] = None

    DB_DSN = 'postgresql://%s:password@%s/%s' \
             % (d['user'], d['host'], d['dbname'])

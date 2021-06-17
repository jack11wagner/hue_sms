import redis
import os


def go():

    r = redis.Redis(
        host='localhost', port=6379, db=0)

    location = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(location + '/hue_log.log') as logs:
        for line in logs:
            line = line.split(':')
            line = line[-1]

            if line.split()[0].lower() == 'color':
                r.hincrby('color_totals', line.split()[1].lower(), 1)


if __name__ == '__main__':
    go()

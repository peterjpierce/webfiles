#!/usr/bin/env python

from webfiles import app


def main():
    app.run(debug=True, host='0.0.0.0', port=48001)


if __name__ == '__main__':
    main()

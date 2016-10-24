import argparse
import sys


def parse_arguments(filename):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', metavar='IDENTITY-FILE', action='store', dest='private_key',
        type=str, help='identity file (private key) for ssh/scp to use')
    parser.add_argument(
        '-r', metavar='REMOTE:DIR', action='store', dest='remote', type=str,
        help='remote pantheon directory: [user@]hostname:dir')

    if filename == 'test.py' or filename == 'run.py':
        parser.add_argument(
            '-f', action='store', dest='flows', type=int, default=1,
            help='number of flows (mm-tunnelclient/mm-tunnelserver pairs)')
        parser.add_argument(
            '-t', action='store', dest='runtime', type=int, default=60,
            help='total runtime of test')
        parser.add_argument(
            '--interval', action='store', dest='interval', type=int,
            default=0, help='interval time between two consecutive flows')

    if filename == 'setup.py':
        parser.add_argument(
            'cc', metavar='mahimahi|congestion-control', type=str,
            help='setup mahimahi before setup any congestion control')
    elif filename == 'test.py':
        parser.add_argument('cc', metavar='congestion-control', type=str,
                            help='name of a congestion control scheme')
    elif filename == 'run.py':
        parser.add_argument(
            '--no-setup', action='store_true', dest='no_setup', default=False,
            help='run tests only without running setup')

    args = parser.parse_args()

    # arguments validation
    if filename == 'test.py' or filename == 'run.py':
        if args.runtime > 60:
            sys.stderr.write('Runtime cannot be greater than 60 seconds\n')
            sys.exit(1)

        if (args.flows - 1) * args.interval >= args.runtime:
            sys.stderr.write('Interval time between flows is too long '
                             'to fit in total runtime\n')
            sys.exit(1)

    return args

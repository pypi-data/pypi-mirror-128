# =============================================================================
# Minet Twitter CLI Utils
# =============================================================================
#
# Miscellaneous generic functions used throughout the twitter actions.
#
import casanova
import re
from twitter import TwitterHTTPError

from minet.cli.utils import LoadingBar
from minet.twitter import TwitterAPIClient

CHARACTERS = re.compile(r'[A-Za-z_]')
NUMBERS = re.compile(r'[0-9]+')
TWITTER_SCREEN_NAME = re.compile(r'[a-zA-Z0-9_]{1,15}')


def make_twitter_action(method_name, csv_headers):

    def action(cli_args):
        enricher = casanova.batch_enricher(
            cli_args.file,
            cli_args.output,
            keep=cli_args.select,
            add=csv_headers
        )

        loading_bar = LoadingBar(
            desc='Retrieving ids',
            unit=method_name[:-1],
            stats={
                'users': 0
            }
        )

        client = TwitterAPIClient(
            cli_args.access_token,
            cli_args.access_token_secret,
            cli_args.api_key,
            cli_args.api_secret_key
        )

        resuming_state = None

        if cli_args.resume:
            resuming_state = cli_args.output.pop_state()

        for row, user in enricher.cells(cli_args.column, with_rows=True):
            loading_bar.update_stats(user=user)

            all_ids = []
            next_cursor = -1
            result = None

            if resuming_state is not None and resuming_state.last_cursor:
                next_cursor = int(resuming_state.last_cursor)

            if cli_args.ids:
                if is_not_user_id(user):
                    loading_bar.die('The column given as argument doesn\'t contain user ids, you have probably given user screen names as argument instead. \nTry removing --ids from the command.')

                client_kwargs = {'user_id': user}

            else:
                if is_probably_not_user_screen_name(user):
                    loading_bar.die('The column given as argument probably doesn\'t contain user screen names, you have probably given user ids as argument instead. \nTry adding --ids to the command.')
                    # force flag to add

                client_kwargs = {'screen_name': user}

            while next_cursor != 0:
                client_kwargs['cursor'] = next_cursor

                skip_in_output = None

                if resuming_state:
                    skip_in_output = resuming_state.values_to_skip
                    resuming_state = None

                try:
                    result = client.call([method_name, 'ids'], **client_kwargs)
                except TwitterHTTPError as e:

                    # The user does not exist
                    loading_bar.inc('users_not_found')
                    break

                if result is not None:
                    all_ids = result.get('ids', [])
                    next_cursor = result.get('next_cursor', 0)

                    loading_bar.update(len(all_ids))

                    batch = []

                    for user_id in all_ids:
                        if skip_in_output and user_id in skip_in_output:
                            continue

                        batch.append([user_id])

                    enricher.writebatch(row, batch, next_cursor or None)
                else:
                    next_cursor = 0

            loading_bar.inc('users')

    return action


def is_not_user_id(item):
    return bool(re.match(CHARACTERS, item))


def is_probably_not_user_screen_name(item):
    matches = TWITTER_SCREEN_NAME.fullmatch(item)
    if matches:
        return bool(NUMBERS.fullmatch(item))
    return True

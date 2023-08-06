import datetime

from .slot import Slot


def print_slot(config, framadate, slot):
    votes_names = framadate.get_votes_names(slot)
    votes_str = ', '.join(map(str, votes_names))
    if config.get_quiet():
        print(f'{slot}: [{votes_str}]')
    else:
        print(f'{slot}: [{votes_str}] ({len(votes_names)} vote(s))')


def compare_slot_constraints(config, framadate, slot):
    """Return and int depending on the config constraints.

    = 0 if slot constraints are respected
    < 0 if not enough votes
    > 0 if too much votes"""
    votes = framadate.get_votes(slot)
    votes_min = None
    votes_max = None
    if config.get_constraints().get_votes_min() is not None:
        votes_min = config.get_constraints().get_votes_min()
    if config.get_constraints().get_votes_max() is not None:
        votes_max = config.get_constraints().get_votes_max()
    if config.get_constraints().get_votes_moment_re() is not None:
        m = config.get_constraints().get_votes_moment_re().match(slot.moment)
        if m is not None:
            nb = int(m.group(1))
            votes_min = nb
            votes_max = nb

    if votes_min is not None and len(votes) < votes_min:
        return len(votes) - votes_min
    elif votes_max is not None and len(votes) > votes_max:
        return len(votes) - votes_max
    else:
        return 0


def print_slot_check(config, framadate, slot):
    ret = compare_slot_constraints(config, framadate, slot)
    if ret < 0:
        mystr = f'{slot}: KO'
        if not config.get_quiet():
            mystr += (f' ({-ret} missing vote(s))')
    elif ret > 0:
        mystr = f'{slot}: KO'
        if not config.get_quiet():
            mystr += f' ({ret} extra vote(s))'
    else:
        mystr = f'{slot}: OK'
        if not config.get_quiet():
            mystr += f' ({len(framadate.get_votes(slot))} vote(s))'

    print(mystr)
    return ret == 0


def print_vote(config, framadate, vote):
    vote_slots_str = ', '.join(map(str, vote.get_slots()))
    print(f'{vote.get_name()}: [{vote_slots_str}]')


def show_slot(config, framadate, args):
    slot = Slot(args.date, args.moment)
    print_slot(config, framadate, slot)
    return 0


def show_date(config, framadate, args):
    for slot in framadate.get_slots(date=args.date):
        print_slot(config, framadate, slot)
    return 0


def show_filtered_slots(config, framadate, args):
    for slot in framadate.get_slots(filter=args.subcommand):
        print_slot(config, framadate, slot)
    return 0


def show_votes(config, framadate, args):
    for vote in framadate.get_votes():
        print_vote(config, framadate, vote)
    return 0


def check_slot(config, framadate, args):
    slot = Slot(args.date, args.moment)
    if print_slot_check(config, framadate, slot):
        return 0
    else:
        return 1


def check_date(config, framadate, args):
    res = 0
    for slot in framadate.get_slots(date=args.date):
        if not print_slot_check(config, framadate, slot):
            res = 1
    return res


def check_filtered_slots(config, framadate, args):
    res = 0
    for slot in framadate.get_slots(filter=args.subcommand):
        if not print_slot_check(config, framadate, slot):
            res = 1
    return res


def add_slot(config, framadate, args):
    slot = Slot(args.date, args.moment)
    framadate.add_slot(slot)
    if not config.get_quiet():
        print(f'{slot}: added')
    return 0


def delete_old_slots(config, framadate, args):
    for slot in framadate.get_old_slots():
        framadate.delete_slot(slot)
        if not config.get_quiet():
            print(f'{slot}: deleted')
    return 0


def delete_vote(config, framadate, args):
    framadate.delete_vote(args.vote)
    if not config.get_quiet():
        print(f'{args.vote}: deleted')
    return 0


def delete_empty_votes(config, framadate, args):
    deleted_votes = framadate.delete_empty_votes()
    for v in deleted_votes:
        print(f'{v}: deleted')
    return 0


def run_job(config, framadate, args):
    job = config.get_job(args.id)
    if job.run(config, framadate, args):
        return 0
    else:
        return 1


COMMANDS_DICT = {
    'show': {
        'help': 'Show poll results',
        'subcommands': {
            'slot': {
                'func': show_slot,
                'help': 'Show results for a given slot',
                'args': [
                    {'name': 'date',
                     'help': 'Date slot in ISO format (YYYY-MM-DD)',
                     'type': datetime.date.fromisoformat},
                    {'name': 'moment',
                     'help': 'Moment of the slot (string)',
                     'type': str},
                ],
            },
            'date': {
                'func': show_date,
                'help': 'Show results for a given date',
                'args': [
                    {'name': 'date',
                     'help': 'Date slot in ISO format (YYYY-MM-DD)',
                     'type': datetime.date.fromisoformat},
                ],
            },
            'all-slots': {
                'func': show_filtered_slots,
                'help': 'Show results for all slots',
            },
            'next-slots': {
                'func': show_filtered_slots,
                'help': 'Show results for all coming slots',
            },
            'next-slot': {
                'func': show_filtered_slots,
                'help': 'Show results for the next coming slot',
            },
            'next-date': {
                'func': show_filtered_slots,
                'help': 'Show results for all slots of the coming date',
            },
            'all-votes': {
                'func': show_votes,
                'help': 'Show all votes',
            },
        },
    },
    'check': {
        'help': 'Check poll results',
        'subcommands': {
            'slot': {
                'func': check_slot,
                'help': 'Check results for a given slot',
                'args': [
                    {'name': 'date',
                     'help': 'Date slot in ISO format (YYYY-MM-DD)',
                     'type': datetime.date.fromisoformat},
                    {'name': 'moment',
                     'help': 'Moment of the slot (string)',
                     'type': str},
                ],
            },
            'date': {
                'func': check_date,
                'help': 'Check results for a given date',
                'args': [
                    {'name': 'date',
                     'help': 'Date slot in ISO format (YYYY-MM-DD)',
                     'type': datetime.date.fromisoformat},
                ],
            },
            'all-slots': {
                'func': check_filtered_slots,
                'help': 'Check results for all slots',
            },
            'next-slots': {
                'func': check_filtered_slots,
                'help': 'Check results for all coming slots',
            },
            'next-slot': {
                'func': check_filtered_slots,
                'help': 'Check results for the next coming slot',
            },
            'next-date': {
                'func': show_filtered_slots,
                'help': 'Check results for all slots of the coming date',
            },
        },
    },
    'add': {
        'help': 'Add new slots',
        'subcommands': {
            'slot': {
                'func': add_slot,
                'help': 'Add a new slot',
                'args': [
                    {'name': 'date',
                     'help': 'Date slot in ISO format (YYYY-MM-DD)',
                     'type': datetime.date.fromisoformat},
                    {'name': 'moment',
                     'help': 'Moment of the slot (string)',
                     'type': str},
                ],
            },
        },
    },
    'delete': {
        'help': 'Delete slots',
        'subcommands': {
            'old-slots': {
                'func': delete_old_slots,
                'help': 'Delete all past slots from the poll',
            },
            'vote': {
                'func': delete_vote,
                'help': 'Delete a vote',
                'args': [
                    {'name': 'vote',
                     'help': 'Name of the vote',
                     'type': str},
                ],
            },
            'empty-votes': {
                'func': delete_empty_votes,
                'help': 'Delete all empty votes from the poll',
            },
        },
    },
    'job': {
        'func': run_job,
        'help': 'Run a job from a config file',
        'args': [
            {'name': 'id',
             'help': 'Job ID from a given config file',
             'type': str},
        ],
    },
}

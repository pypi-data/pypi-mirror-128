import email
import pathlib
import re
import smtplib
import yaml

from .commands import (
    COMMANDS_DICT,
    compare_slot_constraints,
)


class JobCondition:

    def __init__(self, yaml_data):
        self._name = yaml_data['condition']

    def get_name(self):
        return self._name

    def check(self, config, framadate):
        raise Exception('Internal error: method should be overloaded')


class JobConditionSlots(JobCondition):

    def __init__(self, yaml_data):
        JobCondition.__init__(self, yaml_data)
        self._slots = 'all-slots'
        self._votes_less = None
        self._votes_more = None
        self._constraints = None
        if 'slots' in yaml_data.keys():
            self._slots = yaml_data['slots']
            if 'verify' in yaml_data.keys():
                yaml_verify = yaml_data['verify']
                if 'votes' in yaml_verify.keys():
                    yaml_verify_votes = yaml_verify['votes']
                    if 'less' in yaml_verify_votes.keys():
                        self._votes_less = yaml_verify_votes['less']
                        if 'more' in yaml_verify_votes.keys():
                            self._votes_more = yaml_verify_votes['more']
                if 'constraints' in yaml_verify.keys():
                    self._constraints = yaml_verify['constraints']
                    if type(self._constraints) != bool:
                        raise Exception('Yaml error: job > condition > '
                                        'verify > constraints should be a '
                                        'boolean')

    def check(self, config, framadate):
        slots = framadate.get_slots(self._slots)
        for slot in slots:
            votes = framadate.get_votes(slot)
            if (self._votes_less is not None and
                    len(votes) < self._votes_less):
                return True
            if (self._votes_more is not None and
                    len(votes) > self._votes_more):
                return True
            if self._constraints is not None:
                comparison = compare_slot_constraints(config, framadate, slot)
                if self._constraints:
                    if comparison != 0:
                        return True
                else:
                    if comparison == 0:
                        return True
        return False


class JobAction:

    def __init__(self, yaml_data):
        self._name = yaml_data['action']

    def run(self):
        raise Exception('Internal error: method should overloaded')


class JobActionCommand(JobAction):

    def __init__(self, yaml_data):
        JobAction.__init__(self, yaml_data)
        self._command = yaml_data['command']
        self._subcommand = yaml_data['subcommand']

    def run(self, config, framadate, args):
        func = COMMANDS_DICT[self._command]['subcommands'][
            self._subcommand]['func']
        return (func(config, framadate, args) == 0)


class JobActionEmail(JobAction):

    def __init__(self, yaml_data):
        JobAction.__init__(self, yaml_data)
        self._slots = yaml_data['slots']
        self._content = yaml_data['content']

    def run(self, config, framadate, args):
        slots = framadate.get_slots(self._slots)
        allvotes = []
        min_votes = 0
        max_votes = 0
        missing_votes = 0
        exceeding_votes = 0
        for slot in slots:
            votes = framadate.get_votes(slot)
            allvotes += votes
            nb_min = config.get_constraints().get_votes_min()
            nb_max = config.get_constraints().get_votes_max()
            nb_moment_re = config.get_constraints().get_votes_moment_re()
            if nb_moment_re is not None:
                m = nb_moment_re.match(slot.moment)
                if m is not None:
                    nb_min = int(m.group(1))
                    nb_max = nb_min
            if nb_min is not None:
                min_votes += nb_min
                missing_votes += max(nb_min - len(votes), 0)
            if nb_max is not None:
                max_votes += nb_max
                exceeding_votes += max(len(votes) - nb_max, 0)
        allvotes_str = [vote.get_name() for vote in allvotes]
        allvotes_str.sort()

        email_args = {
            'date': slots[0].date,
            'nb_votes': len(allvotes),
            'min_votes': min_votes,
            'max_votes': max_votes,
            'missing_votes': missing_votes,
            'exceeding_votes': exceeding_votes,
            'votes': ', '.join(map(str, allvotes_str)),
        }
        e = email.message_from_bytes(
            self._content.format_map(email_args).encode('utf-8')
        )
        s = smtplib.SMTP(config.get_smtp_host())
        s.send_message(e)
        return True


class JobActionBackup(JobAction):

    def __init__(self, yaml_data):
        JobAction.__init__(self, yaml_data)
        self._slots = 'all-slots'
        self._mode = 'w'
        if 'slots' in yaml_data.keys():
            self._slots = yaml_data['slots']
        if 'mode' in yaml_data.keys():
            self._mode = yaml_data['mode']
        self._filepath = yaml_data['filepath']

    def run(self, config, framadate, args):
        path = pathlib.Path(self._filepath)
        if not path.is_absolute():
            path = pathlib.Path(str(config.get_config_dir()) + '/' +
                                self._filepath)
        with path.open(mode=self._mode, encoding='utf-8') as f:
            for slot in framadate.get_slots(self._slots):
                votes_names = framadate.get_votes_names(slot)
                votes_str = '\n'.join(map(str, votes_names))
                f.write(f'# {slot}\n{votes_str}\n')


class Job:

    def __init__(self, yaml_data):
        self._id = yaml_data['id']
        self._conditions = []
        self._actions = []
        if 'condition' in yaml_data.keys():
            for cond in yaml_data['condition']:
                if cond['condition'] == 'slots':
                    self._conditions.append(JobConditionSlots(cond))
                else:
                    raise Exception(f'Unsupported condition name: '
                                    f'{cond["condition"]}')
        if 'action' in yaml_data.keys():
            for action in yaml_data['action']:
                if action['action'] == 'command':
                    self._actions.append(JobActionCommand(action))
                elif action['action'] == 'email':
                    self._actions.append(JobActionEmail(action))
                elif action['action'] == 'backup':
                    self._actions.append(JobActionBackup(action))
                else:
                    raise Exception(f'Unsupported action name: '
                                    f'{action["action"]}')

    def get_id(self):
        return self._id

    def conditions(self, config, framadate):
        ret = (len(self._conditions) > 0)
        for cond in self._conditions:
            ret = cond.check(config, framadate) and ret
        return ret

    def actions(self, config, framadate, args):
        ret = True
        for action in self._actions:
            ret = action.run(config, framadate, args) and ret
        return ret

    def run(self, config, framadate, args):
        if self.conditions(config, framadate):
            return self.actions(config, framadate, args)
        else:
            return True


class ConfigurationConstraints:

    def __init__(self, yaml_data):
        self._votes_min = None
        self._votes_max = None
        self._votes_moment_regexp = None
        if 'votes' in yaml_data.keys():
            yaml_votes = yaml_data['votes']
            if 'min' in yaml_votes.keys():
                self._votes_min = int(yaml_votes['min'])
            if 'max' in yaml_votes.keys():
                self._votes_max = int(yaml_votes['max'])
            if 'moment_regexp' in yaml_votes.keys():
                self._votes_moment_regexp = \
                    re.compile(yaml_votes['moment_regexp'])

    def get_votes_min(self):
        return self._votes_min

    def get_votes_max(self):
        return self._votes_max

    def get_votes_moment_re(self):
        return self._votes_moment_regexp


class Configuration:

    def __init__(self, yaml_path=None,
                 url=None, votes_min=None, votes_max=None,
                 quiet=None):
        """Initialize the configuration from a YAML file (if given)."""
        self._yaml_path = yaml_path
        self._url = None
        self._constraints = None
        self._quiet = False     # Default value
        self._jobs = {}
        if yaml_path is not None:
            yaml_data = yaml.safe_load(yaml_path.open('r'))
            if 'configuration' in yaml_data.keys():
                yaml_configuration = yaml_data['configuration']
                if 'url' in yaml_configuration.keys():
                    self._url = yaml_configuration['url']
                if 'constraints' in yaml_configuration.keys():
                    self._constraints = ConfigurationConstraints(
                        yaml_configuration['constraints'])
                if 'quiet' in yaml_configuration.keys():
                    self._quiet = bool(yaml_configuration['quiet'])
                if 'email' in yaml_configuration.keys():
                    yaml_email = yaml_configuration['email']
                    self._smtp_host = yaml_email['smtp_host']
            if 'job' in yaml_data.keys():
                self._load_jobs(yaml_data['job'])
        if url is not None:
            self._url = url
        if votes_min is not None:
            self._votes_min = votes_min
        if votes_max is not None:
            self._votes_max = votes_max
        if quiet is not None:
            self._quiet = quiet

    def _load_jobs(self, yaml_data):
        for job in yaml_data:
            self._jobs[job['id']] = Job(job)

    def get_config_dir(self):
        return self._yaml_path.parent

    def get_url(self):
        return self._url

    def get_constraints(self):
        return self._constraints

    def get_quiet(self):
        return self._quiet

    def get_smtp_host(self):
        return self._smtp_host

    def get_job(self, id):
        if id in self._jobs:
            return self._jobs[id]
        else:
            raise Exception('Unknown job ID')

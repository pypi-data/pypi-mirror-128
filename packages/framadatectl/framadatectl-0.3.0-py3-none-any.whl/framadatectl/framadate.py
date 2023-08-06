import base64
import csv
import datetime
import io
import re
import requests
from bs4 import BeautifulSoup

from .slot import Slot
from .vote import Vote


class Framadate:

    _http_headers = {'Accept-Language': 'en-US'}

    def __init__(self, url):
        self._url = url
        self._admin = False     # whether _url is an admin URL
        self._slots = None      # Map {Slot: [Vote]}
        self._dates = None      # Map {datetime.date: [Slot]}
        self._votes = None      # Map {str: Vote}
        self.fetch()

    def _get_exportcsv_url(self):
        m = re.fullmatch(r'''(https{0,1}://.+)/(\w+)/admin''',
                         self._url)
        if m is not None:
            self._admin = True
            return f'{m.group(1)}/exportcsv.php?admin={m.group(2)}'

        m = re.fullmatch(r'''(https{0,1}://.+)/([^/]+)''',
                         self._url)
        if m is not None:
            return f'{m.group(1)}/exportcsv.php?poll={m.group(2)}'

        raise Exception('%s is not a valid Framadate URL' %
                        self._url)

    def fetch(self):
        """Fetch and parse the Framadate CSV file."""
        exportcsv_url = self._get_exportcsv_url()
        r = requests.get(exportcsv_url, headers=self._http_headers)
        if r.status_code != 200:
            raise Exception('HTTP GET %s returned a status code of %d' %
                            (exportcsv_url, r.status_code))
        csvio = io.StringIO(r.text, newline='')
        reader = csv.reader(csvio, dialect=csv.unix_dialect)

        # Read CSV headers
        slots = []
        reader_dates = next(reader)
        reader_moments = next(reader)
        for i in range(1, len(reader_dates) - 1):
            date = datetime.datetime.strptime(reader_dates[i],
                                              '%Y-%m-%d').date()
            moment = reader_moments[i]
            slots.append(Slot(date, moment))

        # Read CSV data
        self._slots = {}
        self._dates = {}
        self._votes = {}
        for slot in slots:
            self._slots[slot] = []
            if slot.date not in self._dates:
                self._dates[slot.date] = []
            self._dates[slot.date].append(slot)
        for record in reader:
            vote_name = record[0]
            vote_slots = []
            for i in range(1, len(record) - 1):
                if record[i] == 'Yes':
                    vote_slots.append(slots[i - 1])
            if vote_name in self._votes:
                raise Exception(f'Internal error: {vote_name} should not '
                                'exist in votes')
            vote = Vote(self, vote_name, vote_slots)
            self._votes[vote_name] = vote
            for slot in vote_slots:
                self._slots[slot].append(vote)

    def _fetch_html(self):
        """Fetch and parse the Framadate HTML page.

        This function is needed for advanced operations like deleting a vote.
        """
        r = requests.get(self._url, headers=self._http_headers)
        if r.status_code != 200:
            raise Exception('HTTP GET %s returned a status code of %d' %
                            (self._url, r.status_code))
        soup = BeautifulSoup(r.text, 'html.parser')
        vote_regexp = re.compile(r'''^Remove line: (.+)$''')
        for v in soup.find_all('a', class_='btn btn-default btn-sm',
                               title=vote_regexp):
            m = vote_regexp.fullmatch(v['title'])
            if m is None:
                raise Exception('Unexpected error: %s is not a valid title' %
                                v['title'])
            vote_name = m.group(1)
            if vote_name not in self._votes:
                raise Exception('Unexpected error: %s cannot be found in the '
                                'votes dict' % vote_name)
            self._votes[vote_name]._set_delete_url(v['href'])

    def get_slots(self, filter=None, date=None):
        """Return a list of slots, potentially filtered.

        The filter can be one of these 2 options:
        - filter: string filter like 'next-slots', 'old-slots', ...
        - date: datetime.date"""
        filters_map = {
            'all-slots': self.get_all_slots,
            'next-slots': self.get_next_slots,
            'next-slot': self.get_next_slot,
            'old-slots': self.get_old_slots,
            'next-date': lambda: self.get_next_slots(nb_dates=1),
        }
        if filter is None and date is None:
            filter = 'all-slots'
        if filter is not None and date is not None:
            raise Exception('2 filters cannot be specified.')
        if filter is not None:
            return filters_map[filter]()
        if date is not None:
            return self._dates[date]

    def get_all_slots(self):
        """Return an array of all slots of the Framadate."""
        res = [s for s in self._slots.keys()]
        res.sort()
        return res

    def get_all_dates(self):
        """Return an array of all dates of the Framadate."""
        res = [d for d in self._dates.keys()]
        res.sort()
        return res

    def get_next_slots(self, nb_dates=None):
        """Return an array of future slots of the Framadate.

        If specified, nb_dates limits to a number of identical dates."""
        today = datetime.date.today()
        next_dates = [d for d in self.get_all_dates() if d >= today]
        res = []
        if nb_dates is not None:
            for i in range(0, nb_dates):
                res += self._dates[next_dates[i]]
        else:
            for date in next_dates:
                res += self._dates[date]
        res.sort()
        return res

    def get_next_slot(self):
        """Return a one slot item array of the next date of the Framadate."""
        return self.get_next_slots()[:1]

    def get_old_slots(self):
        """Return an array of old slots of the Framadate."""
        today = datetime.date.today()
        return [s for s in self.get_all_slots() if s.date < today]

    def get_votes(self, slot=None):
        """Return the list of votes for a given slot (or all)."""
        if slot is None:
            return self._votes.values()
        else:
            return self._slots[slot]

    def get_votes_names(self, slot):
        """Return the list of votes name for a given slot."""
        res = [vote.get_name() for vote in self.get_votes(slot)]
        res.sort()
        return res

    def add_slot(self, slot):
        """Add a new slot slot into the Framadate."""
        if not self._admin:
            raise Exception('Adding slots requires a Framadate admin url')
        if slot in self._slots.keys():
            raise Exception(f'Slot {slot} cannot be added since it already '
                            f'exists')
        r = requests.post(self._url, headers=self._http_headers,
                          data={'newdate': slot.date.isoformat(),
                                'newmoment': slot.moment,
                                'confirm_add_column': ''})
        if r.status_code != 200:
            raise Exception('HTTP POST %s returned a status code of %d' %
                            (self._url, r.status_code))
        self._slots[slot] = []

    def _get_delete_url(self, slot):
        dt = datetime.datetime.combine(slot.date, datetime.time.min)
        b64 = base64.b64encode('{t:.0f}@{moment}'.format(
            t=dt.timestamp(),
            moment=slot.moment
        ).encode())
        dtid = b64.decode().rstrip('=')
        return f'{self._url}/action/delete_column/{dtid}'

    def delete_slot(self, slot):
        """Delete a slot from the Framadate."""
        if not self._admin:
            raise Exception('Deleting slots requires a Framadate admin url')
        if slot not in self._slots.keys():
            raise Exception(f'Slot {slot} cannot be deleted since it '
                            'does not exist')
        delete_url = self._get_delete_url(slot)
        r = requests.get(delete_url, headers=self._http_headers)
        if r.status_code != 200:
            raise Exception('HTTP GET %s returned a status code of %d' %
                            (delete_url, r.status_code))
        for vote in self._slots[slot]:
            vote._delete_slot(slot)
        self._dates[slot.date].remove(slot)
        del self._slots[slot]

    def delete_vote(self, vote_name):
        """Search for a vote and delete it from the Framadate."""
        vote = self._votes[vote_name]
        vote.delete()

    def delete_empty_votes(self):
        """Search for empty votes and delete them."""
        ret = []
        for vote in [vote for vote in self._votes.values()
                     if len(vote.get_slots()) == 0]:
            vote.delete()
            ret.append(vote.get_name())
        return ret

    def _forget_vote(self, vote):
        """Internal function to pop a vote from internal data."""
        del self._votes[vote.get_name()]
        for slot in vote.get_slots():
            votes = self._slots[slot]
            for i in range(0, len(votes)):
                if votes[i] == vote:
                    votes.pop(i)

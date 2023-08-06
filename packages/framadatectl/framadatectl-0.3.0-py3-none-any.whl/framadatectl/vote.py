import requests


class Vote:

    def __init__(self, framadate, name, slots=[]):
        self._framadate = framadate
        self._name = name
        self._slots = slots     # Array [Slot]
        self._delete_url = None

    def get_name(self):
        """Get the name of the vote."""
        return self._name

    def get_slots(self):
        """Get the array of attended slots."""
        return self._slots

    def delete(self):
        """Delete this vote from the Framadate.

        Once called, this object should not be used anymore.
        """
        if self._delete_url is None:
            self._framadate._fetch_html()
        if self._delete_url is None:
            raise Exception('Cannot find deletion URL '
                            '(are you using a Framadate admin url?)')
        r = requests.get(self._delete_url,
                         headers=self._framadate._http_headers)
        if r.status_code != 200:
            raise Exception('HTTP GET %s returned a status code of %d' %
                            (self._delete_url, r.status_code))
        self._framadate._forget_vote(self)

    def _set_delete_url(self, delete_url):
        self._delete_url = delete_url

    def _delete_slot(self, slot):
        """Delete a slot from the array of slots."""
        self._slots.remove(slot)

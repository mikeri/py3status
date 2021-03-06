# -*- coding: utf-8 -*-
"""
Display number of pending updates for Debian based Distros.

Thanks to Iain Tatch <iain.tatch@gmail.com> for the script that this is based on.

This will display a count of how many 'apt' updates are waiting to be installed.

Configuration parameters:
    cache_timeout: How often we refresh this module in seconds (default 600)
    format: Display format to use
        (default 'UPD: {apt}')
    format_one: Display format to use if one update is available. If left empty,
    default format will be used.
        (default '')
    format_none: Display format to use if no updates are available.
        (default '')


Format placeholders:
    {apt} Number of pending apt updates

Requires:
    apt: Needed to display pending 'apt' updates

@author Joshua Pratt <jp10010101010000@gmail.com>
@license BSD

SAMPLE OUTPUT
{'color': '#FFFF00', 'full_text': 'UPD: 5'}
"""

import subprocess
import sys

LINE_SEPARATOR = "\\n" if sys.version_info > (3, 0) else "\n"


class Py3status:
    # available configuration parameters
    cache_timeout = 600
    format = 'UPD: {apt}'
    format_one = ''
    format_none = ''

    def check_updates(self):
        apt_updates = self._check_apt_updates()

        if apt_updates == 0:
            color = self.py3.COLOR_GOOD
            full_text = self.py3.safe_format(
                self.format_none, {'apt': apt_updates})
        elif apt_updates == 1 and self.format_one:
            color = self.py3.COLOR_DEGRADED
            full_text = self.py3.safe_format(
                self.format_one, {'apt': apt_updates})
        else:
            color = self.py3.COLOR_DEGRADED
            full_text = self.py3.safe_format(
                self.format, {'apt': apt_updates})
        return {
            'color': color,
            'cached_until': self.py3.time_in(self.cache_timeout),
            'full_text': full_text,
        }

    def _check_apt_updates(self):
        """
        This method will use the 'checkupdates' command line utility
        to determine how many updates are waiting to be installed via
        'apt list --upgradeable'.
        """
        output = str(subprocess.check_output(["apt", "list", "--upgradeable"]))
        output = output.split(LINE_SEPARATOR)
        return len(output[1:-1])


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)

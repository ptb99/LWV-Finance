Collection of data analyses for 
campaign finance statistics for ballot measures.
Produced for our local League of Women Voters educational efforts.

This uses Marimo notebooks and a standard uv Python environment.
See https://molab.marimo.io/notebooks/ for hosting.

- CA-Props-2026.py - uses PowerSearch site for data on state propositions

- Prop50-totals.py - older code specific to 2025 election

- SCC-Props-2026.py - designed for Marimo hosting, requires upload of
  current data from County Netfile site  in .xlsx format

- SCC-Props-local.py - looks for both 2025 and 2026 .xlsx file in local
  directory (Note that RTM stats are wrong without 2025 data).

- SCC-Props-API.py - uses (unoffical?) Netfile API to get RTM stats.  This
  is the current best approach.

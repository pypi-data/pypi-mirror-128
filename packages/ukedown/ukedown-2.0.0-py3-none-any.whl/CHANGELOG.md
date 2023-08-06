# Changelog

## v 2.0.0
44e9aa0 (HEAD -> master, tag: v2.0.0) Add poetry lockfile
75cb4dd (origin/master, origin/HEAD) python project config using poetry
597e39f reformatted with black
8c8688b (markdown3) Merge pull request #1 from lanky/markdown3
989f9c9 (origin/markdown3) disables pytest until we actually have tests. If ever.
3e810cb Add package builder action
48cf0cc disables pytest until we actually have tests. If ever.
11a4e17 much blackness, plus extension register updates
61c71ec Add package builder action

## v1.0.0 - First PyPi release
efc9102 (tag: v1.0.0) new major version, with versioned deps
e9e7252 README updates, URL correction etc
d24ee73 update to Markdown 3 API, parametrise processors
c67a1bc fixes ElementTree warnings
92d6120 ignore backup files and build artifacts
a167d22 Corrects pypi username
e8a298c corrects type in long_desceription assignment
36debf8 added dependencies to setup.py
386413e Adds license and license headers for GPL v3+
b2198ca move package contents into ukedown subdir
bcae6c2 permits single quotes in backing vox
0495226 removes support for perf notes in chord pattern
11b99ef renders [section] as span, not h2
e544ecf updates chord recognition patterns
7d9c2f5 made notes regex more generic (anything in {})
f45c0cc reverted multiline parsing to fix box detection
4f45f5f Permit '/' in performance notes
9f51836 ukedown updated to stop box sections collapsing together
b0958cd enabled 'notes' markup in udn ({NOTE}) for performance notes
17c66e5 Added support for X/Y to chord patterns ('/')
385caa3 updated translation table to include ellipsis
7718fd6 Migrate to  python3 using 2to3
eb49a5f Multiple updates to udn core
7ef4f2d split out regex and translation tables
e477ffe renamed CollapseDivProcessor to CollapseChildProcessor
e9e3daf header patterns now work inside box sections
d92c0c9 added inline patterns for vox and notes
8f5bb6a added NOTES and VOX patterns
964cb57 treeprocessor for paragraph merging
d15ac69 refactored ukedown extension into ukedown/udn.py Updated mdsession to use this


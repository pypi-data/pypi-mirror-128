import pkg_resources
required = {'mutagen', 'gTTS'}
installed = {pkg.key for pkg in pkg_resources.working_set}
print(installed)
missing = required - installed
print(missing)

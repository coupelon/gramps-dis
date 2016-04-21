register(TOOL, 
         id    = 'DownloadInternetSources',
         name  = _("Download Internet Sources"),
         description =  _("Browse the internet sources for each person and tries to back it up."),
         version = '1.2',
         gramps_target_version = '4.2',
         status = STABLE,
         fname = 'DownloadInternetSources.py',
         authors = ["Olivier Coupelon"],
         authors_email = ["olivier@coupelon.net"],
         category = TOOL_UTILS,
         toolclass = 'DownloadWindow',
         optionclass = 'DownloadOptions',
         tool_modes = [TOOL_MODE_GUI]
         )

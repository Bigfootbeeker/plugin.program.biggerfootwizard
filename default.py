################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################
import xbmc
import xbmcplugin

import sys

try:  # Python 3
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    from urlparse import parse_qsl

from resources.libs.config import CONFIG
from resources.libs import logging

_url = sys.argv[0]
_handle = int(sys.argv[1])


def log_params(params):
    logstring = '{0}: '.format(_url)
    for param in params:
        logstring += '[ {0}: {1} ] '.format(param, params[param])

    logging.log(logstring, level=xbmc.LOGDEBUG)


def route(paramstring):
    params = dict(parse_qsl(paramstring))
    log_params(params)

    mode = None
    url = None
    name = None

    if 'mode' in params:
        mode = params['mode']
    else:
        from resources.libs import menu
        menu.main_menu()

    if 'url' in params:
        url = params['url']
    if 'name' in params:
        name = params['name']

    # SETTINGS
    if mode == 'settings':  # Open Aftermath settings
        CONFIG.open_settings(name)
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'opensettings':  # Open other addons' settings
        id = eval(url.upper()+'ID')[name]['plugin']
        CONFIG.open_settings(id)
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'togglesetting':  # Toggle a setting
        CONFIG.set_setting(name, 'false' if CONFIG.get_setting(name) == 'true' else 'true')
        xbmc.executebuiltin('Container.Refresh()')

    # MENU SECTIONS
    if mode == 'builds':  # Builds
        from resources.libs import menu
        menu.build_menu()
    elif mode == 'viewbuild':  # Builds -> "Your Build"
        from resources.libs import menu
        menu.view_build(name)
    elif mode == 'theme':  # Builds -> "Your Build" -> "Your Theme"
        from resources.libs import menu
        menu.wizard_menu(name, mode, url)
    elif mode == 'install':  # Builds -> Fresh Install/Standard Install/Apply guifix
        from resources.libs import menu
        menu.wizard_menu(name, url)
    elif mode == 'addonpack':  # Install Addon Pack
        from resources.libs import install
        install.install_addon_pack(name, url)
    elif mode == 'skinpack':  # Install Skin Pack
        from resources.libs import install
        install.install_skin(name, url)
    elif mode == 'buildinfo':  # Builds -> Build Info
        from resources.libs import check
        check.build_info(name)
    elif mode == 'buildpreview':  # Builds -> Build Preview
        from resources.libs import yt
        yt.build_video(name)
    elif mode == 'maint':  # Maintenance + Maintenance -> any "Tools" section
        from resources.libs import menu
        menu.maint_menu(name)
    elif mode == 'advancedsetting':  # Maintenance -> System Tweaks/Fixes -> Advanced Settings
        from resources.libs import menu
        menu.advanced_window(name)
    elif mode == 'enableaddons':  # Maintenance - > Addon Tools -> Enable/Disable Addons
        from resources.libs import menu
        menu.enable_addons()
    elif mode == 'toggleaddon':
        from resources.libs import db
        db.toggle_addon(name, url)
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'togglecache':
        from resources.libs import clear
        clear.toggle_cache(name)
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'changefeq':  # Maintenance - Auto Clean Frequency
        from resources.libs import menu
        menu.change_freq()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'systeminfo':  # Maintenance -> System Tweaks/Fixes -> System Information
        from resources.libs import menu
        menu.system_info()
    elif mode == 'nettools':  # Maintenance -> Misc Maintenance -> Network Tools
        from resources.libs import menu
        menu.net_tools()
    elif mode == 'runspeedtest':  # Maintenance -> Misc Maintenance -> Network Tools -> Speed Test -> Run Speed Test
        from resources.libs import menu
        menu.run_speed_test()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'clearspeedtest':  # Maintenance -> Misc Maintenance -> Network Tools -> Speed Test -> Clear Results
        from resources.libs import menu
        menu.clear_speed_test()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'viewspeedtest':  # Maintenance -> Misc Maintenance -> Network Tools -> Speed Test -> any previous test
        from resources.libs import menu
        menu.view_speed_test(name)
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'viewIP':  # Maintenance -> Misc Maintenance -> Network Tools -> View IP Address & MAC Address
        from resources.libs import menu
        menu.view_ip()
    elif mode == 'speedtest':  # Maintenance -> Misc Maintenance -> Network Tools -> Speed Test
        from resources.libs import menu
        menu.speed_test()
    elif mode == 'apk':  # APK Installer
        from resources.libs import menu
        menu.apk_menu(url)
    elif mode == 'apkscrape':  # APK Installer -> Official Kodi APK's
        from resources.libs import menu
        menu.apk_scraper()
    elif mode == 'apkinstall':
        from resources.libs import install
        install.install_apk(name, url)
    elif mode == 'removeaddondata':  # Maintenance - > Addon Tools -> Remove Addon Data
        from resources.libs import menu
        menu.remove_addon_data_menu()
    elif mode == 'savedata':  # Save Data + Builds -> Save Data Menu
        from resources.libs import menu
        menu.save_menu()
    elif mode == 'youtube':  # "YouTube Section"
        from resources.libs import menu
        menu.youtube_menu(url)
    elif mode == 'viewVideo':  # View  Video
        from resources.libs import yt
        yt.play_video(url)
    elif mode == 'addons':  # Addon Installer
        from resources.libs import menu
        menu.addon_menu(url)
    elif mode == 'addoninstall':  # Install Addon
        from resources.libs import install
        install.install_addon(name, url)
    elif mode == 'trakt':  # Save Data -> Keep Trakt Data
        from resources.libs import menu
        menu.trakt_menu()
    elif mode == 'realdebrid':  # Save Data -> Keep Debrid
        from resources.libs import menu
        menu.debrid_menu()
    elif mode == 'login':  # Save Data -> Keep Login Info
        from resources.libs import menu
        menu.login_menu()
    elif mode == 'developer':  # Developer  Menu
        from resources.libs import menu
        menu.developer()

    # MAINTENANCE FUNCTIONS
    elif mode == 'kodi17fix':  # Misc Maintenance -> Kodi 17 Fix
        from resources.libs import db
        db.kodi_17_fix()
    elif mode == 'unknownsources':  # Misc Maintenance -> Enable Unknown Sources
        from resources.libs import skin
        skin.swap_us()
    elif mode == 'asciicheck':  # System Tweaks -> Scan for Non-Ascii Files
        from resources.libs import tools
        tools.ascii_check()
    elif mode == 'convertpath':   # System Tweaks -> Convert Special Paths
        from resources.libs import tools
        tools.convert_special(CONFIG.HOME)
    elif mode == 'fixaddonupdate':   # System Tweaks -> Fix Addons not Updating
        from resources.libs import db
        db.fix_update()
    elif mode == 'forceprofile':  # Misc Maintenance -> Reload Profile
        from resources.libs import tools
        tools.reload_profile(tools.get_info_label('System.ProfileName'))
    elif mode == 'forceclose':  # Misc Maintenance -> Force Close Kodi
        from resources.libs import tools
        tools.kill_kodi()
    elif mode == 'forceskin':  # Misc Maintenance -> Reload Skin
        xbmc.executebuiltin("ReloadSkin()")
        xbmc.executebuiltin('Container.Refresh()')
    # elif mode == 'hidepassword':  # Addon Tools -> Hide Passwords on Keyboard Entry
    #     from resources.libs import db
    #     db.hide_password()
    # elif mode == 'unhidepassword':  # Addon Tools -> Unhide Passwords on Keyboard Entry
    #     from resources.libs import db
    #     db.unhide_password()
    elif mode == 'checksources':   # System Tweaks -> Scan source for broken links
        from resources.libs import check
        check.check_sources()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'checkrepos':   # System Tweaks -> Scan for broken repositories
        from resources.libs import check
        check.check_repos()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'whitelist':  # Whitelist Functions
        from resources.libs import whitelist
        whitelist.whitelist(name)

    #  CLEANING
    elif mode == 'oldThumbs':  # Cleaning Tools -> Clear Old Thumbnails
        from resources.libs import clear
        clear.old_thumbs()
    elif mode == 'clearbackup':  # Backup/Restore -> Clean Up Back Up Folder
        from resources.libs import backup
        backup.cleanup_backup()
    elif mode == 'fullclean':  # Cleaning Tools -> Total Cleanup
        from resources.libs import clear
        clear.total_clean()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'clearcache':  # Cleaning Tools -> Clear Cache
        from resources.libs import clear
        clear.clear_cache()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'clearfunctioncache':  # Cleaning Tools -> Clear Function Caches
        from resources.libs import clear
        clear.clear_function_cache()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'clearpackages':  # Cleaning Tools -> Clear Packages
        from resources.libs import clear
        clear.clear_packages()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'clearcrash':  # Cleaning Tools -> Clear Crash Logs
        from resources.libs import clear
        clear.clear_crash()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'clearthumb':  # Cleaning Tools -> Clear Thumbnails
        from resources.libs import clear
        clear.clear_thumbs()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'cleararchive':  # Cleaning Tools -> Clear Archive Cache
        from resources.libs import clear
        clear.clear_archive()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'freshstart':  # Cleaning Tools -> Fresh Start
        from resources.libs import install
        install.fresh_start()
    elif mode == 'purgedb':  # Cleaning Tools -> Purge Databases
        from resources.libs import db
        db.purge_db()
    elif mode == 'removeaddons':  # Addon Tools -> Remove Addons
        from resources.libs import clear
        clear.remove_addon_menu()
    elif mode == 'removedata':  # Addon Tools -> Remove Addon Data
        from resources.libs import clear
        clear.remove_addon_data(name)
    elif mode == 'resetaddon':  # Addon Tools -> Remove Addon Data -> Remove  Wizard Addon Data
        from resources.libs import tools
        total = tools.clean_house(CONFIG.ADDON_DATA, ignore=True)
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]Addon_Data reset[/COLOR]".format(CONFIG.COLOR2))

    # LOGGING
    elif mode == 'uploadlog':  # Upload Log File
        logging.upload_log()
    elif mode == 'viewlog':  # View kodi.log
        from resources.libs import gui
        gui.show_log_viewer()
    elif mode == 'viewwizlog':  #  View wizard.log
        from resources.libs import gui
        gui.show_log_viewer(CONFIG.WIZLOG)
    elif mode == 'viewerrorlog':  # View errors in log
        logging.error_checking()
    elif mode == 'viewerrorlast':  # View last error in log
        logging.error_checking(last=True)
    elif mode == 'clearwizlog':  # Clear wizard.log
        from resources.libs import tools
        tools.remove_file(CONFIG.WIZLOG)
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]Wizard Log Cleared![/COLOR]".format(CONFIG.COLOR2))

    # BACKUP / RESTORE
    elif mode == 'backupbuild':  # Backup Build
        from resources.libs import backup
        backup.backup('build')
    elif mode == 'backupgui':  # Backup guisettings
        from resources.libs import backup
        backup.backup('guifix')
    elif mode == 'backuptheme':  # Backup Theme
        from resources.libs import backup
        backup.backup('theme')
    elif mode == 'backupaddonpack':  # Backup Addon Pack
        from resources.libs import backup
        backup.backup('addon_pack')
    elif mode == 'backupaddon':  # Backup Addon Data
        from resources.libs import backup
        backup.backup('addon_data')
    elif mode == 'restorezip':  # Restore Build
        from resources.libs import backup
        backup.restore_it('build')
    elif mode == 'restoregui':  # Restore Gui
        from resources.libs import backup
        backup.restore_it('gui')
    elif mode == 'restoreaddon':  # Restore Addon Data
        from resources.libs import backup
        backup.restore_it('addon_data')
    elif mode == 'restoreextzip':  # Restore External Build
        from resources.libs import backup
        backup.restore_it_external('build')
    elif mode == 'restoreextgui':  # Restore External guisettings
        from resources.libs import backup
        backup.restore_it_external('gui')
    elif mode == 'restoreextaddon':  # Restore External Addon Data
        from resources.libs import backup
        backup.restore_it_external('addon_data')

    if mode == 'wizardupdate':  # Wizard Update
        from resources.libs import update
        update.wizard_update()
    elif mode == 'forceupdate':  # Addon Tools -> Force Update Addons
        from resources.libs import update
        update.force_update()

    # ADVANCED SETTINGS
    if mode == 'autoadvanced':  # Advanced Settings AutoConfig
        from resources.libs import advanced
        advanced.autoConfig()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'removeadvanced':  # Remove Current Advanced Settings
        from resources.libs import advanced
        advanced.remove_advanced()
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'currentsettings':  # View Current Advanced Settings
        from resources.libs import advanced
        advanced.view_advanced()
    elif mode == 'writeadvanced':  # Write New Advanced Settings
        from resources.libs import advanced
        advanced.write_advanced(name, url)

    # TRAKT
    elif mode == 'savetrakt':  # Save Trakt Data
        from resources.libs import traktit
        traktit.trakt_it('update', name)
    elif mode == 'restoretrakt':  # Recover All Saved Trakt Data
        from resources.libs import traktit
        traktit.trakt_it('restore', name)
    elif mode == 'addontrakt':  # Clear All Addon Trakt Data
        from resources.libs import traktit
        traktit.trakt_it('clearaddon', name)
    elif mode == 'cleartrakt':  # Clear All Saved Trakt Data
        from resources.libs import traktit
        traktit.clear_saved(name)
    elif mode == 'authtrakt':  # Authorize Trakt
        from resources.libs import traktit
        traktit.activate_trakt(name)
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'updatetrakt':  # Update Saved Trakt Data
        from resources.libs import traktit
        traktit.auto_update('all')
    elif mode == 'importtrakt':  # Import Saved Trakt Data
        from resources.libs import traktit
        traktit.import_list(name)
        xbmc.executebuiltin('Container.Refresh()')

    # DEBRID
    elif mode == 'savedebrid':  # Save Debrid Data
        from resources.libs import debridit
        debridit.debrid_it('update', name)
    elif mode == 'restoredebrid':  # Recover All Saved Debrid Data
        from resources.libs import debridit
        debridit.debrid_it('restore', name)
    elif mode == 'addondebrid':  # Clear All Addon Debrid Data
        from resources.libs import debridit
        debridit.debrid_it('clearaddon', name)
    elif mode == 'cleardebrid':  # Clear All Saved Debrid Data
        from resources.libs import debridit
        debridit.clear_saved(name)
    elif mode == 'authdebrid':  # Authorize Debrid
        from resources.libs import debridit
        debridit.activate_debrid(name)
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'updatedebrid':  # Update Saved Debrid Data
        from resources.libs import debridit
        debridit.auto_update('all')
    elif mode == 'importdebrid':  # Import Saved Debrid Data
        from resources.libs import debridit
        debridit.import_list(name)
        xbmc.executebuiltin('Container.Refresh()')

    # LOGIN
    elif mode == 'savelogin':  # Save Login Data
        from resources.libs import loginit
        loginit.login_it('update', name)
    elif mode == 'restorelogin':  # Recover All Saved Login Data
        from resources.libs import loginit
        loginit.login_it('restore', name)
    elif mode == 'addonlogin':  # Clear All Addon Login Data
        from resources.libs import loginit
        loginit.login_it('clearaddon', name)
    elif mode == 'clearlogin':  # Clear All Saved Login Data
        from resources.libs import loginit
        loginit.clear_saved(name)
    elif mode == 'authlogin':  # "Authorize" Login
        from resources.libs import loginit
        loginit.activate_login(name)
        xbmc.executebuiltin('Container.Refresh()')
    elif mode == 'updatelogin':  # Update Saved Login Data
        from resources.libs import loginit
        loginit.auto_update('all')
    elif mode == 'importlogin':  # Import Saved Login Data
        from resources.libs import loginit
        loginit.import_list(name)
        xbmc.executebuiltin('Container.Refresh()')

    # DEVELOPER MENU
    elif mode == 'createqr':  # Developer Menu -> Create QR Code
        from resources.libs import qr
        qr.create_code()
    elif mode == 'testnotify':  # Developer Menu -> Test Notify
        from resources.libs import test
        test.test_notify()
    elif mode == 'testupdate':  # Developer Menu -> Test Update
        from resources.libs import test
        test.test_update()
    elif mode == 'testsavedata':  # Developer Menu -> Test Save Data Settings
        from resources.libs import test
        test.test_save_data_settings()
    elif mode == 'testbuildprompt':  # Developer Menu -> Test Build Prompt
        from resources.libs import test
        test.test_first_run()

    elif mode == 'contact':  # Contact
        from resources.libs import gui
        gui.show_contact(CONFIG.CONTACT)

    xbmcplugin.endOfDirectory(_handle)


if __name__ == 'main':
    route(sys.argv[2][1:])


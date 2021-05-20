import os
import sys

from setup_app.static import InstallTypes
from setup_app.utils import base

def get_setup_options():


    setupOptions = {
        'setup_properties': None,
        'noPrompt': False,
        'downloadWars': False,
        'installOxAuth': True,
        'installOxTrust': True,
        'wrends_install': InstallTypes.LOCAL,
        'installHTTPD': True,
        'installSaml': False,
        'installOxAuthRP': False,
        'installPassport': False,
        'installGluuRadius': False,
        'installScimServer': False,
        'installCasa': False,
        'installOxd': False,
        'installFido2': False,
        'loadTestData': False,
        'allowPreReleasedFeatures': False,
        'listenAllInterfaces': False,
        'cb_install': InstallTypes.NONE,
        'loadTestDataExit': False,
        'loadData': True,
        'properties_password': None,
    }


    if base.argsp.install_local_wrends:
        setupOptions['wrends_install'] = InstallTypes.LOCAL

    if base.argsp.no_oxauth:
        setupOptions['installOxAuth'] = False

    if base.argsp.no_oxtrust:
        setupOptions['installOxTrust'] = False

    setupOptions['installGluuRadius'] = base.argsp.install_gluu_radius

    if base.argsp.ip_address:
        setupOptions['ip'] = base.argsp.ip_address

    if base.argsp.host_name:
        setupOptions['hostname'] = base.argsp.host_name
        
    if base.argsp.org_name:
        setupOptions['orgName'] = base.argsp.org_name

    if base.argsp.email:
        setupOptions['admin_email'] = base.argsp.email

    if base.argsp.city:
        setupOptions['city'] = base.argsp.city

    if base.argsp.state:
        setupOptions['state'] = base.argsp.state

    if base.argsp.country:
        setupOptions['countryCode'] = base.argsp.country

    if base.argsp.application_max_ram:
        setupOptions['application_max_ram'] = base.argsp.application_max_ram

    if base.argsp.oxtrust_admin_password:
        setupOptions['oxtrust_admin_password'] = base.argsp.oxtrust_admin_password

    if base.argsp.ldap_admin_password:
        setupOptions['ldapPass'] = base.argsp.ldap_admin_password

    if base.argsp.f:
        if os.path.isfile(base.argsp.f):
            setupOptions['setup_properties'] = base.argsp.f
            print("Found setup properties %s\n" % base.argsp.f)
        else:
            print("\nOoops... %s file not found for setup properties.\n" %base.argsp.f)

    setupOptions['noPrompt'] = base.argsp.n

    if base.argsp.no_httpd:
        setupOptions['installHTTPD'] = False

    if base.argsp.enable_scim_test_mode:
        setupOptions['scimTestMode'] = 'true'

    setupOptions['installSaml'] = base.argsp.install_shib
    setupOptions['downloadWars'] = base.argsp.w
    setupOptions['installOxAuthRP'] = base.argsp.install_oxauth_rp
    setupOptions['installPassport'] = base.argsp.install_passport
    setupOptions['loadTestData']  = base.argsp.t
    setupOptions['loadTestDataExit'] = base.argsp.x
    setupOptions['allowPreReleasedFeatures'] = base.argsp.allow_pre_released_features
    setupOptions['listenAllInterfaces'] = base.argsp.listen_all_interfaces
    setupOptions['installCasa'] = base.argsp.install_casa
    setupOptions['installOxd'] = base.argsp.install_oxd
    setupOptions['installScimServer'] = base.argsp.install_scim
    setupOptions['installFido2'] = base.argsp.install_fido2
    setupOptions['couchbase_bucket_prefix'] = base.argsp.couchbase_bucket_prefix

    if base.argsp.remote_ldap:
        setupOptions['wrends_install'] = InstallTypes.REMOTE

    if base.argsp.remote_couchbase:
        setupOptions['cb_install'] = InstallTypes.REMOTE

    if base.argsp.no_data:
        setupOptions['loadData'] = False

    if base.argsp.remote_ldap:
        setupOptions['listenAllInterfaces'] = True

    if base.argsp.oxd_use_gluu_storage:
        setupOptions['oxd_use_gluu_storage'] = True

    if base.argsp.import_ldif:
        if os.path.isdir(base.argsp.import_ldif):
            setupOptions['importLDIFDir'] = base.argsp.import_ldif
            print("Found setup LDIF import directory {}\n".format(base.argsp.import_ldif))
        else:
            print("The custom LDIF import directory {} does not exist. Exiting...".format(base.argsp.import_ldif))
            sys.exit(2)

    setupOptions['properties_password'] = base.argsp.properties_password

    return setupOptions

import os
import glob
import shutil

from setup_app import paths
from setup_app.static import AppType, InstallOption
from setup_app.config import Config
from setup_app.installers.jetty import JettyInstaller

class FidoInstaller(JettyInstaller):

    def __init__(self):
        self.service_name = 'fido2'
        self.needdb = True
        self.app_type = AppType.SERVICE
        self.install_type = InstallOption.OPTONAL
        self.install_var = 'installFido2'
        self.register_progess()

        self.source_files = [
                (os.path.join(Config.distGluuFolder, 'fido2.war'), Config.maven_root + '/maven/org/gluu/fido2-server/{0}/fido2-server-{0}.war'.format(Config.oxVersion))
                ]

        self.fido2ConfigFolder = os.path.join(Config.configFolder, 'fido2')
        self.output_folder = os.path.join(Config.outputFolder, 'fido2')
        self.template_folder = os.path.join(Config.templateFolder, 'fido2')
        self.fido2_dynamic_conf_json = os.path.join(self.output_folder, 'dynamic-conf.json')
        self.fido2_static_conf_json = os.path.join(self.output_folder, 'static-conf.json')
        self.ldif_fido2 = os.path.join(self.output_folder, 'fido2.ldif')

    def install(self):

        self.installJettyService(self.jetty_app_configuration[self.service_name], True)

        self.logIt("Copying fido.war into jetty webapps folder...")
        jettyServiceWebapps = os.path.join(self.jetty_base, self.service_name, 'webapps')
        self.copyFile(self.source_files[0][0], jettyServiceWebapps)
        self.war_for_jetty10(os.path.join(jettyServiceWebapps, os.path.basename(self.source_files[0][0])))
        self.enable()

    def render_import_templates(self, do_import=True):
        Config.templateRenderingDict['fido2ConfigFolder'] = self.fido2ConfigFolder
        self.renderTemplateInOut(self.fido2_dynamic_conf_json, self.template_folder, self.output_folder)
        self.renderTemplateInOut(self.fido2_static_conf_json, self.template_folder, self.output_folder)

        Config.templateRenderingDict['fido2_dynamic_conf_base64'] = self.generate_base64_file(self.fido2_dynamic_conf_json, 1)
        Config.templateRenderingDict['fido2_static_conf_base64'] = self.generate_base64_file(self.fido2_static_conf_json, 1)

        self.renderTemplateInOut(self.ldif_fido2, self.template_folder, self.output_folder)

        if do_import:
            ldif_files = [self.ldif_fido2]
            self.dbUtils.import_ldif(ldif_files)


    def create_folders(self):
        for d in ('authenticator_cert', 'mds/cert', 'mds/toc', 'server_metadata'):
            dpath = os.path.join(self.fido2ConfigFolder, d)
            self.run([paths.cmd_mkdir, '-p', dpath])

    def copy_static(self):
        # Fido2 authenticator certs
        target_dir = os.path.join(self.fido2ConfigFolder, 'authenticator_cert')
        for f in ('yubico-u2f-ca-cert.crt', 'HyperFIDO_CA_Cert_V1.pem', 'HyperFIDO_CA_Cert_V2.pem'):
            src = os.path.join(Config.install_dir, 'static/auth/fido2/authenticator_cert/', f)
            self.copyFile(src, target_dir)

        # Fido2 MDS TOC cert
        self.copyFile(
            os.path.join(Config.install_dir, 'static/auth/fido2/mds_toc_cert/metadata-root-ca.cer'),
            os.path.join(self.fido2ConfigFolder, 'mds/cert')
            )

        # copy Apple_WebAuthn_Root_CA
        apple_webauthn = os.path.join(Config.distAppFolder, 'Apple_WebAuthn_Root_CA.pem')
        if os.path.exists(apple_webauthn):
            target_dir = os.path.join(self.fido2ConfigFolder, 'apple')
            self.run([paths.cmd_mkdir, '-p', target_dir])
            self.copyFile(apple_webauthn, target_dir)

    def installed(self):
        return os.path.exists(os.path.join(Config.jetty_base, self.service_name, 'start.ini'))

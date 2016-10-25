import tarfile, os
from dotenv import load_dotenv
from docker_drupal.helpers import message as msg, run as run_cmd

# # import classes to override
from docker_drupal.archive import Archive
# from docker_drupal.builder import Builder

from subprocess import call


# # add new methods
# class DrushLocal:
#     def localtest(self, text):
#         print text
#
# Drush.__bases__ += (DrushLocal,)
#
# class BuilderLocal:
#     def printlocal(self):
#         self.drush.localtest('printlocal')
#
# Builder.__bases__ += (BuilderLocal,)

# # override existing method
# def drush_uli_local(self):
#     print self.config.DRUPAL_ADMIN_USER
#
# Drush.uli = drush_uli_local


# # replace/add new commands
# build_arrays_overrides = {
#     'localtest': ['confirm_action', 'drush.localtest("upwd %s --password=123" % self.config.DRUPAL_ADMIN_USER)'],
#     'drush_uli': ['confirm_action("no")', 'drush.uli'],
# }

from docker_drupal.builder import Builder

class BuilderLocal:

    def enable_mailcatcher(self):
        self.drush.run("en -y smtp ")
        self.drush.run("config-set -y smtp.settings smtp_on true ")
        self.drush.run("config-set -y smtp.settings smtp_host mailcatcher ")
        self.drush.run("config-set -y smtp.settings 'smtp_protocol' 'standard' ")
        self.drush.run("config-set -y smtp.settings 'smtp_port' 1025 ")
        self.drush.run("config-set -y smtp.settings 'smtp_username' '' ")
        self.drush.run("config-set -y smtp.settings 'smtp_password' '' ")
        self.drush.run("config-set -y smtp.settings 'smtp_allowhtml' true ")

    def admin_pass(self):
        print("Set admin password to 123")
        self.drush.run('user-password admin --password="123"')


class ArchiveLocal:
    def unpack_private_files(self):
        src = os.path.join(self.config.BUILD_PATH, 'files', 'private.tar.gz')
        tar = tarfile.open(src)
        dest = os.path.join(self.config.DRUPAL_ROOT, self.config.FILES_DST, 'files')
        tar.extractall(dest)
        tar.close()


Archive.__bases__ += (ArchiveLocal,)

Builder.__bases__ += (BuilderLocal,)

build_arrays_overrides = {
    'build-in-docker': [
        'archive.unpack_files',
        'drupal_settings.copy_settings',

        'database.drop_db',
        'database.create_db',
        'database.import_db',

        'enable_mailcatcher',

        'drush.run("updb")',

        'admin_pass',

        'drush.run("uli")',
    ],
}

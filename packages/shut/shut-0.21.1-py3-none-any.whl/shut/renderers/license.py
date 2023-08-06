# -*- coding: utf8 -*-
# Copyright (c) 2021 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import datetime
import logging
import os

from pkg_resources import resource_string

from .core import Renderer, register_renderer
from shut.data import load_string
from shut.model import AbstractProjectModel, PackageModel
from shut.utils.io.virtual import VirtualFiles

log = logging.getLogger(__name__)

# https://spdx.org/licenses/
LICENSE_TEMPLATE_MAP = {
  'MIT.txt': ['MIT'],
  'BSD2.txt': ['BSD-2-Clause', 'BSD-Simplified', 'BSD-2', 'BSD2'],
  'BSD3.txt': ['BSD-3-Clause', 'BSD-new', 'BSD-3', 'BSD3'],
  'BSD4.txt': ['BSD-4-Clause', 'BSD-old', 'BSD-Original'],
  'Apache2.txt': ['Apache-2.0', 'Apache-2', 'Apache2']
}


class LicenseTemplateDoesNotExist(Exception):
  pass


def get_license_template(license_name: str) -> str:
  for license_filename, license_identifiers in LICENSE_TEMPLATE_MAP.items():
    for license_identifier in license_identifiers:
      if license_name.lower() == license_identifier.lower():
        # NOTE (NiklasRosenstein): See https://github.com/NiklasRosenstein/shut/issues/17
        return load_string(f'license_templates/{license_filename}')
  raise LicenseTemplateDoesNotExist('License template not available for supplied license name', license_name)


def has_license_template(license_name: str) -> bool:
  try:
    get_license_template(license_name)
    return True
  except LicenseTemplateDoesNotExist:
    return False


class LicenseRenderer(Renderer[AbstractProjectModel]):

  def inherits_monorepo_license(self, package: PackageModel) -> bool:
    """
    Returns #True if the *package* inherits the license file of it's mono repository. This is
    only the case if there is a monorepo, and the package and the monorepo have the same license,
    and the license is one for which we deliver a template for.
    """

    assert package.project
    if not package.license:
      if package.project.monorepo and package.project.monorepo.license:
        return True
      return False
    if not has_license_template(package.license):
      return False

    license_file = package.get_license_file()

    # If this is a package and it uses the same license as the monorepo, and the monorepo
    # license exists or is one we would generate, then we skip producing a license for this
    # package.
    if package.project.monorepo and \
        package.project.monorepo.license == package.license and \
        not license_file:
      return True

    return False

  def get_files(self, files: VirtualFiles, model: AbstractProjectModel) -> None:
    if not model.license or (isinstance(model, PackageModel)
        and self.inherits_monorepo_license(model)):
      return

    if not has_license_template(model.license):
      log.warning('Don\'t have a license tempalte for "%s", make sure to keep the license up to date manually.', model.license)
      return

    author = model.get_author()
    assert author, "need author to render license"

    license_file = model.get_license_file()
    license_file = license_file or os.path.join(model.get_directory(), 'LICENSE.txt')
    license_text = get_license_template(model.license)\
        .format(year=datetime.datetime.utcnow().year, author=author.name)
    files.add_static(license_file, license_text)


register_renderer(AbstractProjectModel, LicenseRenderer)

# -*- coding: utf-8 -*-
#
# This file is part of the parce Python package.
#
# Copyright © 2019-2021 by Wilbert Berendsen <info@wilbertberendsen.nl>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
JobManager manages running treebuilder and transformer.

If this is done correctly, treebuilder and transformer don't have to be subclassed
for background threads or Qt or whatever.

"""


from . import util


class JobManager(util.Observable):
    """Manages the updating of the parce tree and an optional transformer.





    """

    def __init__(self):
        """Initialize ourselves."""
        pass # TODO implement

    def register(self, owner, treebuilder=None, transformer=None):
        """Register owner to use treebuilder and transformer.

        The ``owner`` is a generic object which is recognized by the outer
        world as being a text document. If no ``treebuilder`` is specified, a
        default one is installed, same for the transformer.

        """
        pass # TODO implement

    def unregister(self, owner):
        """Remove the ``owner`` from our management."""
        pass # TODO implement


    def update(self, owner, text, root_lexicon=False, position=0, removed=0, added=None):
        """Process the text change, run TreeBuilder and then Transformer.

        This method must be called if your document has its contents changed,
        or wants to change the root lexicon.

        Add the changes to the treebuilder and start it, if it didn't already
        run. When applicable start also the transformer.

        """
        pass # TODO implement

    def set_treebuilder(self, owner, treebuilder):
        """Set a different treebuilder for owner."""
        self.register(owner, treebuilder, self.get_transformer(owner))

    def get_treebuilder(self, owner):
        """Return the treebuilder registered for owner."""
        pass # TODO implement

    def set_transformer(self, owner, transformer):
        """Set a different transformer for owner."""
        self.register(owner, self.get_treebuilder(owner), transformer)

    def get_transformer(self, owner):
        """Return the transformer registered for owner."""
        pass # TODO implement



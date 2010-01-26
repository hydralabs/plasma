# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
*Plasma* is a Python implementation of Flex Messaging and Remoting.

:copyright: Copyright The Plasma Project. All Rights Reserved.
:contact: `plasma-users@plasmads.org <mailto:plasma-users@plasmads.org>`_
:see: http://plasmads.org

:since: September 2009
:status: Pre-Alpha
"""


import pyamf.util.imports


def flex_loader(alias):
    """
    Loader for all aliases with a `flex.` prefix.

    Will return the class related to `alias` or `None`.
    """
    if not alias.startswith('flex.'):
        return

    mod_path = alias.split('.')
    class_ = mod_path[-1]

    mod_path = '.'.join(['plasma'] + mod_path[:-1])

    try:
        mod = __import__(mod_path)
    except ImportError:
        # perhaps some logging here
        return

    mod_path = '.'.join([mod_path, class_])

    try:
        for path in mod_path.split('.')[1:]:
            mod = getattr(mod, path)
    except AttributeError:
        # definitely some logging here
        return

    return mod


def blaze_loader(alias):
    """
    Loader for BlazeDS framework compatibility classes, specifically
    implementing ISmallMessage.

    .. seealso:: `BlazeDS (external)
       <http://opensource.adobe.com/wiki/display/blazeds/BlazeDS>`_
    :since: 0.1
    """
    if alias not in ['DSC', 'DSK', 'DSA']:
        return

    from plasma.flex.messaging.messages import small

    reload(small)

    return pyamf.get_class_alias(alias)


pyamf.unregister_class_loader(pyamf.flex_loader)
pyamf.unregister_class_loader(pyamf.blaze_loader)
pyamf.register_class_loader(flex_loader)
pyamf.register_class_loader(blaze_loader)

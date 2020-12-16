import logging
import os

from ZenPacks.zenoss.ZenPackLib.lib.base.types import multiline


LOG = logging.getLogger('zen.TransformLoader')


def load_transforms(cfg, transform_dir):
    """
    Load transforms from speparate files to inject into the CFG.

    :param cfg: The cfg object to inject the transforms into
    :type cfg: ZenPacks.zenoss.ZenPackLib.lib.spec.ZenPackSpec
    :param transform_dir: The base directory for transform files
    :type transform_dir: str
    """

    LOG.info('Loading transforms for {0}'.format(cfg.name))
    for eclass, cdata in cfg.event_classes.iteritems():
        LOG.debug('Loading transform for event class {0}'.format(eclass))
        cpath = get_transform_path(transform_dir, eclass)
        ctransform = get_transform(cpath)
        if ctransform:
            cdata.transform = ctransform

        for mclass, mdata in cdata.mappings.iteritems():
            LOG.debug('Loading transform for event mapping {0}'.format(mclass))
            mpath = get_transform_path(transform_dir, eclass, mclass)
            mtransform = get_transform(mpath)
            if mtransform:
                mdata.transform = mtransform


def get_transform_path(base_dir, eclass, mapping=None):
    """
    Build the path to the transform file.

    :param base_dir: Base directory for the transforms
    :type base_dir: str
    :param eclass: The event class of the transform
    :type eclass: str
    :param mapping: The event class mapping, if available
    """

    if mapping:
        file_name = '.'.join([mapping, 'py'])
    else:
        file_name = 'class.py'

    class_path = eclass.strip('/').replace('/', os.path.sep)

    return os.path.sep.join([
        base_dir,
        class_path,
        file_name,
        ])


def get_transform(tpath):
    """
    Attempts to load a transform from the path provided.

    :param tpath: Path of the transform to load
    :type tpath: str
    :returns: string of the python code loaded from the file,
        None if the file does not exist
    """
    try:
        tfile = open(tpath, 'r')
        tdata = tfile.read().rstrip()
        tfile.close()
    except IOError:
        LOG.debug('Unable to open {0}'.format(tpath))
        tform = None
    else:
        LOG.debug('Found transform at {0}'.format(tpath))
        tform = multiline(tdata)

    return tform

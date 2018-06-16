from psutil import Process, NoSuchProcess


def kill_recursively(p: Process, force: bool=True):
    """

    :param force:
    :param p:
    :return:
    """
    children = p.children()
    if children:
        for child in children:
            kill_recursively(child, force=force)
    try:
        if force:
            p.kill()
        else:
            p.terminate()
    except NoSuchProcess:
        pass

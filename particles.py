# coding: utf-8

VOID = 0
LIMIT = 1
SAND = 2

def void_particle(env, position):
    """The void particle never does nothing, but, if awaken, it goes back
       to sleep.
    """
    env.sleep(position)

def sand_particle(env, position):
    """The sand particles tries to "fall" into a lower position.
    """
    x, y = position
    moved_to = None

    # if any under elements are void, move there and awake there
    if env[(x, y+1)] == VOID:
        moved_to = (x, y+1)
    elif env[(x-1, y+1)] == VOID:
        moved_to = (x-1, y+1)
    elif env[(x+1, y+1)] == VOID:
        moved_to = (x+1, y+1)

    # if has moved, awake upper elements, move to target
    if moved_to is not None:
        env[moved_to] = SAND
        env.awake(moved_to)
        env[position] = VOID
        env.awake((x, y-1))
        env.awake((x-1, y-1))
        env.awake((x+1, y-1))

    # anyway, sleep this position
    env.sleep(position)

#: The particle types: id and procedure
PARTICLES = {
        VOID: void_particle,
        LIMIT: void_particle,
        SAND: sand_particle
    }


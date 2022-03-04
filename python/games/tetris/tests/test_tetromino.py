from tetromino import Block, BlockS, BlockZ


def test_block_s():
    t = BlockS(3, -4)
    assert [(5, -3), (6, -3), (4, -2), (5, -2)] == t.coordinates
    assert [(4, -4), (4, -3), (5, -3), (5, -2)] == t.rotate().coordinates
    assert [(5, -3), (6, -3), (4, -2), (5, -2)] == t.rotate().coordinates


def test_block_z():
    t = BlockZ(3, -4)
    assert [(4, -3), (5, -3), (5, -2), (6, -2)] == t.coordinates
    assert [(5, -4), (4, -3), (5, -3), (4, -2)] == t.rotate().coordinates
    assert [(4, -3), (5, -3), (5, -2), (6, -2)] == t.rotate().coordinates


def test_create_block():
    block = Block.create(5, 0)
    assert isinstance(block, Block)

from tetromino import Block, BlockS, BlockZ


def test_block_s():
    t = BlockS(5, 0)
    assert [(5, -2), (6, -2), (4, -1), (5, -1)] == t.coordinates
    assert [(5, -3), (5, -2), (6, -2), (6, -1)] == t.rotate().coordinates
    assert [(5, -2), (6, -2), (4, -1), (5, -1)] == t.rotate().coordinates


def test_block_z():
    t = BlockZ(5, 0)
    assert [(4, -2), (5, -2), (5, -1), (6, -1)] == t.coordinates
    assert [(5, -3), (4, -2), (5, -2), (4, -1)] == t.rotate().coordinates
    assert [(4, -2), (5, -2), (5, -1), (6, -1)] == t.rotate().coordinates


def test_create_block():
    block = Block.create(5, 0)
    assert isinstance(block, Block)

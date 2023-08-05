from pollination.honeybee_radiance.multiphase import ViewMatrix
from queenbee.plugin.function import Function


def test_view_mtx():
    function = ViewMatrix().queenbee
    assert function.name == 'view-matrix'
    assert isinstance(function, Function)

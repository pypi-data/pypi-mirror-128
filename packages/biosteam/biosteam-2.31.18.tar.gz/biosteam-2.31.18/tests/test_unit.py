# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2021, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
import pytest
import biosteam as bst
from numpy.testing import assert_allclose

def test_unit_connections():
    from biorefineries.sugarcane import flowsheet as f
    globals().update(f.unit.data)
    assert R301.neighborhood(1) == {T301, D301, S302, H301}
    assert R301.neighborhood(2) == {S302, C301, H301, M302, D301, R301, T301, M301}
    assert R301.neighborhood(100) == R301.neighborhood(1000) == {
        T304, S201, S301, F301, P302, T202, M301, T204, H302, H301, S202, 
        D303, M303, T203, P201, R301, T301, H201, U101, T205, P202, 
        M202, H202, U201, P303, T206, U202, U401, H303, M201, M302, U301, 
        D301, C201, C301, H304, S302, P304, M305, P203, C202, T302, P306,
        U402, U102, U403, P301, T303, U404, D302, P305, U405, U103, M304
    }
    assert R301.get_downstream_units() == {
        T304, P303, P301, D302, H303, M302, U301, D301, P302, C301, H304,
        S302, P304, M305, H302, T302, D303, M303, M304, R301, T301
    }
    ins = tuple(R301.ins)
    outs = tuple(R301.outs)
    R301.disconnect()
    assert not any(R301.ins + R301.outs)
    ins - R301 - outs
    
    class DummyUnit(bst.Unit, isabstract=True, new_graphics=False):
        _N_ins = 2; _N_outs = 2
        
    unit = DummyUnit(None)
    unit.take_place_of(R301)
    assert tuple(unit.ins + unit.outs) == (ins + outs)
    assert not any(R301.ins + R301.outs)
    R301.take_place_of(unit)

def test_unit_graphics():
    bst.settings.set_thermo(['Water', 'Ethanol'], cache=True)
    M = bst.Mixer(None, outs=None)
    assert M._graphics.get_inlet_options(M, 2) == {'headport': 'c'}
    assert M._graphics.get_inlet_options(M, 100) == {'headport': 'c'}
    assert M._graphics.get_outlet_options(M, 0) == {'tailport': 'e'}
    
    S = bst.Splitter(None, outs=None, split=0.5)
    
    GraphicsWarning = bst.exceptions.GraphicsWarning
    with pytest.warns(GraphicsWarning):
        assert S._graphics.get_inlet_options(S, 1) == {'headport': 'c'}
    
    with pytest.warns(GraphicsWarning):
        assert M._graphics.get_outlet_options(M, 1) == {'tailport': 'c'}

def test_equipment_lifetimes():
    from biorefineries.sugarcane import create_tea
    bst.settings.set_thermo(['Water'], cache=True)
    
    class A(bst.Unit):
        _F_BM_default = {
            'Equipment A': 2,
            'Equipment B': 3,
        }
        _default_equipment_lifetime = {
            'Equipment A': 10,
            'Equipment B': 5,
        }
        def _cost(self):
            purchase_costs = self.baseline_purchase_costs
            purchase_costs['Equipment A'] = 1e6
            purchase_costs['Equipment B'] = 1e5
            
    class B(bst.Unit):
        _F_BM_default = {
            'Equipment A': 2,
        }
        _default_equipment_lifetime = 15
        def _cost(self):
            self.baseline_purchase_costs['Equipment A'] = 1e6

    class C(bst.Unit):
        _F_BM_default = {
            'Equipment A': 4,
        }
        def _cost(self):
            self.baseline_purchase_costs['Equipment A'] = 1e6
            
    @bst.decorators.cost('Flow rate', units='kmol/hr', S=1, BM=3,
                         cost=1e6, n=0.6, CE=bst.CE, lifetime=8)
    class D(bst.Unit): pass
    
    @bst.decorators.cost('Flow rate', units='kmol/hr', S=1, BM=4,
                         cost=1e6, n=0.6, CE=bst.CE, lifetime=20)
    class E(bst.Unit): pass
    
    D_feed = bst.Stream('D_feed', Water=1)
    E_feed = D_feed.copy('E_feed')
    units = [A(None, 'A_feed'), B(None, 'B_feed'), C(None, 'C_feed'), D(None, D_feed), E(None, E_feed)]
    test_sys = bst.System('test_sys', units)
    test_sys.simulate()
    tea = create_tea(test_sys)
    table = tea.get_cashflow_table()
    C_FCI = table['Fixed capital investment [MM$]']
    # Test with lang factor = 3 (default for sugarcane biorefinery)
    cashflows_FCI = [6.12, 9.18, 0.  , 0.  , 0.  , 0.  , 0.  , 0.3 , 0.  , 0.  , 3.  ,
                     0.  , 3.3 , 0.  , 0.  , 0.  , 0.  , 3.3 , 3.  , 0.  , 0.  , 0.  ]
    assert_allclose(C_FCI, cashflows_FCI)
    # Cashflows include maintainance and others, so all entries are not zero
    cashflows = [
       -6120000., -9945000., -4321300., -4321300., -4321300., -4321300.,
       -4321300., -4621300., -4321300., -4321300., -7321300., -4321300.,
       -7621300., -4321300., -4321300., -4321300., -4321300., -7621300.,
       -7321300., -4321300., -4321300., -3556300.
    ]
    assert_allclose(tea.cashflow_array, cashflows)
    
    # Test with bare module costs
    tea.lang_factor = None
    table = tea.get_cashflow_table()
    C_FCI = table['Fixed capital investment [MM$]']
    cashflows_FCI = [
        6.12, 9.18, 0.  , 0.  , 0.  , 0.  , 0.  , 0.3 , 0.  , 0.  , 3.  ,
        0.  , 2.3 , 0.  , 0.  , 0.  , 0.  , 2.3 , 3.  , 0.  , 0.  , 0.  
    ]
    assert_allclose(C_FCI, cashflows_FCI)
    cashflows = [
       -6120000., -9945000., -4321300., -4321300., -4321300., -4321300.,
       -4321300., -4621300., -4321300., -4321300., -7321300., -4321300.,
       -6621300., -4321300., -4321300., -4321300., -4321300., -6621300.,
       -7321300., -4321300., -4321300., -3556300.
    ]
    assert_allclose(tea.cashflow_array, cashflows)
    
if __name__ == '__main__':
    test_unit_connections()
    test_unit_graphics()
    test_equipment_lifetimes()